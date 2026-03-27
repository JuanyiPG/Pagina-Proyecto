from django.utils import timezone
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.db import transaction
import hashlib
from django.db.models import Sum, Max
from datetime import timedelta
from usuarios.views import solo_personal, login_requerido_custom

from django.shortcuts import get_object_or_404, redirect, render
from .models import Abono,Pedido, Variacion, Det_valor, Producto, Estampado, Movimiento_matp,Det_mov_matp,Cliente

#---------------------- COMPROBAR LOGIN ------------------------------

def obtener_cliente_actual(request):
    id_user = request.session.get('usuario_id')
    return Cliente.objects.get(id_usuario_fk=id_user)

#-------------------- CRUD VARIACION --------------------------

def lista_var(request):
    variaciones = Variacion.objects.all()
    return render(request, 'ventas/lista_var.html', {'variaciones': variaciones})

@login_requerido_custom
def crear_variacion(request, producto_id, pedido_id): 
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('login')

    producto = get_object_or_404(Producto, producto_id)
    estampados = Estampado.objects.all()
    if request.method == 'POST': 
        estampado_elegido = request.POST.get('id_estam')
        estam_obj = get_object_or_404(Estampado, id_estam = (estampado_elegido))
        
        variacion = Variacion.objects.create(
        talla_var = request.POST.get('talla_var'),
        cant_soli = int(request.POST.get('cant_soli')),
        color_var = request.POST.get('color_var'),
        mat_var = request.POST.get('mat_var'),
        costo_var = estam_obj.costo_adi,
        id_estam_fk_var = estam_obj
        )

        pedido_actual = get_object_or_404(Pedido, id_pedido = pedido_id)
        Det_valor.objects.create(
            valor_total = (producto.precio + variacion.costo_var)* variacion.cant_soli, 
            cant = variacion.cant_soli,
            tipo_pedido = "Personalizado", 
            id_ped_fk_detval = pedido_actual, 
            id_var_fk_detval = variacion, 
            id_prod_fk_detval = producto
        )

        return redirect('carrito')

    return render(request, 'personalizar.html', {
        #lo que este entre las '', es para poder llamar los datos en el HTML, ejemplo producto.nom y el 
        #otro es la variable la cual tiene todos los datos que traemos desde la base de datos.
        'producto': producto,
        'estampados': estampados
    })

@login_requerido_custom
def editar_variacion(request, detalle_id): 
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('login')
    
    detalle = get_object_or_404(Det_valor, id_var=detalle_id)
    variacion = detalle.id_var_fk_detval
    producto = detalle.id_prod_fk_detval

    estampado = Estampado.objects.all()

    if request.method == 'POST': 
        id_estam_nuevo = request.POST.get('id_estam')
        estampado_obj = get_object_or_404(Estampado, id_estam = id_estam_nuevo)

        variacion.talla_var = request.POST.get('talla_var')
        variacion.cant_soli = request.POST.get('cant_soli')
        variacion.color_var = request.POST.get('color_var')
        variacion.mat_var = request.POST.get('mat_var')
        variacion.costo_var = estampado_obj.costo_adi
        variacion.save()

        detalle.cant = variacion.cant_soli
        detalle.valor_total = (producto.precio + variacion.costo_var) * variacion.cant_soli

        return redirect ('carrito')
    return render (request, 'personalizar.html',{
        'producto': producto,
        'estampados': estampado,
        'variacion': variacion, # Enviamos la variación actual para llenar el form
        'es_edicion': True      # Una bandera para saber que estamos editando
    })

def eliminar_variacion (request, detalle_id):
    detalle = get_object_or_404(Det_valor, id_det_valor=detalle_id)
    
    # Si tiene una variación personalizada, la borramos primero
    if detalle.id_var_fk_detval:
        detalle.id_var_fk_detval.delete()
    
    # Luego borramos el renglón del detalle
    detalle.delete()
    
    return redirect('carrito')



#----------------- CRUD PRODUCTO ------------------------------
@solo_personal
def lista_producto(request): 
    productos = Producto.objects.all()
    rol_usuario = request.session.get('rol')

    # 2. Comprobamos si es del personal (Admin o Empleado)
    if rol_usuario in ['Administrador', 'Empleado']:
        # Si es admin/empleado, ve la tabla de gestión (CRUD)
        return render(request, 'producto/lista_product.html', {'productos': productos})
    else:
        # Si es cliente o visitante anónimo, ve la tienda bonita
        return render(request, 'PAGINAS_LUXY_PROD/PAGINA_PROD.html', {'productos': productos})

