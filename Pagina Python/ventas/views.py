import os
import json
import hashlib
import re
import smtplib  
from decimal import Decimal, InvalidOperation
from datetime import timedelta

from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Max, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.apps import apps
from email.policy import default
from usuarios.views import solo_personal, login_requerido_custom
from .models import Abono, Pedido, Variacion, Det_valor, Producto, Det_mov_matp, Cliente
from inventario.models import Estampado, Movimiento_matp, PedidoPersonalizado
from inventario.services import calcular_precio_personalizacion

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
            pedido_obj = d.id_ped_fk_detval
            id_ped = pedido_obj.id_pedido
            
            if id_ped not in pedidos_agrupados:
                pedido_obj.prendas_agrupadas = []
                
                # 🌟 ASEGURAR QUE EL VALOR NO SEA 0
                if not pedido_obj.valor_ped or pedido_obj.valor_ped == 0:
                    pedido_obj.valor_ped = d.valor_total
                
                # 🌟 ASEGURAR QUE EL MÉTODO DE PAGO NO VENGA VACÍO
                if not pedido_obj.metodo_pago:
                    pedido_obj.metodo_pago = "Abonos / Crédito"
                
                # CONTROL DE EN BLANCO PARA NOMBRES
                if not pedido_obj.id_clien_fk:
                    if d.tipo_pedido and "Venta Empleado:" in str(d.tipo_pedido):
                        pedido_obj.vendedor_nombre = d.tipo_pedido.replace("Venta Empleado:", "").strip()
                    else:
                        pedido_obj.vendedor_nombre = "Venta por Abonos"
                else:
                    try:
                        cliente = pedido_obj.id_clien_fk
                        if hasattr(cliente, 'nom_clien') and cliente.nom_clien:
                            pedido_obj.vendedor_nombre = f"{cliente.nom_clien} {getattr(cliente, 'ape_clien', '')}".strip()
                        else:
                            pedido_obj.vendedor_nombre = cliente.id_usuario_fk.username
                    except AttributeError:
                        pedido_obj.vendedor_nombre = "Cliente Registrado"

                # Formateo seguro de la fecha del pedido
                if pedido_obj.fecha_ped:
                    pedido_obj.fecha_formateada = pedido_obj.fecha_ped.strftime("%d/%m/%Y")
                else:
                    pedido_obj.fecha_formateada = "Sin Fecha"
                
                # Carga del historial de abonos relacionados y cálculo de total abonado
                pedido_obj.abonos_listos = []
                total_abonado = Decimal('0')  # 🌟 Variable para sumar los abonos
                
                if hasattr(pedido_obj, 'abono_set'):
                    for abono in pedido_obj.abono_set.all():
                        try:
                            fecha_txt = abono.fecha_abono.strftime("%d/%m/%Y %H:%M")
                        except AttributeError:
                            fecha_txt = abono.fecha_abono.strftime("%d/%m/%Y") if abono.fecha_abono else "Sin fecha"
                            
                        pedido_obj.abonos_listos.append({
                            'fecha': fecha_txt,
                            'monto': abono.monto_abono,
                            'metodo_pago': abono.metodo_pago if abono.metodo_pago else "Efectivo"
                        })
                        
                        # Acumulamos el monto del abono actual
                        if abono.monto_abono:
                            total_abonado += Decimal(str(abono.monto_abono))
                
                # 🌟 LÓGICA DE ESTADO AUTOMÁTICO PARA ABONOS
                if "Abono" in pedido_obj.metodo_pago or "Crédito" in pedido_obj.metodo_pago:
                    if total_abonado < Decimal(str(pedido_obj.valor_ped)):
                        pedido_obj.estado_ped = "Pendiente"
                    else:
                        pedido_obj.estado_ped = "Entregado"

                pedidos_agrupados[id_ped] = pedido_obj
            else:
                if pedidos_agrupados[id_ped].valor_ped == 0:
                    pedidos_agrupados[id_ped].valor_ped += d.valor_total
                
            pedidos_agrupados[id_ped].prendas_agrupadas.append(d)
        else:
            id_temporal = "Prueba-Suelto"
            if id_temporal not in pedidos_agrupados:
                class PedidoSimulado: pass
                p_sim = PedidoSimulado()
                p_sim.id_pedido = "Sin ID"
                p_sim.id_clien_fk = None
                p_sim.vendedor_nombre = "Prueba Técnica"
                p_sim.valor_ped = d.valor_total
                p_sim.estado_ped = "Prueba"
                p_sim.metodo_pago = "Manual"
                p_sim.fecha_formateada = timezone.now().strftime("%d/%m/%Y")
                p_sim.prendas_agrupadas = []
                p_sim.abonos_listos = []
                pedidos_agrupados[id_temporal] = p_sim
                
            pedidos_agrupados[id_temporal].prendas_agrupadas.append(d)

    pedidos_reales = [p for p in pedidos_agrupados.values() if isinstance(p.id_pedido, int)]
    pedidos_reales.sort(key=lambda x: x.id_pedido, reverse=True)
    
    pedidos_manuales = [p for p in pedidos_agrupados.values() if not isinstance(p.id_pedido, int)]
    lista_final = pedidos_reales + pedidos_manuales

    return render(request, 'ventas/pedido/lista_pedidos.html', {
        'pedidos': lista_final,
    })

