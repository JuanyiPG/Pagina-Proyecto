import re
import os
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.db import transaction
import hashlib
from django.db.models import Sum, Max
from datetime import timedelta
from usuarios.views import solo_personal, login_requerido_custom

from django.shortcuts import get_object_or_404, redirect, render
from .models import Abono,Pedido, Variacion, Det_valor, Producto, Det_mov_matp,Cliente
from inventario.models import Estampado, Movimiento_matp
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

#---------------------- COMPROBAR LOGIN ------------------------------

def obtener_cliente_actual(request):
    id_user = request.session.get('usuario_id')
    if not id_user:
        return None
    try:
        return Cliente.objects.get(id_usuario_fk=id_user)
    except Cliente.DoesNotExist:
        return None

#-------------------- CRUD VARIACION --------------------------

def lista_var(request):
    # 1. Traemos los detalles excluyendo los cancelados con sus relaciones
    detalles_db = Det_valor.objects.exclude(
        id_ped_fk_detval__estado_ped='Cancelado'
    ).select_related(
        'id_ped_fk_detval', 
        'id_prod_fk_detval', 
        'id_var_fk_detval', 
        'id_ped_fk_detval__id_clien_fk'
    )

    pedidos_agrupados = {}

    for d in detalles_db:
        if d.id_ped_fk_detval:
            id_ped = d.id_ped_fk_detval.id_pedido
            
            if id_ped not in pedidos_agrupados:
                pedido_obj = d.id_ped_fk_detval
                pedido_obj.prendas_agrupadas = []
                
                # Formateamos la fecha del pedido de forma segura
                if pedido_obj.fecha_ped:
                    pedido_obj.fecha_formateada = pedido_obj.fecha_ped.strftime("%d/%m/%Y")
                else:
                    pedido_obj.fecha_formateada = "Sin Fecha"
                
                # EXTRAEMOS Y FORMATEAMOS LOS ABONOS AQUÍ EN PYTHON
                pedido_obj.abonos_listos = []
                if hasattr(pedido_obj, 'abono_set'):
                    for abono in pedido_obj.abono_set.all():
                        # Intentamos usar formato con hora, si falla porque es solo fecha, usamos formato simple
                        try:
                            fecha_txt = abono.fecha_abono.strftime("%d/%m/%Y %H:%M")
                        except AttributeError:
                            fecha_txt = abono.fecha_abono.strftime("%d/%m/%Y")
                            
                        pedido_obj.abonos_listos.append({
                            'fecha': fecha_txt,
                            'monto': abono.monto_abono,
                            'metodo_pago': abono.metodo_pago
                        })
                
                pedidos_agrupados[id_ped] = pedido_obj
                
            pedidos_agrupados[id_ped].prendas_agrupadas.append(d)
        else:
            # Control para datos huérfanos de prueba
            id_temporal = "Prueba-Suelto"
            if id_temporal not in pedidos_agrupados:
                class PedidoSimulado:
                    pass
                p_sim = PedidoSimulado()
                p_sim.id_pedido = "Sin ID"
                p_sim.id_clien_fk = None
                p_sim.valor_ped = d.valor_total
                p_sim.estado_ped = "Prueba"
                p_sim.metodo_pago = "Manual"
                p_sim.fecha_formateada = timezone.now().strftime("%d/%m/%Y")
                p_sim.prendas_agrupadas = []
                p_sim.abonos_listos = [] # Lista vacía para que no rompa el bucle
                pedidos_agrupados[id_temporal] = p_sim
                
            pedidos_agrupados[id_temporal].prendas_agrupadas.append(d)

    # 2. Ordenamos los pedidos colocando los reales numéricos primero
    pedidos_reales = [p for p in pedidos_agrupados.values() if isinstance(p.id_pedido, int)]
    pedidos_reales.sort(key=lambda x: x.id_pedido, reverse=True)
    
    pedidos_manuales = [p for p in pedidos_agrupados.values() if not isinstance(p.id_pedido, int)]
    lista_final = pedidos_reales + pedidos_manuales

    return render(request, 'ventas/pedido/lista_pedidos.html', {
        'pedidos': lista_final,
    })

