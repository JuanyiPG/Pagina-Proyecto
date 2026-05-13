import os
import uuid
import json
import base64
import hashlib
import pandas as pd
from decimal import Decimal

# Django Core
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.core.files.base import ContentFile
from django.template.loader import get_template
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

# PDF y Reportes
from xhtml2pdf import pisa

# Django Rest Framework
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Modelos y Views de otras Apps (Luxy Fashion Bridge)
from .models import Estampado, Proveedor, Movimiento_matp, PedidoPersonalizado
from .serializers import MovimientoSerializer, ProveedorSerializer
from django.contrib.auth.decorators import login_required

# Importaciones desde Ventas (Para el Carrito)
from ventas.models import Producto, Pedido, Det_valor, Cliente, Variacion
from ventas.views import obtener_cliente_actual

# Importaciones desde Usuarios (Para Seguridad)
from usuarios.models import Usuario
from usuarios.views import login_requerido_custom, solo_personal

# Si tienes decoradores personalizados en usuarios/views.py
# from usuarios.views import login_requerido_custom

# --- FUNCIONES AUXILIARES ---

def b64_to_file(data_url, name):
    """Convierte una cadena base64 de Three.js en un archivo de imagen para Django."""
    if not data_url or ';base64,' not in data_url:
        return None
    try:
        format, imgstr = data_url.split(';base64,')
        ext = format.split('/')[-1]
        return ContentFile(base64.b64decode(imgstr), name=f"{name}.{ext}")
    except Exception as e:
        print(f"Error en b64_to_file: {e}")
        return None

# --- PROVEEDORES ---

def lista_provee(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            nom_provee=request.POST.get('nom_provee'),
            fech_ingre=request.POST.get('fech_ingre'),
            num_tel=request.POST.get('num_tel')
        )
        return redirect('inventario:lista_provee') 
    proveedores = Proveedor.objects.all()
    return render(request, "inventario/proveedor/lista.html", {'proveedor': proveedores})

def editar_provee(request, id):
    proveedor = get_object_or_404(Proveedor, id_provee=id)
    if request.method == "POST":
        proveedor.nom_provee = request.POST.get('nom_provee')
        proveedor.fech_ingre = request.POST.get('fech_ingre')
        proveedor.num_tel = request.POST.get('num_tel')
        proveedor.save()
        return redirect('inventario:lista_provee')
    return render(request, 'inventario/proveedor/editar.html', {'proveedor': proveedor})

def eliminar_provee(request, id):
    get_object_or_404(Proveedor, id_provee=id).delete()
    return redirect('inventario:lista_provee')

# --- MOVIMIENTOS MATP ---

def lista_mmtp(request):
    if request.method == "POST":
        tipo = request.POST.get('tipo_mmtp')
        id_pro = request.POST.get('id_proveedor_fk')
        
        if id_pro:
            proveedor_instancia = get_object_or_404(Proveedor, id_provee=id_pro)
            
            # 1. CORRECCIÓN DE LÓGICA:
            # Queremos que si el número es negativo se vuelva 0, 
            # pero si es positivo se mantenga igual.
            stock_recibido = int(request.POST.get('stock_mmtp', 0))
            stock_final = stock_recibido if stock_recibido > 0 else 0
            
            Movimiento_matp.objects.create(
                tipo_mmtp=tipo,
                color_mmtp=request.POST.get('color_mmtp', ''), 
                fecha_mmtp=request.POST.get('fecha_mmtp'),
                stock_mmtp=stock_final, # Guardamos el valor validado
                mat_mmtp=request.POST.get('mat_mmtp'),
                id_proveedor_fk=proveedor_instancia
            )
            return redirect('inventario:lista_mmtp')

    # 2. PROCESAMIENTO PARA EL MODAL (HISTORIAL)
    # Traemos todos los movimientos
    mmtp = Movimiento_matp.objects.all()

    for m in mmtp:
        # Obtenemos el historial cronológico (del más viejo al más nuevo)
        h_queryset = m.history.all().order_by('history_date')
        
        procesados = []
        saldo = 0
        
        for h in h_queryset:
            # Usamos getattr para evitar problemas con campos que el editor ve "grises"
            cantidad = float(getattr(h, 'stock_mmtp', 0))
            tipo_mov = getattr(h, 'tipo_mmtp', 'ENTRADA')
            
            antes = saldo
            if tipo_mov == 'ENTRADA':
                despues = antes + cantidad
            else:
                despues = antes - cantidad
                if despues < 0: despues = 0
            
            procesados.append({
                'fecha': h.history_date,
                'antes': antes,
                'variacion': cantidad,
                'tipo': tipo_mov,
                'despues': despues
            })
            saldo = despues # El final de este es el inicio del próximo
            
        # Guardamos la lista invertida (más nuevo arriba) dentro del objeto
        procesados.reverse()
        m.historial_calculado = procesados

    return render(request, "inventario/movimiento_matp/lista.html", {
        'mmtp': mmtp,
        'proveedores': Proveedor.objects.all()
    })