@solo_personal
def eliminar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    try:
        Det_valor.objects.filter(id_ped_fk_detval=pedido).delete()
        pedido.delete()
        messages.success(request, f"El pedido #{id_pedido} y todo su historial se borraron correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar el pedido: {str(e)}")
        
    return redirect('ventas:lista_pedido')

@solo_personal
def lista_var_e(request):
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
                
                if not pedido_obj.id_clien_fk:
                    if "Venta Empleado:" in d.tipo_pedido:
                        pedido_obj.vendedor_nombre = d.tipo_pedido.replace("Venta Empleado:", "").strip()
                    else:
                        pedido_obj.vendedor_nombre = "Empleado Interno"
                else:
                    pedido_obj.vendedor_nombre = pedido_obj.id_clien_fk.id_usuario_fk.username if hasattr(pedido_obj.id_clien_fk, 'id_usuario_fk') else "Cliente Virtual"

                if pedido_obj.fecha_ped:
                    pedido_obj.fecha_formateada = pedido_obj.fecha_ped.strftime("%d/%m/%Y")
                else:
                    pedido_obj.fecha_formateada = "Sin Fecha"
                
                pedido_obj.abonos_listos = []
                if hasattr(pedido_obj, 'abono_set'):
                    for abono in pedido_obj.abono_set.all():
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
            id_temporal = "Prueba-Suelto"
            if id_temporal not in pedidos_agrupados:
                class PedidoSimulado: pass
                p_sim = PedidoSimulado()
                p_sim.id_pedido = "Sin ID"
                p_sim.id_clien_fk = None
                p_sim.vendedor_nombre = "Prueba Técnica"
                p_sim.valor_ped = d.valor_total
                p_sim.estado_ped = "Prueba"
                p_sim.metodo_pago = "Manual"
                p_sim.fecha_formateada = timezone.now().strftime("%d/%m/%Y")
                p_sim.prendas_agrupadas = []
                p_sim.abonos_listos = []
                pedidos_agrupados[id_temporal] = p_sim
                
            pedidos_agrupados[id_temporal].prendas_agrupadas.append(d)

    pedidos_reales = [p for p in pedidos_agrupados.values() if isinstance(p.id_pedido, int)]
    pedidos_reales.sort(key=lambda x: x.id_pedido, reverse=True)
    
    pedidos_manuales = [p for p in pedidos_agrupados.values() if not isinstance(p.id_pedido, int)]
    lista_final = pedidos_reales + pedidos_manuales

    return render(request, 'ventas/pedido/lista_pedidos_e.html', {
        'pedidos': lista_final,
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
                talla_var=talla,
                cant_soli=cantidad,
                color_var=color,
                mat_var=descripcion_mat,
                costo_var=precio_base_producto
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

def eliminar_variacion(request, detalle_id):
    detalle = get_object_or_404(Det_valor, id_det_valor=detalle_id)
    if detalle.id_var_fk_detval:
        detalle.id_var_fk_detval.delete()
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
                try:
                    ultimo_movimiento = Movimiento_matp.objects.filter(
                        mat_mmtp=d.materia_prima.mat_mmtp,
                        color_mmtp=d.materia_prima.color_mmtp
                    ).latest('id_mmtp')
                    stock_actual = ultimo_movimiento.stock_mmtp
                except Movimiento_matp.DoesNotExist:
                    stock_actual = 0

                if stock_actual <= 0 or stock_actual < d.cantidad_usada:
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
        imagen_produc = request.FILES.get('imagen_produc')
        nom_produc = request.POST.get('nom_produc')
        gen_produc = request.POST.get('gen_produc')
        desc_produc = request.POST.get('desc_produc')
        categoria_produc = request.POST.get('cat_produc')
        estado_produc = request.POST.get('estado_produc')
        precio = request.POST.get('precio')
        dias_produccion = request.POST.get('dias_produccion')

        tallas_elegidas = request.POST.getlist('tallas_seleccionadas[]')
        colores_elegidos = request.POST.getlist('colores_nuevos[]')

        try:
            precio_limpio = re.sub(r'[^\d.]', '', precio.replace(',', '.'))
            valor = Decimal(precio_limpio)
        except (InvalidOperation, TypeError, ValueError):
            valor = Decimal('0.00')

        if imagen_produc:
            hasher = hashlib.sha256()
            for chunk in imagen_produc.chunks():
                hasher.update(chunk)
            nuevo_hash = hasher.hexdigest()
            imagen_produc.seek(0)

            if Producto.objects.filter(imagen_hash=nuevo_hash).exists():
                return render(request, 'ventas/producto/lista_product.html', {
                    'error': 'ERROR: Esta prenda ya ha sido subida anteriormente.',
                    'materiales': materiales_db,
                    'productos': productos
                })

        nuevo_p = Producto.objects.create(
            imagen_product=imagen_produc,
            imagen_hash=nuevo_hash,
            nom_produc=nom_produc,
            gen_produc=gen_produc,
            desc_produc=desc_produc,
            categoria_produc=categoria_produc,
            estado_produc=estado_produc,
            precio=valor,
            dias_produccion=dias_produccion,
            tallas_disponibles=",".join(tallas_elegidas) if tallas_elegidas else "S,M,L",
            colores_disponibles=",".join(colores_elegidos) if colores_elegidos else "#ffffff,#000000"
        )

        ids_materiales = request.POST.getlist('material_ids[]')
        cantidades = request.POST.getlist('cantidades[]')

        for id_mat, cant in zip(ids_materiales, cantidades):
            if id_mat and cant:
                try:
                    Det_mov_matp.objects.create(
                        producto=nuevo_p,
                        materia_prima_id=id_mat,
                        cantidad_usada=Decimal(cant)
                    )
                except (ValueError, InvalidOperation):
                    continue

                messages.success(request, "Producto creado con éxito.")
        return redirect('ventas:lista_producto_admin')

    return render(request, 'ventas/producto/lista_product.html', {
        'materiales': materiales_db,
        'productos': productos
    })

@solo_personal
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id_produc=id)
    Movimiento_matp = apps.get_model('inventario', 'Movimiento_matp')
    
    if request.method == 'POST':
        nueva_imagen = request.FILES.get('imagen_product')
        if nueva_imagen:
            producto.imagen_product = nueva_imagen
            hasher = hashlib.sha256()
            for chunk in nueva_imagen.chunks():
                hasher.update(chunk)
            producto.imagen_hash = hasher.hexdigest()
            nueva_imagen.seek(0)

        producto.nom_produc = request.POST.get('nom_produc')
        producto.gen_produc = request.POST.get('gen_produc')
        producto.desc_produc = request.POST.get('desc_produc', '')
        producto.categoria_produc = request.POST.get('categoria_produc')
        
        dias = request.POST.get('dias_produccion')
        producto.dias_produccion = int(dias) if dias and dias.strip() != "" else 10
        producto.estado_produc = request.POST.get('estado_produc', 'Nuevo')
        
        precio = request.POST.get('precio', '0')
        try:
            precio_limpio = re.sub(r'[^\d.]', '', precio.replace(',', '.'))
            producto.precio = Decimal(precio_limpio)
        except (InvalidOperation, TypeError, ValueError):
            producto.precio = Decimal('0.00')

        tallas_nuevas = request.POST.getlist('tallas_seleccionadas[]')
        colores_nuevos = request.POST.getlist('colores_nuevos[]')
        
        producto.tallas_disponibles = ",".join(tallas_nuevas) if tallas_nuevas else "S,M,L"
        producto.colores_disponibles = ",".join(colores_nuevos) if colores_nuevos else "#ffffff,#000000"
        
        producto.save()

        Det_mov_matp.objects.filter(producto=producto).delete()
        material_ids = request.POST.getlist('material_ids[]')
        cantidades = request.POST.getlist('cantidades[]')

        for id_mat, cant in zip(material_ids, cantidades):
            if id_mat and cant:
                try:
                    insumo = Movimiento_matp.objects.get(pk=id_mat)
                    Det_mov_matp.objects.create(
                        producto=producto,
                        materia_prima=insumo,
                        cantidad_usada=Decimal(cant)
                    )
                except (Movimiento_matp.DoesNotExist, ValueError, InvalidOperation):
                    continue

                messages.success(request, "Producto actualizado con exito.")
        return redirect('ventas:lista_producto_admin')
        
    materiales_db = Movimiento_matp.objects.all()
    detalles_materiales = Det_mov_matp.objects.filter(producto=producto).select_related('materia_prima')

    tallas_actuales = producto.tallas_disponibles.split(',') if producto.tallas_disponibles else ["S", "M", "L"]
    colores_actuales = producto.colores_disponibles.split(',') if producto.colores_disponibles else ["#ffffff", "#000000"]
    
    contexto = {
        'producto': producto,
        'materiales': materiales_db,
        'tallas_actuales': tallas_actuales,
        'colores_actuales': colores_actuales,
        'detalles_materiales': detalles_materiales,
    }
    return render(request, 'ventas/producto/editar_producto.html', contexto)

@solo_personal
def eliminar_producto(request, product_id):
    producto = get_object_or_404(Producto, id_produc=product_id)
    
    try:
        with transaction.atomic():
            producto.delete()
            messages.success(request, f"✅ Producto '{producto.nom_produc}' eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"❌ Error al intentar eliminar: {e}")

    return redirect('ventas:lista_producto_admin')

#----------------- PRODUCTO SIN VARIACION ---------------------
@login_requerido_custom
def producto_sin_personalizar(request, producto_id):
    producto = get_object_or_404(Producto, id_produc=producto_id)

    tallas = producto.tallas_disponibles.split(',') if producto.tallas_disponibles else ["S", "M", "L"]
    colores = producto.colores_disponibles.split(',') if producto.colores_disponibles else ["#ffffff", "#000000"]
    if request.method == 'POST':
        print("ENTRÓ AL POST")
        print(request.POST)

    if request.method == 'POST':
        cliente = obtener_cliente_actual(request)
        talla = request.POST.get('talla')
        color = request.POST.get('color')
        
        try:
            cantidad = int(request.POST.get('cantidad', 1))
        except (ValueError, TypeError):
            cantidad = 1

        with transaction.atomic():
            pedido, creado = Pedido.objects.get_or_create(
                id_clien_fk=cliente,
                estado_ped='Carrito', 
                defaults={'subtotal_ped': 0, 'valor_ped': 0, 'metodo_pago': 'Pendiente'}
            )

            detalle_existente = Det_valor.objects.filter(
                id_ped_fk_detval=pedido,
                id_prod_fk_detval=producto,
                id_var_fk_detval__talla_var=talla,
                id_var_fk_detval__color_var=color,
                tipo_pedido='Estandar'
            ).first()

            if detalle_existente:
                var = detalle_existente.id_var_fk_detval
                var.cant_soli += cantidad
                var.save()

                detalle_existente.cant = var.cant_soli
                detalle_existente.valor_total = int(producto.precio * detalle_existente.cant)
                detalle_existente.save()
            else:
                variacion = Variacion.objects.create(
                    talla_var=talla, 
                    cant_soli=cantidad, 
                    color_var=color,
                    mat_var="Algodón", 
                    costo_var=0,  
                    id_estam_fk_var=None 
                )

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
@login_requerido_custom
def lista_abono(request):
    abonos = Abono.objects.all()
    return render(request, 'ventas/abono/lista_abono.html', {'abonos': abonos})

@login_requerido_custom
def crear_abono(request, pedido_id):
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
    
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
    print("===== FINALIZAR PEDIDO =====")
    print("SESSION:", dict(request.session))
    print("usuario_id:", request.session.get('usuario_id'))
    print("rol:", request.session.get('rol'))

    cliente = obtener_cliente_actual(request)
    print("CLIENTE:", cliente)

    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('usuarios:login')
    
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id)
    detalles = Det_valor.objects.filter(id_ped_fk_detval=pedido)
    
    # --- CÁLCULOS FINANCIEROS (Fuera del POST para disponibilidad en GET) ---
    resultados = detalles.aggregate(
        total=Sum('valor_total'),
        max_espera=Max('id_prod_fk_detval__dias_produccion')
    )
    
    total_productos = Decimal(str(resultados['total'] or 0))
    dias_produccion = resultados['max_espera'] or 1
    
    abonos_previos = Abono.objects.filter(id_pedido_fk_abono=pedido).aggregate(total_abonos=Sum('monto_abono'))
    total_abonado = Decimal(str(abonos_previos['total_abonos'] or 0))
    
    saldo_pendiente = total_productos - total_abonado
    # -----------------------------------------------------------------------
    
    if request.method == 'POST':
        tipo_pago = request.POST.get('tipo_pago')

        if tipo_pago == 'abono':
            return redirect('ventas:crear_abono', pedido_id=pedido.id_pedido)
            
        if not detalles.exists():
            messages.error(request, "Tu carrito está vacío.")
            return redirect('ventas:lista_product')
            
        
        try: 
            with transaction.atomic(): 
                alerta_stock = gestionar_inventario(pedido, operacion='RESTAR')
                
                pedido.subtotal_ped = total_productos
                pedido.valor_ped = total_productos
                pedido.metodo_pago = request.POST.get('metodo_pago')
                pedido.fecha_ped = timezone.now().date()
                pedido.fecha_entrega = timezone.now().date() + timedelta(days=dias_produccion)
                pedido.estado_ped = 'Confirmado' 
                pedido.save()

                Abono.objects.create(
                    id_pedido_fk_abono=pedido,
                    monto_abono=saldo_pendiente,
                    metodo_pago=request.POST.get('metodo_pago'),
                    descripcion=f"Pago final por saldo pendiente de ${saldo_pendiente}."
                )

                messages.success(request, f"¡Pedido confirmado! Saldo liquidado: ${saldo_pendiente}. Estará listo el {pedido.fecha_entrega}")
                return redirect('ventas:lista_product')
            
        except Exception as e: 
            messages.error(request, f"Error al procesar el pago: {e}")
            return redirect('ventas:ver_carrito')

    # Al llegar aquí (GET), las variables ya existen y el template las recibirá correctamente
    return render(request, 'ventas/pedido/finalizar.html', {
        'pedido': pedido, 
        'total_productos': total_productos,
        'total_abonado': total_abonado,
        'saldo_pendiente': saldo_pendiente
    })


@login_requerido_custom
def lista_pedidos_client(request):
    cliente = obtener_cliente_actual(request)
    if not cliente:
        return redirect('usuarios:login')
    total_pedidos_cliente = Pedido.objects.filter(id_clien_fk=cliente).count()
    print(f"DEBUG: Cliente {cliente} tiene {total_pedidos_cliente} pedidos en total.")
    
    # Imprime cuántos pedidos quedan tras el filtro
    pedidos_queryset = Pedido.objects.filter(
        id_clien_fk=cliente
    ).exclude(estado_ped__in=['Entregado', 'Cancelado']).order_by('-id_pedido')
    
    print(f"DEBUG: Pedidos después del filtro: {pedidos_queryset.count()}")
    
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
            'estado': pedido.estado_ped, 
            'foto': primer_item.id_prod_fk_detval.imagen_product.url if primer_item and primer_item.id_prod_fk_detval.imagen_product else None,
            'total': total_pedido,
            'total_abonado': total_abonado,
            'saldo_pendiente': saldo_pendiente,
            'bloqueado': bloqueado
        })

    return render(request, 'ventas/pedido/lista_ped_cliente.html', {
        'pedidos_con_detalles': pedidos_con_detalles
    })