def eliminar_pedido(request, id_pedido):
    # Buscamos el pedido en la base de datos (dispara 404 si ya no existe)
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    
    try:
        # 1. Eliminamos los detalles asociados primero
        Det_valor.objects.filter(id_ped_fk_detval=pedido).delete()
        
        # 2. Borramos el pedido principal
        pedido.delete()
        
        messages.success(request, f"El pedido #{id_pedido} y todo su historial se borraron correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar el pedido: {str(e)}")
        
    # CORRECCIÓN: Redirección limpia usando el name exacto de tu urls.py
    return redirect('ventas:lista_pedido')

def lista_var_e(request):
    detalles = Det_valor.objects.exclude(
        id_ped_fk_detval__estado_ped='Cancelado'
    ).select_related('id_ped_fk_detval', 'id_prod_fk_detval', 'id_var_fk_detval')
    
    return render(request, 'ventas/pedido/lista_pedidos_e.html', {
        'detalles': detalles,
    })

@login_requerido_custom
def crear_variacion(request, producto_id, pedido_id): 
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('ventas:lista_product')

    producto = get_object_or_404(Producto, id_produc=producto_id)
    estampados = Estampado.objects.all()
    
    if request.method == 'POST': 
        estampado_elegido = request.POST.get('id_estam')
        estam_obj = get_object_or_404(Estampado, id_estam=estampado_elegido)
        
        with transaction.atomic():
            variacion = Variacion.objects.create(
                talla_var=request.POST.get('talla_var'),
                cant_soli=int(request.POST.get('cant_soli')),
                color_var=request.POST.get('color_var'),
                mat_var=request.POST.get('mat_var'),
                costo_var=estam_obj.costo_adi,
                id_estam_fk_var=estam_obj
            )

            pedido_actual = get_object_or_404(Pedido, id_pedido=pedido_id)
            
            Det_valor.objects.create(
                valor_total=(producto.precio + variacion.costo_var) * variacion.cant_soli, 
                cant=variacion.cant_soli,
                tipo_pedido="Personalizado", 
                id_ped_fk_detval=pedido_actual, 
                id_var_fk_detval=variacion, 
                id_prod_fk_detval=producto
            )

        return redirect('ventas:ver_carrito')

    return render(request, 'personalizar.html', {
        'producto': producto,
        'estampados': estampados
    })

