from django.shortcuts import render, redirect, get_object_or_404
import os 
import hashlib
from .models import Estampado, Proveedor, Movimiento_matp
from django.db.models import Q 

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
        id_est = request.POST.get('id_estamp_fk_invent')
        id_pro = request.POST.get('id_proveedor_fk')

        if id_est and id_pro:
            Movimiento_matp.objects.create(
                tipo_mmtp=request.POST.get('tipo_mmtp'),
                talla_mmtp=request.POST.get('talla_mmtp'),
                color_mmtp=request.POST.get('color_mmtp', ''), 
                fecha_mmtp=request.POST.get('fecha_mmtp'),
                stock_mmtp=request.POST.get('stock_mmtp'),
                id_estamp_fk_invent=get_object_or_404(Estampado, id_estamp=id_est),
                id_proveedor_fk=get_object_or_404(Proveedor, id_provee=id_pro)
            )
            return redirect('inventario:lista_mmtp')

    return render(request, "inventario/movimiento_matp/lista.html", {
        'mmtp': Movimiento_matp.objects.all(), 
        'estampados': Estampado.objects.all(), 
        'proveedores': Proveedor.objects.all()
    })

def editar_mmtp(request, id):
    mmtp = get_object_or_404(Movimiento_matp, id_mmtp=id)
    
    if request.method == 'POST':
        mmtp.tipo_mmtp = request.POST.get('tipo_mmtp')
        mmtp.talla_mmtp = request.POST.get('talla_mmtp')
        mmtp.color_mmtp = request.POST.get('color_mmtp', '') # Evita el MultiValueDictKeyError
        mmtp.fecha_mmtp = request.POST.get('fecha_mmtp')
        mmtp.stock_mmtp = request.POST.get('stock_mmtp')
        
        id_est = request.POST.get('id_estamp_fk_invent')
        id_pro = request.POST.get('id_proveedor_fk')
        
        mmtp.id_estamp_fk_invent = get_object_or_404(Estampado, id_estamp=id_est)
        mmtp.id_proveedor_fk = get_object_or_404(Proveedor, id_provee=id_pro)
        mmtp.save()
        return redirect('inventario:lista_mmtp') 

    return render(request, 'inventario/movimiento_matp/editar.html', {
        'mmtp': mmtp,
        'estampados': Estampado.objects.all(),
        'proveedores': Proveedor.objects.all()
    })

def eliminar_mmtp(request, id):
    get_object_or_404(Movimiento_matp, id_mmtp=id).delete()
    return redirect('inventario:lista_mmtp')


# --- ESTAMPADOS ---
def lista_estampado(request):
    query = request.GET.get('q') 
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre_estamp')
        costo = request.POST.get('costo_adi')
        tipo = request.POST.get('tipo_estamp')
        archivo_img = request.FILES.get('archivo_imagen')

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
        estampado.costo_adi = request.POST.get('costo_adi')
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