@login_requerido_custom
def editar_pedido(request, id): 
    cliente = obtener_cliente_actual(request)
    if not cliente: 
        messages.error(request, "Perfil de cliente no encontrado.")
        return redirect('usuarios:login')
        
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


@login_requerido_custom
def gestionar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    
    if request.method == "POST":
        accion = request.POST.get('accion')
        
        if accion == "cancelar":
            with transaction.atomic():
                pedido.estado_ped = "Cancelado"
                pedido.save()
                
                # 🌟 LOGICA: Devolvemos la materia prima al inventario
                gestionar_inventario(pedido, 'SUMAR')
                
                try:
                    correo_cliente = pedido.id_clien_fk.correo_clien if pedido.id_clien_fk else None
                    
                    if correo_cliente:
                        # 🌟 CORRECCIÓN: Corrección de sintaxis Python para el nombre por defecto
                        nombre_cliente = pedido.id_clien_fk.nom_clien if pedido.id_clien_fk and pedido.id_clien_fk.nom_clien else 'Cliente'
                        
                        asunto = f"Actualización de tu Pedido #{pedido.id_pedido} - Luxy Fashion"
                        cuerpo_mensaje = (
                            f"Hola {nombre_cliente},\n\n"
                            f"Te notificamos que tu pedido #{pedido.id_pedido} ha sido cancelado con éxito.\n\n"
                            f"Atentamente,\nEquipo Luxy Fashion"
                        )
                        
                        email = EmailMessage(
                            subject=asunto,
                            body=cuerpo_mensaje,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[correo_cliente],
                        )
                        email.send(fail_silently=False)
                        messages.success(request, "El pedido ha sido cancelado, el inventario devuelto y se notificó al cliente.")
                    else:
                        messages.success(request, "El pedido ha sido cancelado (Venta presencial sin correo asociado).")
                
                except Exception as e:
                    print(f"\n ERROR DETECTADO EN ENVIAR CORREO: {str(e)}\n")
                    messages.error(request, f"Pedido cancelado e inventario devuelto, pero falló el correo: {e}")
            
            return redirect('ventas:lista_pedidos_cliente')
            
        elif accion == "entregado":
            with transaction.atomic():
                pedido.estado_ped = "Entregado"
                pedido.save()
            
            try:
                if pedido.id_clien_fk and pedido.id_clien_fk.correo_clien:
                    email = EmailMessage(
                        subject=f"¡Tu pedido #{pedido.id_pedido} ha sido entregado! 🎉",
                        body=f"Hola, confirmamos que tu pedido ha sido entregado exitosamente.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[pedido.id_clien_fk.correo_clien],
                    )
                    email.send(fail_silently=False)
                    messages.success(request, "¡Entrega confirmada y correo enviado!")
                else:
                    messages.success(request, "¡Entrega confirmada!")
            except Exception as e:
                print(f"🚨 ERROR EN ENTREGA: {str(e)}")
                messages.error(request, f"Entrega guardada, pero el correo falló: {e}")
            
            return redirect('ventas:lista_pedido')

    return redirect('ventas:lista_pedido')