@login_requerido_custom
def editar_variacion(request, detalle_id): 
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('login')
    
    detalle = get_object_or_404(Det_valor, id_det_valor=detalle_id)
    variacion = detalle.id_var_fk_detval
    producto = detalle.id_prod_fk_detval

    estampado = Estampado.objects.all()

    if request.method == 'POST': 
        id_estam_nuevo = request.POST.get('id_estam')
        estampado_obj = get_object_or_404(Estampado, id_estam=id_estam_nuevo)

        variacion.talla_var = request.POST.get('talla_var')
        variacion.cant_soli = int(request.POST.get('cant_soli', 1))
        variacion.color_var = request.POST.get('color_var')
        variacion.mat_var = request.POST.get('mat_var')
        variacion.costo_var = estampado_obj.costo_adi
        variacion.save()

        # Actualizar el detalle del valor
        detalle.cant = variacion.cant_soli
        detalle.valor_total = (producto.precio + variacion.costo_var) * variacion.cant_soli
        detalle.save()  

        return redirect('ventas:ver_carrito')
        
    return render(request, 'personalizar.html', {
        'producto': producto,
        'estampados': estampado,
        'variacion': variacion, 
        'es_edicion': True      
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
    todos = Producto.objects.prefetch_related('det_mov_matp_set__materia_prima').all()
    productos_visibles = []

    for p in todos:
        es_valido = True
        detalles = p.det_mov_matp_set.all()
        
        if not detalles.exists():
            es_valido = False
        else:
            for d in detalles:
                h = d.materia_prima.history.all()
                # Calculamos stock rápido
                stock = sum(x.stock_mmtp if x.tipo_mmtp == 'ENTRADA' else -x.stock_mmtp for x in h)
                if stock < d.cantidad_usada :
                    es_valido = False
                elif stock == 0: 
                    es_valido = False
                    break
        
        if es_valido:
            productos_visibles.append(p)

    return render(request, 'PAGINAS_LUXY_PROD/PAGINA_PROD.html', {'productos': productos_visibles})
    

@solo_personal
def lista_producto_admin(request): 
    nuevo_hash = None
    materiales_db = Movimiento_matp.objects.all()
    productos = Producto.objects.all()

    if request.method == 'POST': 
        #POST para textos plano, FILES, para img, pdf, etc
        imagen_produc = request.FILES.get('imagen_produc')
        nom_produc = request.POST.get('nom_produc')
        gen_produc = request.POST.get('gen_produc')
        desc_produc = request.POST.get('desc_produc')
        categoria_produc = request.POST.get('cat_produc')
        estado_produc = request.POST.get('estado_produc')
        precio = request.POST.get('precio')
        dias_produccion = request.POST.get('dias_produccion')

        #Converir String a Decimal
        try: 
            precio_limpio = re.sub(r'[^\d]', '', precio)
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
                return render(request, 'ventas/producto/lista_product.html',{
                    'error': 'ERROR: Esta prenda ya ha sido subida anteriormente.'
            })
        
        nuevo_p = Producto.objects.create(imagen_product=imagen_produc, imagen_hash=nuevo_hash, nom_produc=nom_produc, gen_produc=gen_produc,
                                desc_produc=desc_produc, categoria_produc=categoria_produc,estado_produc=estado_produc, precio=valor, dias_produccion=dias_produccion )
        
        ids_materiales = request.POST.getlist('material_ids[]')
        cantidades = request.POST.getlist('cantidades[]')

        for id_mat, cant in zip(ids_materiales, cantidades):
            if id_mat and cant:
                Det_mov_matp.objects.create(
                    producto = nuevo_p, # Aquí usamos el objeto que acabamos de guardar
                    materia_prima_id = id_mat, 
                    cantidad_usada = cant
                )

        return redirect('ventas:lista_producto_admin')
    return render(request, 'ventas/producto/lista_product.html',{
        'materiales': materiales_db,
        'productos': productos
    })

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
        producto.gen_produc = request.POST.get('gen_produc')
        producto.desc_produc = request.POST['desc_produc']
        producto.categoria_produc = request.POST.get('categoria_produc')

        dias = request.POST.get('dias_produccion')

        if not dias or dias.strip() == "":
            producto.dias_produccion = 10
        else:
            producto.dias_produccion = int(dias)

        producto.save()
        
        producto.estado_produc = request.POST['estado_produc']
        precio = request.POST['precio']
        try: 
            precio_limpio = re.sub(r'[^\d]', '', precio)
            valor = Decimal(precio_limpio)
        except(InvalidOperation, TypeError):
            valor = Decimal('0.00')

        producto.precio = valor
        producto.save()
        return redirect('ventas:lista_producto_admin')
    return render(request, 'ventas/producto/editar_producto.html', {'producto': producto})

@solo_personal
def eliminar_producto(request, product_id): 
    producto = get_object_or_404(Producto, id_produc=product_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ventas:lista_producto_admin')
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
        except (ValueError, TypeError):
            cantidad = 1

        with transaction.atomic():
            # 1. Obtener o crear el carrito
            pedido, creado = Pedido.objects.get_or_create(
                id_clien_fk=cliente,
                estado_ped='Carrito', 
                defaults={
                    'subtotal_ped': 0, 
                    'valor_ped': 0, 
                    'metodo_pago': 'Pendiente'
                }
            )

            # 2. Crear la variación 
            variacion = Variacion.objects.create(
                talla_var = talla, 
                cant_soli = cantidad, 
                color_var = color,
                mat_var = "Algodón", # Agregué un valor por defecto si es obligatorio
                costo_var = producto.precio, 
                id_estam_fk_var = None 
            )

            # 3. Crear el detalle 
            Det_valor.objects.create(
                id_ped_fk_detval=pedido, 
                id_prod_fk_detval=producto,
                id_var_fk_detval=variacion,
                valor_total=int(producto.precio * cantidad),
                tipo_pedido='Estandar'
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
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
    
    # Totales actuales
    items = Det_valor.objects.filter(id_ped_fk_detval=pedido)
    total_productos = items.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    total_abonado_previo = Abono.objects.filter(id_pedido_fk_abono=pedido).aggregate(Sum('monto_abono'))['monto_abono__sum'] or 0
    saldo_pendiente = total_productos - total_abonado_previo

    if request.method == 'POST':
        monto_raw = request.POST.get('monto_abono', '0')
        metodo = request.POST.get('metodo_pago', 'Efectivo')

        valor_limpio = re.sub(r'[^\d]', '', str(monto_raw))
        
        try:
            valor_ingresado = Decimal(valor_limpio) if valor_limpio else Decimal('0')
            
            if valor_ingresado <= 0:
                messages.error(request, "El monto debe ser mayor a 0.")
                return redirect('ventas:crear_abono', pedido_id=pedido_id)

            if valor_ingresado > saldo_pendiente:
                messages.error(request, f"El monto (${valor_ingresado}) supera el saldo (${saldo_pendiente}).")
                return redirect('ventas:crear_abono', pedido_id=pedido_id)

            with transaction.atomic():
                tiene_abonos = Abono.objects.filter(id_pedido_fk_abono=pedido).exists()
                if not tiene_abonos:
                    gestionar_inventario(pedido, 'RESTAR')

                Abono.objects.create(
                    id_pedido_fk_abono=pedido,
                    monto_abono=valor_ingresado,
                    metodo_pago=metodo,
                    descripcion=request.POST.get('descripcion', 'Abono parcial')
                )
                
                total_pagado_ahora = total_abonado_previo + valor_ingresado
                if total_pagado_ahora >= total_productos:
                    pedido.estado_ped = 'Confirmado' 
                    pedido.save()
                    messages.success(request, "¡Pago completado con éxito!")
                else:
                    messages.success(request, f"Abono de ${valor_ingresado} registrado.")

            return redirect('ventas:ver_carrito')

        except (InvalidOperation, ValueError) as e:
            messages.error(request, f"Error en el formato del número: {e}")
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


@login_requerido_custom
def finalizar_pedido(request, pedido_id):
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('login')
    
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
def lista_pedidos_client(request):
    cliente = obtener_cliente_actual(request)
    if not cliente:
        return redirect('login')
    
    pedidos_queryset = Pedido.objects.filter(
        id_clien_fk=cliente
    ).exclude(estado_ped__in=['Entregado', 'Cancelado']).order_by('-id_pedido')

    formato = Decimal('0.00')
    pedidos_con_detalles = []

    for pedido in pedidos_queryset:
        items = Det_valor.objects.filter(id_ped_fk_detval=pedido).select_related('id_prod_fk_detval')
        primer_item = items.first()
        
        total_raw = items.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        total_pedido = Decimal(str(total_raw)).quantize(formato)

        abono_raw = Abono.objects.filter(id_pedido_fk_abono=pedido).aggregate(Sum('monto_abono'))['monto_abono__sum'] or 0
        total_abonado = Decimal(str(abono_raw)).quantize(formato)
        
        saldo_pendiente = (total_pedido - total_abonado).quantize(formato)

        
        bloqueado = saldo_pendiente > 0

        pedidos_con_detalles.append({
            'objeto': pedido,
            'foto': primer_item.id_prod_fk_detval.imagen_product.url if primer_item and primer_item.id_prod_fk_detval.imagen_product else None,
            'total': total_pedido,
            'abonado': total_abonado,
            'saldo': max(0, saldo_pendiente),
            'bloqueado': bloqueado 
        })

    return render(request, 'ventas/pedido/lista_ped_cliente.html', {
        'pedidos_detallados': pedidos_con_detalles
    })



@login_requerido_custom
def editar_pedido(request, id): 
    cliente = obtener_cliente_actual(request)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('login')
    pedido = get_object_or_404(Pedido, id_pedido=id)

    if request.method == 'POST':
        pedido.fecha_ped = request.POST.get('fecha_ped')
        pedido.subtotal_ped = request.POST.get('subtotal_ped')
        pedido.valor_ped = request.POST.get('valor_ped')
        pedido.estado_ped = request.POST.get('estado_ped')
        pedido.metodo_pago = request.POST.get('metodo_pago')
        pedido.fecha_entrega = request.POST.get('fecha_entrega')
        pedido.save()
        return redirect('ventas:lista_pedido') 
        
    return render(request, 'ventas/pedido/editar_pedido.html', {'pedido': pedido})

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages

@login_requerido_custom
def gestionar_pedido(request, id_pedido):
    """Vista procesadora de acciones mediante POST"""
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    accion = request.POST.get('accion')

    try:
        if accion == 'cancelar':
            with transaction.atomic():
                realizo_pago = Abono.objects.filter(id_pedido_fk_abono=pedido).exists()
                if realizo_pago:    
                    gestionar_inventario(pedido, 'SUMAR')
                pedido.estado_ped = 'Cancelado'
                pedido.save()
                messages.success(request, "Pedido cancelado correctamente.")
        
        elif accion == 'entregado':
            pedido.delete() 
            messages.success(request, "¡Gracias por confirmar la entrega!")

    except Exception as e:
        messages.error(request, f"Error: {e}")

    return redirect('ventas:lista_pedidos_cliente')

#------------------------ CARRITO --------------------------

@login_requerido_custom
def ver_carrito(request): 
    try:
        cliente = obtener_cliente_actual(request)
    except Cliente.DoesNotExist:
        return render(request, 'ventas/pedido/carrito.html', {'pedidos_info': []})

    # 1. TRAEMOS TODOS LOS PEDIDOS (Quitamos el .first())
    pedidos = Pedido.objects.filter(
        id_clien_fk=cliente
    ).exclude(estado_ped__in=['Entregado', 'Cancelado', 'Completado']).order_by('-id_pedido')

    if not pedidos.exists():
        return render(request, 'ventas/pedido/carrito.html', {'pedidos_info': []})

    # 2. PROCESAMOS CADA PEDIDO PARA SACAR SUS TOTALES
    pedidos_info = [] 
    formato = Decimal('0.00')

    for pedido in pedidos:
        items = Det_valor.objects.filter(id_ped_fk_detval=pedido).select_related('id_var_fk_detval', 'id_prod_fk_detval')

        total_product = 0
        for item in items:
            if item.id_var_fk_detval:
                total_product += item.id_var_fk_detval.cant_soli
        total_raw = items.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        total_productos = Decimal(str(total_raw)).quantize(formato)

        abono_raw = Abono.objects.filter(id_pedido_fk_abono=pedido).aggregate(Sum('monto_abono'))['monto_abono__sum'] or 0
        total_abonado = Decimal(str(abono_raw)).quantize(formato)
        
        saldo_pendiente = (total_productos - total_abonado).quantize(formato)

        # Solo lo agregamos si no está pagado totalmente o si es el carrito actual
        if saldo_pendiente > 0 or pedido.estado_ped == 'Carrito':
            pedidos_info.append({
                'pedido': pedido,
                'items': items,
                'total_product' : total_product,
                'total_productos': total_productos,
                'total_abonado': total_abonado,
                'saldo_pendiente': max(0, saldo_pendiente),
            })

    return render(request, 'ventas/pedido/carrito.html', {
        'pedidos_info': pedidos_info
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
        return redirect('ventas:ver_carrito')

    with transaction.atomic():
        if detalle.id_personalizacion_3d:
            pedido_3d = detalle.id_personalizacion_3d
            
            for img in [pedido_3d.foto_frente, pedido_3d.foto_espalda, pedido_3d.foto_lateral]:
                if img and os.path.exists(img.path):
                    os.remove(img.path)
            
            pedido_3d.delete()
        
        if detalle.id_var_fk_detval:
            detalle.id_var_fk_detval.delete()
        
        detalle.delete()
        
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('ventas:ver_carrito')

@login_requerido_custom
def editar_carrito(request, id_det_valor):
    detalle = get_object_or_404(Det_valor, id_det_valor=id_det_valor)
    
    id_producto = detalle.id_prod_fk_detval.id_produc
    id_pedido = detalle.id_ped_fk_detval.id_pedido
    es_personalizado = (detalle.tipo_pedido == "Personalizado")

    with transaction.atomic():
        if detalle.id_var_fk_detval:
            detalle.id_var_fk_detval.delete()
        detalle.delete()

    if es_personalizado:
        return redirect('ventas:crear_variacion', producto_id=id_producto, pedido_id=id_pedido)
    else:
        return redirect('ventas:producto_sin_personalizar', producto_id=id_producto)

#------------- DET_MOV_MATP ---------------------------------

def gestionar_inventario(pedido, operacion):
    # Traemos los productos del pedido y sus variaciones (cantidades)
    detalles_pedido = Det_valor.objects.filter(id_ped_fk_detval=pedido).select_related('id_var_fk_detval', 'id_prod_fk_detval')
    
    with transaction.atomic():
        for item in detalles_pedido:

            cantidad_prendas = item.id_var_fk_detval.cant_soli if item.id_var_fk_detval else 0
            
            if cantidad_prendas <= 0:
                continue

            receta = Det_mov_matp.objects.filter(producto=item.id_prod_fk_detval)

            for insumo in receta:
                try:
                    material_stock = Movimiento_matp.objects.filter(
                        mat_mmtp=insumo.materia_prima.mat_mmtp,
                        color_mmtp=insumo.materia_prima.color_mmtp
                    ).latest('id_mmtp')

                    cantidad_a_mover = insumo.cantidad_usada * cantidad_prendas

                    if operacion == 'RESTAR':
                        material_stock.stock_mmtp -= cantidad_a_mover
                    elif operacion == 'SUMAR':
                        material_stock.stock_mmtp += cantidad_a_mover
                    
                    material_stock.save()
                except Movimiento_matp.DoesNotExist:
                    continue


#---------------------- listas empleados --------------------------------------------------------




def lista_producto_e(request):
    productos = Producto.objects.all()
    return render(request, 'ventas/producto/lista_producto_e.html', {'productos': productos})


from .models import (
    Pedido,
    Variacion,
    Det_valor,
    Producto,
    Abono
)

@csrf_exempt
def venta_empleado(request):

    if request.method == 'POST':

        try:
            data = json.loads(request.body)

            productos = data.get('productos', [])
            metodo_pago = data.get('metodo_pago', 'Efectivo')

            if not productos:
                return JsonResponse({
                    'success': False,
                    'message': 'No hay productos'
                })

            # =========================
            # CREAR PEDIDO
            # =========================

            pedido = Pedido.objects.create(
                subtotal_ped = 0,
                valor_ped = 0,
                estado_ped = 'Confirmado',
                metodo_pago = metodo_pago,
                id_clien_fk = None
            )

            total = Decimal('0')

            # =========================
            # RECORRER PRODUCTOS
            # =========================

            for item in productos:

                producto = Producto.objects.get(
                    id_produc = item['id']
                )

                cantidad = int(item['cantidad'])

                talla = item['talla']

                color = item['color']

                subtotal = Decimal(str(producto.precio)) * cantidad

                # =========================
                # VARIACION
                # =========================

                variacion = Variacion.objects.create(
                    talla_var = talla,
                    cant_soli = cantidad,
                    color_var = color,
                    mat_var = "Venta Empleado",
                    costo_var = subtotal
                )

                # =========================
                # DETALLE
                # =========================

                Det_valor.objects.create(
                    valor_total = subtotal,
                    tipo_pedido = "Venta Empleado",
                    id_ped_fk_detval = pedido,
                    id_var_fk_detval = variacion,
                    id_prod_fk_detval = producto
                )

                total += subtotal

            # =========================
            # ACTUALIZAR PEDIDO
            # =========================

            pedido.subtotal_ped = total
            pedido.valor_ped = total
            pedido.save()

            # =========================
            # ABONO
            # =========================

            Abono.objects.create(
                monto_abono = total,
                metodo_pago = metodo_pago,
                descripcion = "Venta de Empleado",
                id_pedido_fk_abono = pedido
            )

            # =========================
            # DESCONTAR INVENTARIO
            # =========================

            gestionar_inventario(
                pedido,
                'RESTAR'
            )

            return JsonResponse({
                'success': True,
                'message': 'Pago realizado correctamente'
            })

        except Exception as e:

            return JsonResponse({
                'success': False,
                'message': str(e)
            })

    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    })