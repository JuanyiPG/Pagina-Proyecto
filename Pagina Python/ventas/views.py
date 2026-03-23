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
    producto = get_object_or_404(Producto, id_produc=id)
    if request.method == 'POST': 
        nueva_imagen = request.FILES.get('imagen_product')
        # Solo asignamos la imagen si 'nueva_imagen' no es None
        if nueva_imagen:
            producto.imagen_product = nueva_imagen
            
            # Si usas el sistema de hash, recúclalo aquí también
            hasher = hashlib.sha256()
            for chunk in nueva_imagen.chunks():
                hasher.update(chunk)
            producto.imagen_hash = hasher.hexdigest()
            nueva_imagen.seek(0)

        producto.nom_produc = request.POST.get('nom_produc')
        producto.desc_produc = request.POST['desc_produc']
        producto.categoria_produc = request.POST.get('categoria_produc')
        producto.estado_produc = request.POST['estado_produc']
        producto.save()
        return redirect('ventas:lista_product')
    return render(request, 'producto/editar_producto.html', {'producto': producto})


def eliminar_producto(request, product_id): 
    producto = get_object_or_404(Producto, id_produc=product_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ventas:lista_product')
    return render(request, 'producto/eliminar_producto.html', {'producto':producto})


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
        # Es más seguro usar .get() para evitar errores si falta un campo
        Pedido.objects.create(
            nom_ped=request.POST.get('nom_ped'),
            talla_ped=request.POST.get('talla_ped'),
            color_ped=request.POST.get('color_ped'),
            categoria_ped=request.POST.get('categoria_ped'),
            material_ped=request.POST.get('material_ped'),
            cant_ped=request.POST.get('cant_ped'),
            desc_ped=request.POST.get('desc_ped'),
            valor_ped=request.POST.get('valor_ped'),
            estado_ped=request.POST.get('estado_ped'),
            metodo_pago=request.POST.get('metodo_pago')
        )
        return redirect('ventas:lista_pedido') # Asegúrate que este nombre coincida con tu urls.py
    return render(request, 'pedido/form_pedido.html', {})

def editar_pedido(request, id): 
    # CORRECCIÓN: El primer parámetro es el Modelo, no request
    pedido = get_object_or_404(Pedido, id_pedido=id)

    if request.method == 'POST': 
        pedido.nom_ped = request.POST.get('nom_ped')
        pedido.talla_ped = request.POST.get('talla_ped')
        pedido.color_ped = request.POST.get('color_ped')
        pedido.categoria_ped = request.POST.get('categoria_ped')
        pedido.cant_ped = request.POST.get('cant_ped') # Corregido: antes tenías desc_ped
        pedido.valor_ped = request.POST.get('valor_ped')
        pedido.estado_ped = request.POST.get('estado_ped')
        pedido.metodo_pago = request.POST.get('metodo_pago')
        pedido.save() # Esto disparará el cálculo del subtotal automáticamente
        return redirect('ventas:lista_pedido') 
        
    return render(request, 'pedido/editar_pedido.html', {'pedido': pedido})

def eliminar_pedido(request): 
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST': 
        pedido.delete()
        return redirect('lista_pedido')
    return render(request, 'pedido/eliminar_pedido.html', {'pedido' : pedido})
    