#------------------------ CARRITO --------------------------
@login_requerido_custom
def ver_carrito(request): 
    cliente = obtener_cliente_actual(request)

    # 1. Definimos los pedidos base (Carrito O Pendientes de pago)
    # Excluimos terminados/cancelados
    pedidos = Pedido.objects.filter(
        Q(id_clien_fk=cliente) | Q(id_clien_fk__isnull=True)
    ).exclude(
        estado_ped__in=['Entregado', 'Cancelado', 'Completado']
    )

    pedidos_info = [] 
    formato = Decimal('0.00')

    for pedido in pedidos:
        # Calculamos totales
        items = Det_valor.objects.filter(id_ped_fk_detval=pedido).select_related('id_var_fk_detval')
        
        # Total productos
        total_raw = items.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        total_productos = Decimal(str(total_raw)).quantize(formato)

        # Total abonado
        abono_raw = Abono.objects.filter(id_pedido_fk_abono=pedido).aggregate(Sum('monto_abono'))['monto_abono__sum'] or 0
        total_abonado = Decimal(str(abono_raw)).quantize(formato)
        
        saldo_pendiente = (total_productos - total_abonado).quantize(formato)

        # 2. LÓGICA CLAVE: 
        # Mostramos si está en 'Carrito' O si tiene saldo pendiente
        if pedido.estado_ped == 'Carrito' or saldo_pendiente > 0:
            
            # Verificamos si tiene personalización 3D
            tiene_3d = items.filter(id_personalizacion_3d__isnull=False).exists()

            pedidos_info.append({
                'pedido': pedido,
                'items': items,
                'total_productos': total_productos,
                'total_abonado': total_abonado,
                'saldo_pendiente': saldo_pendiente,
                'tiene_3d': tiene_3d, # Variable para el template
            })

    return render(request, 'ventas/pedido/carrito.html', {'pedidos_info': pedidos_info})