@solo_personal
def crear_producto(request): 
    nuevo_hash = None #inicializamos la variable

    if request.method == 'POST': 
        #POST para textos plano, FILES, para img, pdf, etc
        imagen_produc = request.FILES.get('imagen_produc')
        nom_produc = request.POST.get('nom_produc')
        desc_produc = request.POST.get('desc_produc')
        categoria_produc = request.POST.get('cat_produc')
        estado_produc = request.POST.get('estado_produc')
        precio = request.POST.get('precio')

        #Converir String a Decimal
        try: 
            precio_limpio = precio.replace('$', '').replace(',', '').strip()
            valor = Decimal(precio_limpio)
        except(InvalidOperation, TypeError):
            valor = Decimal('0.00')

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
                                desc_produc=desc_produc, categoria_produc=categoria_produc,estado_produc=estado_produc, precio=valor )
        
        return redirect('ventas:lista_product')
    return render(request, 'producto/form_producto.html')

@solo_personal
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
        producto.precio = request.POST['precio']
        try: 
            precio_limpio = producto.precio.replace('$', '').replace(',', '').strip()
            valor = Decimal(precio_limpio)
        except(InvalidOperation, TypeError):
            valor = Decimal('0.00')

        producto.save()
        return redirect('ventas:lista_product')
    return render(request, 'producto/editar_producto.html', {'producto': producto})

