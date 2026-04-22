from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa
import os 
from decimal import Decimal, InvalidOperation
import hashlib
from .models import Estampado, Proveedor, Movimiento_matp
from ventas.models import Producto 
from django.db.models import Q 
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from .serializers import MovimientoSerializer
from django.conf import settings
import base64
from .serializers import ProveedorSerializer
from rest_framework import viewsets

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
    
        if tipo not in ['ENTRADA', 'SALIDA']:
            return render(request, "inventario/movimiento_matp/lista.html", {
                'error': 'Tipo de movimiento no válido',
                'mmtp': Movimiento_matp.objects.all(),
                'proveedores': Proveedor.objects.all()
            })

        if id_pro:
            proveedor_instancia = get_object_or_404(Proveedor, id_provee=id_pro)
            
            Movimiento_matp.objects.create(
                tipo_mmtp=tipo, # Usamos la variable ya validada
                color_mmtp=request.POST.get('color_mmtp', ''), 
                fecha_mmtp=request.POST.get('fecha_mmtp'),
                stock_mmtp=request.POST.get('stock_mmtp'),
                mat_mmtp=request.POST.get('mat_mmtp'),
                id_proveedor_fk=proveedor_instancia
            )
            return redirect('inventario:lista_mmtp')

    return render(request, "inventario/movimiento_matp/lista.html", {
        'mmtp': Movimiento_matp.objects.all(), 
        'proveedores': Proveedor.objects.all()
    })

def editar_mmtp(request, id):
    mmtp = get_object_or_404(Movimiento_matp, id_mmtp=id)
    
    if request.method == 'POST':
        mmtp.tipo_mmtp = request.POST.get('tipo_mmtp')
        mmtp.color_mmtp = request.POST.get('color_mmtp', '') # Evita el MultiValueDictKeyError
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

@api_view(['GET'])
def report_mmtp(request):
    movimiento= Movimiento_matp.objects.all()
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'IMG', 'logo.png')

    
    try:
        with open(logo_path, "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode('utf-8')
            logo_final = f"data:image/png;base64,{data}"
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        logo_final = "" 

    context = {
        'movimientos': movimiento,
        'Logo': logo_final 
    }

    template= get_template('reportes/mmtp.html')
    html_string = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reporte_Movimiento_Materia_Prima.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    
    return response


@api_view(['POST'])
def carga_masiva(request):
    archivo = request.FILES.get('archivo_excel')
    if not archivo:
        return Response({"error": "No hay archivo"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        df = pd.read_excel(archivo)
        df['fecha_mmtp'] = pd.to_datetime(df['fecha_mmtp']).dt.date
        datos = df.to_dict(orient='records')
        
        serializador = MovimientoSerializer(data=datos, many=True)

        if serializador.is_valid():
            serializador.save()
            return Response({"msj": "Carga masiva realizada con éxito"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- ESTAMPADOS ---
def lista_estampado(request):
    query = request.GET.get('q') 
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre_estamp')
        precio = request.POST.get('costo_adi')
        tipo = request.POST.get('tipo_estamp')
        archivo_img = request.FILES.get('archivo_imagen')
        
        try: 
            limpiar = precio.replace('$', '').replace(',','.').strip()
            costo = Decimal(limpiar)
        except(InvalidOperation, TypeError):
            costo = Decimal('0.000')
        
        nuevo_hash = None
        if archivo_img:
            hasher = hashlib.sha256()
            for chunk in archivo_img.chunks():
                hasher.update(chunk)
            nuevo_hash = hasher.hexdigest()
            archivo_img.seek(0)

            if Estampado.objects.filter(imagen_hash=nuevo_hash).exists():
                return render(request, "inventario/estampado/lista.html", {
                    'estampados': Estampado.objects.all(),
                    'error': '¡Atención! Este diseño ya existe en el inventario.',
                    'query': query
                })

        Estampado.objects.create(
            nombre_estamp=nombre,
            costo_adi=costo,
            tipo_estamp=tipo,
            imagen_estamp=archivo_img,
            imagen_hash=nuevo_hash
        )
        return redirect('inventario:lista_estampado')
    if query:
        # Si hay algo en el buscador, filtramos por nombre O por técnica
        estampados = Estampado.objects.filter(
            Q(nombre_estamp__icontains=query) | 
            Q(tipo_estamp__icontains=query)
        )
    else:
        estampados = Estampado.objects.all()

    return render(request, "inventario/estampado/lista.html", {
        'estampados': estampados, 
        'query': query # Enviamos 'query' para que el texto no se borre del input al buscar
    })

def editar_estampado(request, id):
    estampado = get_object_or_404(Estampado, id_estamp=id)
    
    if request.method == "POST":
        nueva_img = request.FILES.get('archivo_imagen')
        if nueva_img:
            # 1. Borramos la imagen anterior de la carpeta para limpiar
            if estampado.imagen_estamp:
                if os.path.exists(estampado.imagen_estamp.path):
                    os.remove(estampado.imagen_estamp.path)
            
            # 2. Asignamos la nueva imagen 
            estampado.imagen_estamp = nueva_img
            
            # 3. RECUERDA: Si cambias la imagen, ¡debes recalcular el HASH!
            hasher = hashlib.sha256()
            for chunk in nueva_img.chunks():
                hasher.update(chunk)
            estampado.imagen_hash = hasher.hexdigest()
            nueva_img.seek(0) # Siempre rebobinar

        # Actualizamos los demás campos de texto
        estampado.nombre_estamp = request.POST.get('nombre_estamp')
        costo = request.POST.get('costo_adi')
        try: 
            limpiar = costo.replace('$','').replace(',','.').strip()
            precio_adi = Decimal(limpiar)
        except(InvalidOperation, TypeError): 
            precio_adi = Decimal('0.000')
        
        estampado.costo_adi = precio_adi
        estampado.tipo_estamp = request.POST.get('tipo_estamp')
        
        estampado.save() # Guarda todos los cambios en MySQL
        return redirect('inventario:lista_estampado')

    return render(request, 'inventario/estampado/editar.html', {'estampado': estampado})


def eliminar_estampado(request, id):
    estampado = get_object_or_404(Estampado, id_estamp=id)
    
    # 2. Verificamos si el estampado tiene una imagen asociada
    if estampado.imagen_estamp:
        # Obtenemos la ruta física en tu computadora (C:/xampp/htdocs/...)
        ruta_archivo = estampado.imagen_estamp.path
        
        # 3. Si el archivo existe físicamente, lo borramos
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
    
    # 4. Ahora sí, borramos el registro de la base de datos
    estampado.delete()
    
    return redirect('inventario:lista_estampado')


def modelo(request, producto_id):
    producto = get_object_or_404(Producto, id_produc=producto_id)
    # Traemos todos los diseños guardados en el inventario
    estampados = Estampado.objects.all() 
    
    return render(request, 'inventario/modelo/index.html', {
        'producto': producto,
        'estampados': estampados  
    })

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer