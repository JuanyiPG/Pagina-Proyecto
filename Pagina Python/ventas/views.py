import hashlib

from django.shortcuts import get_object_or_404, redirect, render
from .models import Abono,Pedido, Variacion, Det_valor, Producto

#-------------------- CRUD VARIACION --------------------------

def lista_var(request):
    variaciones = Variacion.objects.all()
    return render(request, 'ventas/lista_var.html', {'variaciones': variaciones})

#----------------- CRUD PRODUCTO ------------------------------

def lista_producto(request): 
    productos = Producto.objects.all()
    return render(request, 'producto/lista_product.html', {'productos': productos})

def crear_producto(request): 
    nuevo_hash = None #inicializamos la variable

    if request.method == 'POST': 
        #POST para textos plano, FILES, para img, pdf, etc
        imagen_produc = request.FILES.get('imagen_produc')
        nom_produc = request.POST.get('nom_produc')
        desc_produc = request.POST.get('desc_produc')
        categoria_produc = request.POST.get('cat_produc')
        estado_produc = request.POST.get('estado_produc')

        if imagen_produc: 
            #Generar el hash
            hasher = hashlib.sha256()
            for chunk in imagen_produc.chunks():
                hasher.update(chunk)
            nuevo_hash = hasher.hexdigest()

            #Rebobinar el archivo
            imagen_produc.seek(0)

            #Verificar si ya existe el hash
            if Producto.objects.filter(imagen_hash=nuevo_hash).exists():
                return render(request, 'producto/form_producto.html',{
                    'error': 'ERROR: Esta prenda ya ha sido subida anteriormente.'
            })
        
        Producto.objects.create(imagen_product=imagen_produc, imagen_hash=nuevo_hash, nom_produc=nom_produc,
                                desc_produc=desc_produc, categoria_produc=categoria_produc,estado_produc=estado_produc )
        
        return redirect('ventas:lista_product')
    return render(request, 'producto/form_producto.html')


def editar_producto(request, id): 
    productos = get_object_or_404(Producto, id_produc=id)
    if request.method == 'POST': 
        productos.imagen_product = request.POST['imagen_product']
        productos.nom_produc = request.POST['nom_produc']
        productos.desc_produc = request.POST['desc_produc']
        productos.categoria_produc = request.POST['categoria_produc']
        productos.estado_produc = request.POST['estado_produc']
        productos.save()
        return redirect('lista_producto')
    return render(request, 'producto/editar_producto.html', {'productos': productos})


def eliminar_producto(request, product_id): 
    productos = get_object_or_404(Producto, id_produc=product_id)
    if request.method == 'POST':
        productos.delete()
        return redirect('lista_productos')
    return render(request, 'producto/eliminar_producto.html', {'productos':productos})


#----------------- CRUD ABONO ------------------------------

def lista_abono(request):
    abonos = Abono.objects.all()
    return render(request, 'abono/lista_abono.html', {'abonos': abonos})

def crear_abono(request, detalle_id):
    detalle = get_object_or_404(Det_valor, id_det_valor= detalle_id)
    if request.method == 'POST': 
        monto_abono = request.POST.get['monto_abono']
        metodo_pago = request.POST['metodo_pago']
        descripcion = request.POST['descripcion']
        Abono.objects.create(id_det_valor= detalle, monto_abono = monto_abono, metodo_pago = metodo_pago, descripcion = descripcion)
    
    return render(request, 'abono/form_abono.html', {})

def eliminar_abono(request): 
    abonos = get_object_or_404(Abono, id=id)
    if request.method == 'POST': 
        abonos.delete()
        return redirect('lista_abono')
    return render(request, 'abono/eliminar_abono.html', {'abonos' : abonos})

#---------------- CRUD DETALLE VALOR -------------------

def lista_det_val(request): 
    detalles = Det_valor.objects.all()
    return render(request, 'detVal/lista_detVal.html', {'detalles', detalles})

#--------------------- CRUD PEDIDO -----------------

def lista_pedido(request): 
    pedidos = Pedido.objects.all()
    return render(request, 'pedido/lista_pedido.html', {'pedidos': pedidos})

def crear_pedido(request): 
    if request.method == 'POST': 
        nom_ped = request.POST['nom_ped']
        talla_ped = request.POST['talla_ped']
        color_ped = request.POST['color_ped']
        categoria_ped = request.POST['categoria_ped']
        material_ped = request.POST['material_ped']
        cant_ped = request.POST['cant_ped']
        desc_ped = request.POST['desc_ped']
        subtotal_ped = request.POST['subtotal_ped']
        valor_ped = request.POST['valor_ped']
        estado_ped = request.POST['estado_ped']
        metodo_pago = request.POST['metodo_pago']

    return render(request, 'pedido/form_pedido.html', {})

def eliminar_pedido(request, id): 
    pedidos = get_object_or_404(Pedido, id_pedido = id)
    if request.method == 'POST': 
        pedidos.delete()
        return redirect('lista_pedido')
    return render(request, 'pedido/eliminar_pedido.html', {'pedidos': pedidos})