@login_requerido_custom
def eliminar_del_carrito(request, id_det_valor):
    # Usamos pk=id_det_valor para buscar por ID automáticamente
    detalle = get_object_or_404(Det_valor, pk=id_det_valor)
    
    if detalle.id_ped_fk_detval.estado_ped != 'Carrito':
        messages.error(request, "No puedes eliminar productos de un pedido ya confirmado.")
        return redirect('ventas:ver_carrito')

    with transaction.atomic():
        # Limpieza de archivos 3D
        if hasattr(detalle, 'id_personalizacion_3d') and detalle.id_personalizacion_3d:
            pedido_3d = detalle.id_personalizacion_3d
            for img in [pedido_3d.foto_frente, pedido_3d.foto_espalda, pedido_3d.foto_lateral]:
                if img and os.path.exists(img.path):
                    os.remove(img.path)
            pedido_3d.delete()
        
        detalle.delete()
        
    messages.success(request, "Producto eliminado correctamente.")
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
                        material_stock.pedido_origen = pedido
                        material_stock.tipo_mmtp = 'SALIDA'
                    elif operacion == 'SUMAR':
                        material_stock.stock_mmtp += cantidad_a_mover
                        material_stock.pedido_origen = pedido
                        material_stock.tipo_mmtp = 'ENTRADA'
                    
                    material_stock.save()
                except Movimiento_matp.DoesNotExist:
                    continue


