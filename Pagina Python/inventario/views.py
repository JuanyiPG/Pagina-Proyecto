from django.shortcuts import render, redirect, get_object_or_404
from .models import Estampado, Proveedor, Movimiento_matp

# --- PROVEEDORES ---
def lista_provee(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            nom_provee=request.POST.get('nom_provee'),
            fech_ingre=request.POST.get('fech_ingre'),
            num_tel=request.POST.get('num_tel')
        )
        return redirect('lista_provee') 

    proveedores = Proveedor.objects.all()
    return render(request, "proveedor/lista.html", {'proveedor': proveedores})

def editar_provee(request, id):
    proveedor = get_object_or_404(Proveedor, id_provee=id)
    if request.method == "POST":
        proveedor.nom_provee = request.POST.get('nom_provee')
        proveedor.fech_ingre = request.POST.get('fech_ingre')
        proveedor.num_tel = request.POST.get('num_tel')
        proveedor.save()
        return redirect('lista_provee')
    return render(request, 'proveedor/editar.html', {'proveedor': proveedor})

def eliminar_provee(request, id):
    get_object_or_404(Proveedor, id_provee=id).delete()
    return redirect('lista_provee')

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
            return redirect('lista_mmtp')

    return render(request, "movimiento_matp/lista.html", {
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
        return redirect('lista_mmtp') 

    return render(request, 'movimiento_matp/editar.html', {
        'mmtp': mmtp,
        'estampados': Estampado.objects.all(),
        'proveedores': Proveedor.objects.all()
    })

def eliminar_mmtp(request, id):
    get_object_or_404(Movimiento_matp, id_mmtp=id).delete()
    return redirect('lista_mmtp')

# --- ESTAMPADOS ---
def lista_estampado(request):
    if request.method == 'POST':
        Estampado.objects.create(
            nombre_estamp=request.POST.get('nombre_estamp'),
            link_estamp=request.POST.get('link_estamp'),
            costo_adi=request.POST.get('costo_adi'),
            tipo_estamp=request.POST.get('tipo_estamp')
        )
        return redirect('lista_estampado')
    return render(request, "estampado/lista.html", {'estampados': Estampado.objects.all()})

def editar_estampado(request, id):
    estampado = get_object_or_404(Estampado, id_estamp=id)
    if request.method == "POST":
        estampado.nombre_estamp = request.POST.get('nombre_estamp')
        estampado.link_estamp = request.POST.get('link_estamp')
        estampado.costo_adi = request.POST.get('costo_adi')
        estampado.tipo_estamp = request.POST.get('tipo_estamp')
        estampado.save()
        return redirect('lista_estampado')
    return render(request, 'estampado/editar.html', {'estampado': estampado})

def eliminar_estampado(request, id):
    get_object_or_404(Estampado, id_estamp=id).delete()
    return redirect('lista_estampado')