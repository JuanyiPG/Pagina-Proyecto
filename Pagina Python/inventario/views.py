from datetime import date
import os
import uuid
import json
import base64
import hashlib
import pandas as pd
from decimal import Decimal
from django.contrib import messages
from dateutil.relativedelta import relativedelta

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
from ventas.models import Det_mov_matp, Producto, Pedido, Det_valor, Cliente, Variacion
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
    # Calcular límites de fechas para hoy y dos meses atrás
    hoy = timezone.now().date()
    hace_dos_meses = hoy - relativedelta(months=2)
    
    if hace_dos_meses.year < hoy.year:
        hace_dos_meses = date(hoy.year, 1, 1)

    if request.method == 'POST':
        fecha_str = request.POST.get('fech_ingre')
        
        if fecha_str:
            fecha_usuario = date.fromisoformat(fecha_str)
            
            if fecha_usuario > hoy:
                messages.error(request, "Error: La fecha de ingreso no puede ser mayor a la actual.")
                return redirect('inventario:lista_provee')
                
            if fecha_usuario < hace_dos_meses:
                messages.error(request, f"Error: La fecha no puede ser anterior al {hace_dos_meses.strftime('%d/%m/%Y')}.")
                return redirect('inventario:lista_provee')

        Proveedor.objects.create(
            nom_provee=request.POST.get('nom_provee'),
            fech_ingre=fecha_str,
            num_tel=request.POST.get('num_tel')
        )
        messages.success(request, f"Proveedor guardado con éxito")
        return redirect('inventario:lista_provee') 
        
    proveedores = Proveedor.objects.all()
    
    return render(request, "inventario/proveedor/lista.html", {
        'proveedor': proveedores,
        'fecha_maxima': hoy.isoformat(),
        'fecha_minima': hace_dos_meses.isoformat()  
    })

def editar_provee(request, id):
    proveedor = get_object_or_404(Proveedor, id_provee=id)

    hoy = timezone.now().date()
    hace_dos_meses = hoy - relativedelta(months=2)
    
    if hace_dos_meses.year < hoy.year:
        hace_dos_meses = date(hoy.year, 1, 1)

    if request.method == "POST":
        fecha_str = request.POST.get('fech_ingre')
        
        if fecha_str:
            fecha_usuario = date.fromisoformat(fecha_str)

            if fecha_usuario > hoy:
                messages.error(request, "Error: La fecha de ingreso no puede ser mayor a la actual.")
                return redirect('inventario:editar_provee', id=id) 
            if fecha_usuario < hace_dos_meses:
                messages.error(request, f"Error: La fecha no puede ser anterior al {hace_dos_meses.strftime('%d/%m/%Y')}.")
                return redirect('inventario:editar_provee', id=id)

        proveedor.nom_provee = request.POST.get('nom_provee')
        proveedor.fech_ingre = fecha_str
        proveedor.num_tel = request.POST.get('num_tel')
        proveedor.save()
        
        messages.success(request, f"Proveedor actualizado con éxito")
        return redirect('inventario:lista_provee')
        
    return render(request, 'inventario/proveedor/editar.html', {
        'proveedor': proveedor,
        'fecha_maxima': hoy.isoformat(),
        'fecha_minima': hace_dos_meses.isoformat()
    })

def eliminar_provee(request, id):
    get_object_or_404(Proveedor, id_provee=id).delete()
    return redirect('inventario:lista_provee')

# --- MOVIMIENTOS MATP ---

def obtener_motivo_pedido(h):
    try:
        # Aquí debes tener un código similar a este que busca el pedido:
        if h.pedido_origen_id:  # o como tengas nombrado el campo en tu modelo
            # 🌟 IMPORTANTE: Envolvemos el .get() para atrapar el error si no existe
            pedido = Pedido.objects.get(id_pedido=h.pedido_origen_id)
            return f"Pedido #{pedido.id_pedido} - Cliente"
        
        # Si está asociado a un proveedor
        if h.id_proveedor_fk_id:
            return f"Entrada Proveedor"
            
        return "Manual / Ajuste"

    except Pedido.DoesNotExist:
        # 🛡️ Si el pedido fue eliminado, evitamos que la página se rompa
        return "Pedido Eliminado (Historial)"

