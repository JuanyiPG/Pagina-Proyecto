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
        return redirect('ventas:lista_product')

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

        return redirect('ventas:ver_carrito')

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

        return redirect ('ventas:ver_carrito')
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
    
    return redirect('ventas:ver_carrito')



#----------------- CRUD PRODUCTO ------------------------------

def lista_producto(request): 
    productos = Producto.objects.all()
    return render(request, 'PAGINAS_LUXY_PROD/PAGINA_PROD.html', {'productos': productos})
    
def lista_producto_admin(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/producto/lista_product.html', {'productos': productos})

#@solo_personal
def crear_producto(request): 
    nuevo_hash = None

    if request.method == 'POST': 
        #POST para textos plano, FILES, para img, pdf, etc
        imagen_produc = request.FILES.get('imagen_produc')
        nom_produc = request.POST.get('nom_produc')
        gen_produc = request.POST.get('gen_produc')
        desc_produc = request.POST.get('desc_produc')
        categoria_produc = request.POST.get('cat_produc')
        estado_produc = request.POST.get('estado_produc')
        precio = request.POST.get('precio')

        #Converir String a Decimal
        try: 
            precio_limpio = precio.replace('$', '').replace(',', '.', '""').strip()
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
                return render(request, 'ventas/producto/form_producto.html',{
                    'error': 'ERROR: Esta prenda ya ha sido subida anteriormente.'
            })
        
        Producto.objects.create(imagen_product=imagen_produc, imagen_hash=nuevo_hash, nom_produc=nom_produc, gen_produc=gen_produc,
                                desc_produc=desc_produc, categoria_produc=categoria_produc,estado_produc=estado_produc, precio=valor )
        
        return redirect('ventas:lista_producto_admin')
    return render(request, 'ventas/producto/form_producto.html')


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
        producto.gen_produc = request.POST.get('gen_produc')
        producto.desc_produc = request.POST['desc_produc']
        producto.categoria_produc = request.POST.get('categoria_produc')
        producto.estado_produc = request.POST['estado_produc']
        precio = request.POST['precio']
        try: 
            precio_limpio = precio.replace('$', '').replace(',', '.').strip()
            valor = Decimal(precio_limpio)
        except(InvalidOperation, TypeError):
            valor = Decimal('0.00')

        producto.precio = valor
        producto.save()
        return redirect('ventas:lista_producto_admin')
    return render(request, 'ventas/producto/editar_producto.html', {'producto': producto})


def eliminar_producto(request, product_id): 
    producto = get_object_or_404(Producto, id_produc=product_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ventas:lista_product')
    return render(request, 'ventas/producto/eliminar_producto.html', {'producto':producto})

#----------------- PRODUCTO SIN VARIACION ---------------------
@login_requerido_custom
def producto_sin_personalizar(request, producto_id):
    producto = get_object_or_404(Producto, id_produc=producto_id)
    tallas = ["S", "M", "L", "XL", "XXL"]
    colores = ["rojo", "blanco", "gris", "azul"]
    
    if request.method == 'POST':
        cliente = obtener_cliente_actual(request)
        talla = request.POST.get('talla')
        color = request.POST.get('color')
        
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
                color = color,
                cant=cantidad,
                valor_total=producto.precio * cantidad,
                tipo_pedido='Estandar',
                id_var_fk_detval=None
            )

        messages.success(request, f"{producto.nom_produc} añadido al carrito.")
        return redirect('ventas:lista_product')
    
    return render(request, 'ventas/producto/vista_producto.html', {
        'producto': producto,
        'tallas': tallas,
        'colores': colores
    })
#----------------- CRUD ABONO ------------------------------

def lista_abono(request):
    abonos = Abono.objects.all()
    return render(request, 'ventas/abono/lista_abono.html', {'abonos': abonos})

@login_requerido_custom
def crear_abono(request, pedido_id):
    cliente = obtener_cliente_actual(request)
    if not cliente: 
        return redirect('login')
    
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
    
    # 1. Calculamos totales actuales
    items = Det_valor.objects.filter(id_ped_fk_detval=pedido)
    total_productos = items.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    
    total_abonado_previo = Abono.objects.filter(id_pedido_fk_abono=pedido).aggregate(Sum('monto_abono'))['monto_abono__sum'] or 0
    saldo_pendiente = total_productos - total_abonado_previo

    if request.method == 'POST':
        monto_str = request.POST.get('monto_abono', '0')
        # Si no llega método, ponemos uno por defecto para evitar el error 1048
        metodo = request.POST.get('metodo_pago', 'Efectivo')

        try:
            # Limpieza del valor ingresado
            valor_ingresado = int(monto_str.replace('$', '').replace('.', '').replace(',', '').strip())
            
            # VALIDACIÓN: No permitir abonos de 0 o negativos
            if valor_ingresado <= 0:
                messages.error(request, "El monto debe ser mayor a 0.")
                return redirect('ventas:crear_abono', pedido_id=pedido_id)

            # VALIDACIÓN: No permitir pagar más de lo que se debe
            if valor_ingresado > saldo_pendiente:
                messages.error(request, f"El monto (${valor_ingresado}) supera el saldo pendiente (${saldo_pendiente}).")
                return redirect('ventas:crear_abono', pedido_id=pedido_id)

            with transaction.atomic():
                # Verificamos si es el primer abono para descontar inventario
                tiene_abonos = Abono.objects.filter(id_pedido_fk_abono=pedido).exists()
                if not tiene_abonos:
                    # Solo restamos del inventario la primera vez que pone dinero
                    gestionar_inventario(pedido, 'RESTAR')

                # REGISTRAMOS EL ABONO EXACTO
                Abono.objects.create(
                    id_pedido_fk_abono=pedido,
                    monto_abono=valor_ingresado,
                    metodo_pago=metodo,
                    descripcion=request.POST.get('descripcion', 'Abono parcial')
                )
                
                # Calculamos cuánto lleva pagado en total sumando el nuevo abono
                total_pagado_ahora = total_abonado_previo + valor_ingresado

                # CAMBIO DE ESTADO: Solo si llegó al total exacto
                if total_pagado_ahora >= total_productos:
                    # Cambiamos a 'Confirmado' o 'PAGADO' (según uses en tus filtros)
                    pedido.estado_ped = 'Confirmado' 
                    pedido.save()
                    messages.success(request, "¡Felicidades! Has completado el pago de tu pedido.")
                else:
                    messages.success(request, f"Abono de ${valor_ingresado} registrado con éxito.")

            return redirect('ventas:ver_carrito')
            
        except ValueError:
            messages.error(request, "Por favor, ingresa un número válido.")
            return redirect('ventas:crear_abono', pedido_id=pedido_id)

    return render(request, 'ventas/abono/form_abono.html', {
        'pedido': pedido,
        'total_productos': total_productos,
        'total_abonado': total_abonado_previo, 
        'saldo_pendiente': saldo_pendiente
    })

def eliminar_abono(request, id):
    abono = get_object_or_404(Abono, id_abono=id) 
    if request.method == 'POST': 
        abono.delete()
        return redirect('lista_abono')
    return render(request, 'ventas/abono/eliminar_abono.html', {'abono': abono})


#---------------- CRUD DETALLE VALOR -------------------

def lista_det_val(request): 
    detalles = Det_valor.objects.all()
    return render(request, 'ventas/detVal/lista_detVal.html', {'detalles': detalles})

#--------------------- CRUD PEDIDO -----------------

def lista_pedido(request): 
    pedidos = Pedido.objects.all()
    return render(request, 'ventas/pedido/lista_pedido.html', {'pedidos': pedidos})

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
        tipo_pago = request.POST.get('tipo_pago')

        if tipo_pago == 'abono':
            return redirect ('ventas:crear_abono', pedido_id=pedido.id_pedido)
        # Traemos todos los detalles (prendas) que el cliente metió en este pedido
        detalles = Det_valor.objects.filter(id_ped_fk_detval=pedido)
        
        if not detalles.exists():
            messages.error(request, "Tu carrito está vacío.")
            return redirect('ventas:lista_product')

        # SUMAR TOTAL Y DÍAS DE PRODUCCIÓN
        # Usamos aggregate para que la base de datos haga el trabajo pesado
        resultados = detalles.aggregate(
            total=Sum('valor_total'),
            max_espera=Max('id_prod_fk_detval__dias_produccion')
        )
        
        total_real = resultados['total'] or 0
        dias_produccion = resultados['max_espera'] or 1
        
        try: 
            with transaction.atomic(): 
                alerta_stock = gestionar_inventario(pedido, operacion='RESTAR')
        # Actualizamos datos de pedido
                pedido.subtotal_ped = total_real
                pedido.valor_ped = total_real
                pedido.metodo_pago = request.POST.get('metodo_pago')
                pedido.fecha_ped = timezone.now().date() # Fecha de hoy
                pedido.fecha_entrega = timezone.now().date() + timedelta(days=dias_produccion)
        
        #cambio estado
                pedido.estado_ped = 'Confirmado' 
                pedido.save()

                Abono.objects.create(
                    id_pedido_fk_abono=pedido,
                    monto_abono=total_real, # El 100%
                    metodo_pago=request.POST.get('metodo_pago'),
                    descripcion="Pago Exitoso."
                )

                if alerta_stock: 
                    print(f"El pedido {pedido.id_pedido} requiere compra de {alerta_stock} ")

                messages.success(request, f"¡Pedido confirmado! Estará listo el {pedido.fecha_entrega}")
                return redirect('ventas:lista_product')
            
        except Exception as e: 
            messages.error(request, f"Error al procesar el pago: {e}")
            return redirect('ventas:ver_carrito')

    return render(request, 'ventas/pedido/finalizar.html', {'pedido': pedido})

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
        
    return render(request, 'ventas/pedido/editar_pedido.html', {'pedido': pedido})

@login_requerido_custom
def eliminar_pedido(request, id):
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('login')
    pedido = get_object_or_404(Pedido, id_pedido=id)
    
    if request.method == 'POST':
        if pedido.estado_ped == 'Cancelado': 
            messages.warning(request, "Pedido ya cancelado")
            return redirect('ventas:lista_pedido')
        try: 
            with transaction.atomic():
            # Si el pedido ya tenía abonos, significa que el inventario se descontó
                realizo_pago = Abono.objects.filter(id_pedido_fk_abono=pedido).exists()
                if realizo_pago:    
                    gestionar_inventario(pedido, 'SUMAR') # Devolvemos el material
            
            pedido.estado_ped = 'Cancelado'
            pedido.save()
            return redirect('ventas:lista_pedido')
        except Exception as e:
            messages.success(request, f"Error al cancelar el pedido: {e}")
            return redirect('ventas:lista_pedido')
            
    return render(request, 'ventas/pedido/eliminar_pedido.html', {'pedido': pedido})

#------------------------ CARRITO --------------------------

@login_requerido_custom
def ver_carrito(request):
    
    try:
        cliente = obtener_cliente_actual(request)
    except Cliente.DoesNotExist:

        return render(request, 'ventas/pedido/carrito.html', {
            'items': [], 
            'total_productos': 0, 
            'error_perfil': "No tienes un perfil de Cliente asociado a tu usuario."
        })

    pedido = Pedido.objects.filter(id_clien_fk=cliente, estado_ped='Carrito').first()

    if not pedido:
        return render(request, 'ventas/pedido/carrito.html', {'items': [], 'total_productos': 0})
    
    decimal = Decimal('0.000')

    items = Det_valor.objects.filter(id_ped_fk_detval=pedido)
    total_products = items.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    total_productos = Decimal(total_products).quantize(decimal)

    total_abono = Abono.objects.filter(id_pedido_fk_abono=pedido).aggregate(Sum('monto_abono'))['monto_abono__sum'] or 0
    total_abonado = Decimal(total_abono).quantize(decimal)
    saldo_pendiente = max(0, total_productos - total_abonado).quantize(decimal)

    if saldo_pendiente <= 0 and pedido.estado_ped in ['PAGADO', 'Confirmado', 'Confirmada']:
        return render(request, 'ventas/pedido/carrito.html', {'items': [], 'total_productos': 0})

    return render(request, 'ventas/pedido/carrito.html', {
        'pedido': pedido,
        'items': items,
        'total_productos': total_productos,
        'saldo_pendiente': saldo_pendiente,
        'tiene_abonos': total_abonado > 0
    })

@login_requerido_custom
def eliminar_del_carrito(request, id_det_valor):
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('login')
    
    detalle = get_object_or_404(Det_valor, id_det_valor=id_det_valor)
    
    if detalle.id_ped_fk_detval.estado_ped != 'Carrito':
        messages.error(request, "No puedes eliminar productos de un pedido ya confirmado.")
        return redirect('ventas:lista_pedido')

    with transaction.atomic():
        
        if detalle.id_var_fk_detval:
            detalle.id_var_fk_detval.delete()
        
        detalle.delete()
        
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('ventas:ver_carrito')

@login_requerido_custom
def editar_carrito(request, id_det_valor):
    # 1. Obtenemos el detalle que se quiere "cambiar"
    detalle = get_object_or_404(Det_valor, id_det_valor=id_det_valor)
    
    # 2. Guardamos los datos necesarios antes de borrar
    id_producto = detalle.id_prod_fk_detval.id_produc
    id_pedido = detalle.id_ped_fk_detval.id_pedido
    es_personalizado = (detalle.tipo_pedido == "Personalizado")

    # 3. Borramos el registro actual del carrito
    with transaction.atomic():
        if detalle.id_var_fk_detval:
            detalle.id_var_fk_detval.delete() # Borra la variación si existe
        detalle.delete() # Borra el renglón del carrito

    # 4. Redirección inteligente según el tipo de producto
    if es_personalizado:
        # Te manda al formulario de personalización (talla, estampado, etc.)
        return redirect('ventas:crear_variacion', producto_id=id_producto, pedido_id=id_pedido)
    else:
        # Te manda a la vista simple (solo talla)
        return redirect('ventas:producto_sin_personalizar', producto_id=id_producto)

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
    return render(request, 'ventas/admin/registrar_producto.html',{
        'producto': producto,
        'materiales': materiales
    })

def gestionar_inventario(pedido, operacion):
    detalles = Det_valor.objects.filter(id_ped_fk_detval=pedido)
    materiales_faltantes = [] # Lista para guardar los materiales faltantes

    with transaction.atomic():
        for item in detalles:
            receta = Det_mov_matp.objects.filter(producto=item.id_prod_fk_detval)
            
            for insumo in receta:
                material = insumo.materia_prima
                cantidad_total = insumo.cantidad_usada * item.cant

                if operacion == 'RESTAR':
                    # Restamos de todos modos
                    material.stock_movi_mtp -= cantidad_total
                    
                    # Si el stock bajó de cero, lo anotamos en la lista de faltantes
                    if material.stock_movi_mtp < 0:
                        materiales_faltantes.append(f"{material.tipo_movi_mtp} (Faltan {abs(material.stock_movi_mtp)} unidades)")
                
                elif operacion == 'SUMAR':
                    material.stock_movi_mtp += cantidad_total
                
                material.save()
    
    return materiales_faltantes