#---------------------- listas empleados --------------------------------------------------------

def lista_producto_e(request):
    productos = Producto.objects.all()
    estampados = Estampado.objects.all()
    context = {
        'productos': productos,
        'estampados': estampados,
    }
    return render(request, 'ventas/producto/lista_producto_e.html', context)

@csrf_exempt
def venta_empleado(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            productos = data.get('productos', [])
            metodo_pago = data.get('metodo_pago', 'Efectivo')

            if not productos:
                return JsonResponse({'success': False, 'message': 'No hay productos en la solicitud'})

            nombre_empleado = request.session.get('username', 'Empleado Sistema')

            with transaction.atomic():
                # 1. Crear el Pedido base
                pedido = Pedido.objects.create(
                    subtotal_ped=0,
                    valor_ped=0,
                    estado_ped='Confirmado',
                    metodo_pago=metodo_pago,
                    id_clien_fk=None  
                )

                total = Decimal('0')

                # 2. Recorrer cada producto enviado desde el carrito/tabla
                for item in productos:
                    producto = Producto.objects.get(id_produc=item['id'])
                    cantidad = int(item['cantidad'])
                    talla = item['talla']
                    color = item['color']
                    
                    id_estampado = item.get('id_estampado')
                    foto_frente_base64 = item.get('foto_frente')
                    tamano_estampado = float(item.get('tamano_estampado', 40))
                    lista_estampados = item.get('lista_estampados',[])
                    print("LISTA:", lista_estampados)
                    cantidad_total_estampados = int(item.get('cantidad_total_estampados',0))
                    print("TOTAL:", cantidad_total_estampados)
                    print("ITEM:", item)

                    precio_base_producto = Decimal(str(producto.precio))
                    personalizacion_3d = None
                    tamano_texto = "Estándar"
                    descripcion_mat = "Venta Empleado"

                    # 💰 CÁLCULO MATEMÁTICO INTACTO DESDE EL SERVIDOR
                    if id_estampado:
                        # Si es imagen propia subida por el cliente
                        costo_imagen_propia = float(
                            item.get('costo_imagen_propia', 20000)
                        )

                        precio_base_producto = calcular_precio_personalizacion(
                            producto.precio,
                            lista_estampados,
                            tamano_estampado,
                            cantidad_total_estampados,
                            costo_imagen_propia
                        )
                                                
                        # 🛡️ BLINDAJE: Django decide el tamaño real según la escala numérica del objeto
                        precio_tamano = Decimal('0')
                        if tamano_estampado >= 180:
                            precio_tamano = Decimal('12000')
                            tamano_texto = "Grande"

                        elif tamano_estampado >= 90:
                            precio_tamano = Decimal('5000')
                            tamano_texto = "Mediano"

                        else:
                            tamano_texto = "Pequeño"

                        
                        # Guardamos el registro del tamaño real calculado por el servidor en la descripción
                        descripcion_mat += f" ({tamano_texto})"

                        # 📸 CAPTURA VISUAL DE EVIDENCIA
                        if foto_frente_base64 and ";base64," in foto_frente_base64:
                            import base64
                            from django.core.files.base import ContentFile
                            
                            format, imgstr = foto_frente_base64.split(';base64,')
                            ext = format.split('/')[-1]
                            
                            archivo_foto = ContentFile(
                            base64.b64decode(imgstr),
                            name=f"render_empleado.{ext}"
                        )

                        personalizacion_3d = PedidoPersonalizado.objects.create(
                            producto=producto,
                            estampado=None,
                            color_hex=color,
                            tipo_personalizacion="3D",
                            foto_frente=archivo_foto,
                            precio_final=precio_base_producto
                        )

                    # Calcular subtotal definitivo multiplicando por la cantidad
                    subtotal = precio_base_producto * cantidad

                    # 3. Crear Variación
                    variacion = Variacion.objects.create(
                        talla_var=talla,
                        cant_soli=cantidad,
                        color_var=color,
                        mat_var=descripcion_mat,
                        costo_var=subtotal
                    )

                    # 4. Crear Detalle de Valor
                    Det_valor.objects.create(
                        valor_total=subtotal,
                        tipo_pedido=f"Venta Empleado: {nombre_empleado}",
                        id_ped_fk_detval=pedido,
                        id_var_fk_detval=variacion,
                        id_prod_fk_detval=producto,
                        id_personalizacion_3d=personalizacion_3d 
                    )

                    total += subtotal

                # 5. Actualizar totales del pedido
                pedido.subtotal_ped = total
                pedido.valor_ped = total
                pedido.save()

                # 6. Registrar el Abono/Pago inmediato
                Abono.objects.create(
                    monto_abono=total,
                    metodo_pago=metodo_pago,
                    descripcion=f"Venta registrada por {nombre_empleado}",
                    id_pedido_fk_abono=pedido
                )

                # 7. Descontar stock de materias primas
                gestionar_inventario(pedido, 'RESTAR')

            return JsonResponse({'success': True, 'message': 'Pago realizado correctamente'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Método no permitido'})