@solo_personal
def eliminar_producto(request, product_id): 
    producto = get_object_or_404(Producto, id_produc=product_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ventas:lista_product')
    return render(request, 'producto/eliminar_producto.html', {'producto':producto})

#----------------- PRODUCTO SIN VARIACION ---------------------
@login_requerido_custom
def producto_sin_personalizar(request, producto_id):
    print("¡ENTRÉ A LA VISTA!") 
    if request.method == 'POST':
        print("¡ES UN POST!")
    producto = get_object_or_404(Producto, id_produc=producto_id)
    tallas = ["S", "M", "L", "XL", "XXL"]
    
    if request.method == 'POST':
        cliente = obtener_cliente_actual(request)
        talla = request.POST.get('talla')
        
        try:
            cantidad = int(request.POST.get('cantidad', 1))
        except ValueError:
            cantidad = 1

        with transaction.atomic():
            pedido, creado = Pedido.objects.get_or_create(
                id_clien_fk=cliente,
                estado_ped='Carrito', 
                defaults={'subtotal_ped': 0, 'valor_ped': 0, 'metodo_pago': 'Pendiente'}
            )

            Det_valor.objects.create(
                id_ped_fk_detval=pedido, 
                id_prod_fk_detval=producto,
                talla=talla, 
                cant=cantidad,
                valor_total=producto.precio * cantidad,
                tipo_pedido='Estandar',
                id_var_fk_detval=None  # Porque no es personalizado
            )

        messages.success(request, f"{producto.nom_produc} añadido al carrito.")
        # IMPORTANTE: Después de agregar, lo mandamos a ver su carrito
        return redirect('ventas:ver_carrito')
    
    # --- PARTE 3: RENDERIZAR LA PÁGINA (SI ES GET O SI EL POST FALLÓ) ---
    return render(request, 'producto/vista_producto.html', {
        'producto': producto,
        'tallas': tallas
    })
#----------------- CRUD ABONO ------------------------------

def lista_abono(request):
    abonos = Abono.objects.all()
    return render(request, 'abono/lista_abono.html', {'abonos': abonos})

@login_requerido_custom
def crear_abono(request, pedido_id):
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('login')
    
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
    
    if request.method == 'POST':
        monto_str = request.POST.get('monto_abono', '0')
        try:
            # Limpiamos el monto (tu modelo usa BigIntegerField)
            valor = int(monto_str.replace('$', '').replace('.', '').replace(',', '').strip())
            
            with transaction.atomic():
                # --- PUNTO CRÍTICO: ¿Es el primer abono? ---
                tiene_abonos = Abono.objects.filter(id_pedido_fk_abono=pedido).exists()
                
                if not tiene_abonos:
                    # Si es el primero, intentamos descontar de la bodega
                    gestionar_inventario(pedido, 'RESTAR')
                
                # Creamos el abono (esto disparará el save() del modelo que cambia el estado a PAGADO si aplica)
                Abono.objects.create(
                    id_pedido_fk_abono=pedido,
                    monto_abono=valor,
                    metodo_pago=request.POST.get('metodo_pago'),
                    descripcion=request.POST.get('descripcion', '')
                )
                
            messages.success(request, "Abono registrado correctamente.")
            return redirect('lista_abono')
            
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('crear_abono', pedido_id=pedido_id)

    return render(request, 'abono/form_abono.html', {'pedido': pedido})

def eliminar_abono(request, id): # <-- IMPORTANTE: Agregar el id aquí
    abono = get_object_or_404(Abono, id_abono=id) # Usamos el nombre de tu PK: id_abono
    if request.method == 'POST': 
        abono.delete()
        return redirect('lista_abono')
    return render(request, 'abono/eliminar_abono.html', {'abono': abono})


#---------------- CRUD DETALLE VALOR -------------------

def lista_det_val(request): 
    detalles = Det_valor.objects.all()
    return render(request, 'detVal/lista_detVal.html', {'detalles': detalles})

#--------------------- CRUD PEDIDO -----------------

def lista_pedido(request): 
    pedidos = Pedido.objects.all()
    return render(request, 'pedido/lista_pedido.html', {'pedidos': pedidos})

    # Ahora redirigimos a la vista de "Personalizar" (crear_variacion) 
    # pasándole el ID del pedido que acabamos de encontrar o crear.
    return redirect('crear_variacion', producto_id=producto.id_produc, pedido_id=pedido.id_pedido)

@login_requerido_custom
def finalizar_pedido(request, pedido_id):
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('login')
    # Buscamos el pedido que se creó en el paso anterior
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
    
    if request.method == 'POST':
        # Traemos todos los detalles (prendas) que el cliente metió en este pedido
        detalles = Det_valor.objects.filter(id_ped_fk_detval=pedido)
        
        if not detalles.exists():
            messages.error(request, "Tu carrito está vacío.")
            return redirect('lista_productos')

        # 1. SUMA TOTAL Y DÍAS DE PRODUCCIÓN
        # Usamos aggregate para que la base de datos haga el trabajo pesado
        resultados = detalles.aggregate(
            total=Sum('valor_total'),
            max_espera=Max('id_prod_fk_detval__dias_produccion')
        )
        
        total_real = resultados['total'] or 0
        dias_produccion = resultados['max_espera'] or 1

        # 2. TRANSFORMACIÓN DEL PEDIDO
        # Actualizamos los campos que estaban en 0 o vacíos
        pedido.subtotal_ped = total_real
        pedido.valor_ped = total_real
        pedido.metodo_pago = request.POST.get('metodo_pago')
        pedido.fecha_ped = timezone.now().date() # Fecha de hoy
        pedido.fecha_entrega = timezone.now().date() + timedelta(days=dias_produccion)
        
        # CAMBIO DE ESTADO: Aquí deja de ser un carrito
        pedido.estado_ped = 'Confirmado' 
        pedido.save()

        messages.success(request, f"¡Pedido confirmado! Estará listo el {pedido.fecha_entrega}")
        return redirect('ventas:lista_pedido')

    return render(request, 'pedido/finalizar.html', {'pedido': pedido})

@login_requerido_custom
def editar_pedido(request, id): 
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('login')
    # CORRECCIÓN: El primer parámetro es el Modelo, no request
    pedido = get_object_or_404(Pedido, id_pedido=id)

    if request.method == 'POST':
        pedido.fecha_ped = request.POST.get('fecha_ped')
        pedido.subtotal_ped = request.POST.get('subtotal_ped')
        pedido.valor_ped = request.POST.get('valor_ped')
        pedido.estado_ped = request.POST.get('estado_ped')
        pedido.metodo_pago = request.POST.get('metodo_pago')
        pedido.fecha_entrega = request.POST.get('fecha_entrega')
        pedido.save() # Esto disparará el cálculo del subtotal automáticamente
        return redirect('ventas:lista_pedido') 
        
    return render(request, 'pedido/editar_pedido.html', {'pedido': pedido})

@login_requerido_custom
def eliminar_pedido(request, id):
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('login')
    pedido = get_object_or_404(Pedido, id_pedido=id)
    
    if request.method == 'POST':
        with transaction.atomic():
            # Si el pedido ya tenía abonos, significa que el inventario se descontó
            if Abono.objects.filter(id_pedido_fk_abono=pedido).exists():
                gestionar_inventario(pedido, 'SUMAR') # Devolvemos el material
            
            pedido.delete()
            messages.success(request, "Pedido eliminado y materiales devueltos al stock.")
            return redirect('ventas:lista_pedido')
            
    return render(request, 'pedido/eliminar_pedido.html', {'pedido': pedido})

#------------------------ CARRITO --------------------------

@login_requerido_custom
def ver_carrito(request):
    usuario_id = request.session.get('usuario_id')

    try:
        cliente = Cliente.objects.get(id_clien=usuario_id)
    except Cliente.DoesNotExist:
        # Si no hay sesión manual, redirigimos al login
        return redirect('usuarios:login')

    # CORRECCIÓN AQUÍ: Usamos la variable 'cliente' que definimos arriba
    # En lugar de request.user.cliente
    pedido = Pedido.objects.filter(id_clien_fk=cliente, estado_ped='Carrito').first()
    
    if pedido:
        # Traemos todos los detalles de ese pedido
        items = Det_valor.objects.filter(id_ped_fk_detval=pedido)
        # Sumamos el total para mostrarlo en el HTML
        total = items.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    else:
        items = []
        total = 0

    return render(request, 'pedido/carrito.html', {
        'pedido': pedido,
        'items': items,
        'total': total
    })

@login_requerido_custom
def eliminar_del_carrito(request, detalle_id):
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('login')
    
    # Buscamos el detalle que el cliente quiere quitar
    detalle = get_object_or_404(Det_valor, id_det_valor=detalle_id)
    
    # Verificamos que el pedido aún sea un 'Carrito' (Seguridad)
    if detalle.id_ped_fk_detval.estado_ped != 'Carrito':
        messages.error(request, "No puedes eliminar productos de un pedido ya confirmado.")
        return redirect('ventas:lista_pedido')

    with transaction.atomic():
        # Si el detalle tiene una variación (talla, color, etc.), la borramos primero
        if detalle.id_var_fk_detval:
            detalle.id_var_fk_detval.delete()
        
        # Luego borramos el detalle del carrito
        detalle.delete()
        
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('ver_carrito')

#------------- DET_MOV_MATP ---------------------------------
def matp_producto(request, producto_id): 
    producto = get_object_or_404(Producto, id_produc = producto_id)
    materiales = Movimiento_matp.objects.all()

    if request.method == 'POST': 
        id_material = request.POST.get('material')
        cantidad = request.POST.get('cantidad')

        Det_mov_matp.objects.create(
            producto = producto,
            materia_prima = id_material,
            cantidad_usada = cantidad
        )

        return redirect('detalle_producto', producto_id=producto.id_produc)
    return render(request, 'admin/registrar_producto.html',{
        'producto': producto,
        'materiales': materiales
    })

def gestionar_inventario(pedido, operacion):
    """
    operacion: 'RESTAR' (Venta/Abono), 'SUMAR' (Cancelación)
    """
    detalles = Det_valor.objects.filter(id_ped_fk_detval=pedido)
    
    with transaction.atomic():
        for item in detalles:
            # Buscamos la receta en Det_mov_matp usando 'producto' (como en tu modelo)
            receta = Det_mov_matp.objects.filter(producto=item.id_prod_fk_detval)
            
            for insumo in receta:
                material = insumo.materia_prima
                # Cantidad necesaria = (lo que gasta 1) * (cantidad comprada)
                cantidad_total = insumo.cantidad_usada * item.cant

                if operacion == 'RESTAR':
                    if material.stock_movi_mtp >= cantidad_total:
                        material.stock_movi_mtp -= cantidad_total
                    else:
                        raise ValueError(f"No hay suficiente {material.tipo_movi_mtp} para {item.id_prod_fk_detval.nom_produc}")
                
                elif operacion == 'SUMAR':
                    material.stock_movi_mtp += cantidad_total
                
                material.save()