def editar_mmtp(request, id):
    mmtp = get_object_or_404(Movimiento_matp, id_mmtp=id)
    if request.method == 'POST':
        mmtp.tipo_mmtp = request.POST.get('tipo_mmtp')
        mmtp.color_mmtp = request.POST.get('color_mmtp', '')
        mmtp.fecha_mmtp = request.POST.get('fecha_mmtp')
        mmtp.stock_mmtp = request.POST.get('stock_mmtp')
        mmtp.mat_mmtp = request.POST.get('mat_mmtp')
        id_pro = request.POST.get('id_proveedor_fk')
        mmtp.id_proveedor_fk = get_object_or_404(Proveedor, id_provee=id_pro)
        mmtp.save()
        return redirect('inventario:lista_mmtp') 

    return render(request, 'inventario/movimiento_matp/editar.html', {
        'mmtp': mmtp,
        'proveedores': Proveedor.objects.all()
    })

def eliminar_mmtp(request, id):
    get_object_or_404(Movimiento_matp, id_mmtp=id).delete()
    return redirect('inventario:lista_mmtp')

#----------------------------- historial mov MatP -----------------------------------------------

def history_MatP(request, id):
    # 1. Buscamos el material por su ID
    matP = get_object_or_404(Movimiento_matp, id_mmtp=id)
    
    # 2. Obtenemos el historial desde el primero que se creó (cronológico)
    # Importante: Usamos order_by('history_date') para que la suma sea correcta
    h_queryset = matP.history.all().order_by('history_date')
    
    datos_para_tabla = []
    saldo_acumulado = 0

    for h in h_queryset:
        # Obtenemos el valor de stock. Si no existe, usamos 0.
        valor_movimiento = getattr(h, 'stock_mmtp', 0)
        tipo = getattr(h, 'tipo_mmtp', 'ENTRADA')
        
        antes = saldo_acumulado
        
        if tipo == 'ENTRADA':
            despues = antes + valor_movimiento
        else:
            despues = antes - valor_movimiento
            if despues < 0: despues = 0 # Evitar negativos
            
        datos_para_tabla.append({
            'fecha': h.history_date,
            'stock_antes': antes,
            'variacion': valor_movimiento,
            'tipo': tipo,
            'stock_despues': despues
        })
        
        # El saldo final de este registro es el acumulado para el siguiente
        saldo_acumulado = despues

    # 3. Volteamos la lista para que el movimiento más nuevo aparezca arriba
    datos_para_tabla.reverse()

    # 4. Enviamos 'historial' al template
    return render(request, 'inventario/movimiento_matp/lista.html', {
        'matP': matP,
        'historial': datos_para_tabla 
    })