def lista_mmtp(request):
    if request.method == "POST":
        tipo = request.POST.get('tipo_mmtp')
        id_pro = request.POST.get('id_proveedor_fk')
        
        if id_pro:
            proveedor_instancia = get_object_or_404(Proveedor, id_provee=id_pro)
            stock_recibido = int(request.POST.get('stock_mmtp', 0))
            stock_final = stock_recibido if stock_recibido > 0 else 0
            
            Movimiento_matp.objects.create(
                tipo_mmtp=tipo,
                color_mmtp=request.POST.get('color_mmtp', ''), 
                fecha_mmtp=request.POST.get('fecha_mmtp'),
                stock_mmtp=stock_final,
                mat_mmtp=request.POST.get('mat_mmtp'),
                id_proveedor_fk=proveedor_instancia,
                pedido_origen=None # proveedores no tienen un pedido de cliente asociado
            )
            messages.success(request, f"Materia Prima guardada con éxito")
            return redirect('inventario:lista_mmtp')

    mmtp = Movimiento_matp.objects.all()

    for m in mmtp:
        h_queryset = list(m.history.all().order_by('history_date'))
        procesados = []
        
        for i, h in enumerate(h_queryset):
            stock_en_esta_foto = float(h.stock_mmtp)
            
            if i == 0:
                antes = 0
            else:
                antes = float(h_queryset[i-1].stock_mmtp)
            
            variacion = stock_en_esta_foto - antes
            
            # Definimos visualmente si subió o bajó el stock
            tipo_mov_real = 'ENTRADA' if variacion >= 0 else 'SALIDA'
            
            # Trae el motivo real leyendo la clave foránea guardada en la foto del historial
            motivo_real = obtener_motivo_pedido(h)
            
            procesados.append({
                'fecha': h.history_date,
                'antes': antes,
                'variacion': abs(variacion),
                'tipo': tipo_mov_real,
                'despues': stock_en_esta_foto,
                'motivo': motivo_real
            })
            
        procesados.reverse()
        m.historial_calculado = procesados

        if procesados:
            m.motivo_principal = procesados[0]['motivo']
        else:
            m.motivo_principal = "Manual"

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
        mmtp._history_change_reason = "Manual"
        mmtp.save()
        messages.success(request, f"Materia Prima actualizado con exito")
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
    m = get_object_or_404(Movimiento_matp, id_mmtp=id)
    h_queryset = list(m.history.all().order_by('history_date'))
    procesados = []
    
    for i, h in enumerate(h_queryset):
        stock_en_esta_foto = float(h.stock_mmtp)
        
        if i == 0:
            antes = 0
        else:
            antes = float(h_queryset[i-1].stock_mmtp)
        
        variacion = stock_en_esta_foto - antes
        tipo_mov_real = 'ENTRADA' if variacion >= 0 else 'SALIDA'
        
        # 🌟 AQUÍ TAMBIÉN LLAMAMOS A NUESTRA FUNCIÓN DE LA VISTA:
        motivo_operacion = obtener_motivo_pedido(h)
        
        procesados.append({
            'fecha': h.history_date,
            'antes': antes,
            'variacion': abs(variacion),
            'tipo': tipo_mov_real,
            'despues': stock_en_esta_foto,
            'motivo': motivo_operacion  
        })
        
    procesados.reverse()
    m.historial_calculado = procesados

    return render(request, "inventario/movimiento_matp/lista.html", {
        'mmtp': [m],  
        'proveedores': Proveedor.objects.all()
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
        messages.success(request, f"Estampado guardado con exito")
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
        messages.success(request, f"Estampado actualizado con exito")
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
    tallas = producto.tallas_disponibles.split(',') if producto.tallas_disponibles else ["S", "M", "L", "XL", "XXL"]
    # ---------------------------

    return render(request, 'inventario/modelo/index.html', {
        'producto': producto,
        'estampados': estampados,
        'tallas': tallas  # <--- ¡IMPORTANTE: Agrega esto aquí!
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

# ... (Todo el resto de tus importaciones y funciones de Proveedores/Movimientos quedan exactamente IGUAL) ...

def guardar_diseno_3d(request):
    if request.method == 'POST':
        try:
            # 1. IDENTIFICACIÓN DE SESIÓN FLEXIBLE
            cliente_usuario = obtener_cliente_actual(request)
            es_empleado = request.session.get('username') is not None or not cliente_usuario

            # 2. CARGA DE DATOS
            data = json.loads(request.body)
            producto_id = data.get('producto_id')
            color = data.get('color')
            talla = data.get('talla') 
            cantidad = int(data.get('cantidad', 1))
            estampado_id = data.get('estampado_id')
            lista_ids_estampados = data.get('lista_estampados', []) 
            total_estampados_escena = int(data.get('cantidad_total_estampados', 0))
            foto_frente_base64 = data.get('foto_frente')
            
            # --- NUEVO: Capturar el costo adicional por el tamaño del estampado ---
            # Si viene del cliente (que no tiene esta opción), por defecto es 0.
            costo_tamano_estampado = float(data.get('costo_tamano_estampado', 0))
            escala_estampado = float(data.get('escala_estampado',0.4))

            producto_base = get_object_or_404(Producto, id_produc=producto_id)

            # 3. LÓGICA DE PRECIOS
            precio_unitario = float(producto_base.precio)
            extra_total_estampados = 0
            estampado_obj_principal = None

            for est_id in lista_ids_estampados:
                if est_id == "imagen_propia": continue
                try:
                    est_temp = Estampado.objects.get(id_estamp=est_id)
                    extra_total_estampados += float(est_temp.costo_adi)
                    if str(est_id) == str(estampado_id):
                        estampado_obj_principal = est_temp
                except Estampado.DoesNotExist: continue
            
            if not estampado_obj_principal and estampado_id and estampado_id != "imagen_propia":
                try: estampado_obj_principal = Estampado.objects.get(id_estamp=estampado_id)
                except: pass

            lista_solo_catalogo = [x for x in lista_ids_estampados if x != "imagen_propia"]
            amount_propios = total_estampados_escena - len(lista_solo_catalogo)
            if amount_propios > 0:
                extra_total_estampados += (20000 * amount_propios)

            # --- NUEVO: Sumar el costo del tamaño del estampado al total de extras ---
            extra_total_estampados += costo_tamano_estampado

            precio_unitario += extra_total_estampados
            valor_total_final = int(precio_unitario * cantidad)

            # 4. PROCESAR IMAGEN
            archivo_foto = None
            if foto_frente_base64 and ';base64,' in foto_frente_base64:
                format, imgstr = foto_frente_base64.split(';base64,')
                ext = format.split('/')[-1]
                nombre_archivo = f"diseno_{uuid.uuid4()}.{ext}"
                archivo_foto = ContentFile(base64.b64decode(imgstr), name=nombre_archivo)

            # 5. GUARDADO ATÓMICO
            with transaction.atomic():
                personalizacion = PedidoPersonalizado.objects.create(
                    producto=producto_base,
                    estampado=estampado_obj_principal, 
                    color_hex=color,
                    tipo_personalizacion="3D",
                    foto_frente=archivo_foto,
                    precio_final=precio_unitario 
                )

                nueva_variacion = Variacion.objects.create(
                    talla_var=talla,
                    cant_soli=cantidad,
                    color_var=color,
                    mat_var="Algodón",
                    costo_var=precio_unitario, 
                    id_estam_fk_var=estampado_obj_principal 
                )

                # DETERMINAR PEDIDO
                if es_empleado:
                    pedido_asociado = Pedido.objects.create(
                        subtotal_ped=0, valor_ped=0, 
                        estado_ped='Procesando_Emp', metodo_pago='Efectivo',
                        id_clien_fk=None 
                    )
                else:
                    pedido_asociado = obtener_o_crear_pedido_cliente(cliente_usuario)

                detalle = Det_valor.objects.create(
                    id_ped_fk_detval=pedido_asociado,
                    id_prod_fk_detval=producto_base,
                    id_var_fk_detval=nueva_variacion,
                    id_personalizacion_3d=personalizacion,
                    valor_total=valor_total_final, 
                    tipo_pedido="Venta Personalizada"
                )

            return JsonResponse({
                    'status': 'success', 
                    'detalle_id': detalle.id_det_valor, 
                    'precio_final': valor_total_final
                })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


def eliminar_pedido_personalizado(request, id):
    pedido = get_object_or_404(PedidoPersonalizado, id=id)
    for img in [pedido.foto_frente, pedido.foto_espalda, pedido.foto_lateral]:
        if img and os.path.exists(img.path): os.remove(img.path)
    pedido.delete()
    return redirect('ventas:ver_carrito')