@api_view(['GET'])
def report_mmtp(request):
    movimientos = Movimiento_matp.objects.all()
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'IMG', 'logo.png')
    
    try:
        with open(logo_path, "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode('utf-8')
            logo_final = f"data:image/png;base64,{data}"
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        logo_final = "" 

    context = {
        'movimientos': movimientos,
        'Logo': logo_final 
    }

    template= get_template('reportes/mmtp.html')
    html_string = template.render(context)

    template = get_template('reportes/mmtp.html')
    html_string = template.render({'movimientos': movimientos, 'Logo': logo_final})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reporte_Movimiento.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    return response

@api_view(['POST'])
def carga_masiva(request):
    archivo = request.FILES.get('archivo_excel')
    if not archivo:
        return Response({"error": "No hay archivo"}, status=400)
    try:
        df = pd.read_excel(archivo)
        df['fecha_mmtp'] = pd.to_datetime(df['fecha_mmtp']).dt.date
        serializador = MovimientoSerializer(data=df.to_dict(orient='records'), many=True)
        if serializador.is_valid():
            serializador.save()
            return Response({"msj": "Carga masiva exitosa"}, status=201)
        return Response(serializador.errors, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# --- ESTAMPADOS ---

def lista_estampado(request):
    query = request.GET.get('q') 
    if request.method == 'POST':
        nombre = request.POST.get('nombre_estamp')
        precio = request.POST.get('costo_adi')
        tipo = request.POST.get('tipo_estamp')
        archivo_img = request.FILES.get('archivo_imagen')
        
        try: 
            costo = Decimal(precio.replace('$', '').replace(',','.').strip())
        except:
            costo = Decimal('0.00')
        
        nuevo_hash = None
        if archivo_img:
            hasher = hashlib.sha256()
            for chunk in archivo_img.chunks(): hasher.update(chunk)
            nuevo_hash = hasher.hexdigest()
            archivo_img.seek(0)
            if Estampado.objects.filter(imagen_hash=nuevo_hash).exists():
                return render(request, "inventario/estampado/lista.html", {
                    'estampados': Estampado.objects.all(),
                    'error': '¡Atención! Este diseño ya existe.',
                    'query': query
                })

        Estampado.objects.create(
            nombre_estamp=nombre, costo_adi=costo, tipo_estamp=tipo,
            imagen_estamp=archivo_img, imagen_hash=nuevo_hash
        )
        return redirect('inventario:lista_estampado')

    estampados = Estampado.objects.filter(Q(nombre_estamp__icontains=query) | Q(tipo_estamp__icontains=query)) if query else Estampado.objects.all()
    return render(request, "inventario/estampado/lista.html", {'estampados': estampados, 'query': query})

def editar_estampado(request, id):
    estampado = get_object_or_404(Estampado, id_estamp=id)
    if request.method == "POST":
        nueva_img = request.FILES.get('archivo_imagen')
        if nueva_img:
            if estampado.imagen_estamp and os.path.exists(estampado.imagen_estamp.path):
                os.remove(estampado.imagen_estamp.path)
            estampado.imagen_estamp = nueva_img
            hasher = hashlib.sha256()
            for chunk in nueva_img.chunks(): hasher.update(chunk)
            estampado.imagen_hash = hasher.hexdigest()
            nueva_img.seek(0)

        estampado.nombre_estamp = request.POST.get('nombre_estamp')
        try:
            estampado.costo_adi = Decimal(request.POST.get('costo_adi').replace('$','').replace(',','.').strip())
        except:
            estampado.costo_adi = Decimal('0.00')
        
        estampado.tipo_estamp = request.POST.get('tipo_estamp')
        estampado.save()
        return redirect('inventario:lista_estampado')
    return render(request, 'inventario/estampado/editar.html', {'estampado': estampado})

def eliminar_estampado(request, id):
    estampado = get_object_or_404(Estampado, id_estamp=id)
    if estampado.imagen_estamp and os.path.exists(estampado.imagen_estamp.path):
        os.remove(estampado.imagen_estamp.path)
    estampado.delete()
    return redirect('inventario:lista_estampado')

# --- PERSONALIZACIÓN 3D ---
@ensure_csrf_cookie
def modelo(request, producto_id):
    producto = get_object_or_404(Producto, id_produc=producto_id)
    estampados = Estampado.objects.all() 
    return render(request, 'inventario/modelo/index.html', {
        'producto': producto,
        'estampados': estampados  
    })

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

def b64_to_file(data, filename):
    """Convierte una cadena Base64 enviada por Three.js en un archivo de imagen real"""
    if data and ';base64,' in data:
        try:
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            return ContentFile(base64.b64decode(imgstr), name=f"{filename}.{ext}")
        except Exception as e:
            print(f"Error al decodificar imagen 3D: {e}")
    return None

# inventario/views.py

def guardar_diseno_3d(request):
    if request.method == 'POST':
        try:
            # 1. Identificar al cliente (tu función de sesión manual)
            cliente_usuario = obtener_cliente_actual(request)
            if not cliente_usuario:
                return JsonResponse({'status': 'error', 'message': 'Sesión no válida'}, status=401)

            # 2. Cargar los datos que vienen del JavaScript
            data = json.loads(request.body)
            producto_id = data.get('producto_id')
            color = data.get('color')
            talla = data.get('talla', 'M')
            cantidad = int(data.get('cantidad', 1))
            estampado_id = data.get('estampado_id')
            foto_frente_base64 = data.get('foto_frente')

            # --- AQUÍ ESTABA EL ERROR: Necesitamos definir producto_base ---
            producto_base = get_object_or_404(Producto, id_produc=producto_id)

            # 3. Procesar la captura del 3D (Base64 a archivo real)
            archivo_foto = None
            if foto_frente_base64 and ';base64,' in foto_frente_base64:
                format, imgstr = foto_frente_base64.split(';base64,')
                ext = format.split('/')[-1]
                nombre_archivo = f"diseno_{uuid.uuid4()}.{ext}"
                archivo_foto = ContentFile(base64.b64decode(imgstr), name=nombre_archivo)

            # 4. Buscar el estampado si existe
            estampado_obj = None
            if estampado_id:
                try:
                    estampado_obj = Estampado.objects.get(id_estamp=estampado_id)
                except Estampado.DoesNotExist:
                    estampado_obj = None

            # 5. Guardar todo en la base de datos
            with transaction.atomic():
                # A. Crear la personalización (Donde se guarda la foto)
                personalizacion = PedidoPersonalizado.objects.create(
                    producto=producto_base,
                    estampado=estampado_obj,
                    color_hex=color,
                    tipo_personalizacion="3D",
                    foto_frente=archivo_foto,
                    precio_final=producto_base.precio
                )

                # B. Crear la variación física
                nueva_variacion = Variacion.objects.create(
                    talla_var=talla,
                    cant_soli=cantidad,
                    color_var=color,
                    mat_var="Algodón",
                    costo_var=producto_base.precio,
                    id_estam_fk_var=estampado_obj 
                )

                # C. Buscar o crear el carrito del cliente
                pedido, _ = Pedido.objects.get_or_create(
                    id_clien_fk=cliente_usuario,
                    estado_ped='Carrito',
                    defaults={'subtotal_ped': 0, 'valor_ped': 0, 'metodo_pago': 'Pendiente'}
                )

                # D. Crear el detalle final
                Det_valor.objects.create(
                    id_ped_fk_detval=pedido, 
                    id_prod_fk_detval=producto_base,
                    id_var_fk_detval=nueva_variacion,
                    id_personalizacion_3d=personalizacion,
                    valor_total=int(producto_base.precio * cantidad),
                    tipo_pedido='Personalizado'
                )

            return JsonResponse({'status': 'success', 'message': '¡Diseño guardado correctamente!'})

        except Exception as e:
            print(f"Error detallado: {str(e)}") # Esto lo verás en tu terminal
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


def eliminar_pedido_personalizado(request, id):
    pedido = get_object_or_404(PedidoPersonalizado, id=id)
    for img in [pedido.foto_frente, pedido.foto_espalda, pedido.foto_lateral]:
        if img and os.path.exists(img.path): os.remove(img.path)
    pedido.delete()
    return redirect('ventas:ver_carrito')
