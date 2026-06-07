from email.policy import default
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
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
import smtplib  
from django.apps import apps

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
                # Si el pedido es por abonos/crédito y lo abonado es menor al valor total, pasa a 'Pendiente'
                if "Abono" in pedido_obj.metodo_pago or "Crédito" in pedido_obj.metodo_pago:
                    if total_abonado < Decimal(str(pedido_obj.valor_ped)):
                        pedido_obj.estado_ped = "Pendiente"
                    else:
                        pedido_obj.estado_ped = "Entregado" # O el estado completado que manejes

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
                
                # 🌟 CONTROL DE EN BLANCO: Si no viene cliente, inyectamos la marca del empleado
                if not pedido_obj.id_clien_fk:
                    if "Venta Empleado:" in d.tipo_pedido:
                        # Extrae el nombre del empleado que guardamos en el string
                        pedido_obj.vendedor_nombre = d.tipo_pedido.replace("Venta Empleado:", "").strip()
                    else:
                        pedido_obj.vendedor_nombre = "Empleado Interno"
                else:
                    # Si es un cliente normal, usamos su nombre de usuario de la FK
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
                p_sim.vendedor_nombre = "Prueba Técnica" # Anti-en blanco para huérfanos
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
@login_requerido_custom
def lista_producto(request):
    # Traemos los productos con sus recetas e insumos optimizados
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
                    # 🌟 Buscamos el ÚLTIMO movimiento real de este insumo en el inventario
                    ultimo_movimiento = Movimiento_matp.objects.filter(
                        mat_mmtp=d.materia_prima.mat_mmtp,
                        color_mmtp=d.materia_prima.color_mmtp
                    ).latest('id_mmtp')
                    
                    stock_actual = ultimo_movimiento.stock_mmtp
                    
                except Movimiento_matp.DoesNotExist:
                    # Si ni siquiera tiene un registro en movimientos, no hay stock disponible
                    stock_actual = 0

                # 🚨 LA CORRECCIÓN CLAVE: Si el stock es menor o igual a 0, 
                # o si no alcanza para cubrir la cantidad que usa la receta, se oculta.
                if stock_actual <= 0 or stock_actual < d.cantidad_usada:
                    es_valido = False
                    break # Detiene la revisión de este producto, ya sabemos que no tiene material

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

        # 🌟 NUEVO: Capturar las opciones de variantes elegidas
        tallas_elegidas = request.POST.getlist('tallas_seleccionadas[]')
        colores_elegidos = request.POST.getlist('colores_nuevos[]')

        try: 
            precio_limpio = re.sub(r'[^\d]', '', precio)
            valor = Decimal(precio_limpio)
        except(InvalidOperation, TypeError):
            valor = Decimal('0.00')

        if imagen_produc: 
            hasher = hashlib.sha256()
            for chunk in imagen_produc.chunks():
                hasher.update(chunk)
            nuevo_hash = hasher.hexdigest()
            imagen_produc.seek(0)

            if Producto.objects.filter(imagen_hash=nuevo_hash).exists():
                return render(request, 'ventas/producto/lista_product.html',{
                    'error': 'ERROR: Esta prenda ya ha sido subida anteriormente.',
                    'materiales': materiales_db,
                    'productos': productos
                })
        
        # Estructura lógica original e intacta
        nuevo_p = Producto.objects.create(
            imagen_product=imagen_produc, imagen_hash=nuevo_hash, nom_produc=nom_produc, gen_produc=gen_produc,
            desc_produc=desc_produc, categoria_produc=categoria_produc, estado_produc=estado_produc, 
            precio=valor, dias_produccion=dias_produccion
        )
        
        # 🌟 Guardar la relación en la sesión para que el cliente la pueda leer sin alterar la tabla Producto
        if not request.session.get('variaciones_productos'):
            request.session['variaciones_productos'] = {}
        
        request.session['variaciones_productos'][str(nuevo_p.id_produc)] = {
            'tallas': tallas_elegidas if tallas_elegidas else ["S", "M", "L"],
            'colores': [c.strip().lower() for c in colores_elegidos if c.strip()] if colores_elegidos else ["blanco"]
        }
        request.session.modified = True

        ids_materiales = request.POST.getlist('material_ids[]')
        cantidades = request.POST.getlist('cantidades[]')

        for id_mat, cant in zip(ids_materiales, cantidades):
            if id_mat and cant:
                Det_mov_matp.objects.create(
                    producto = nuevo_p,
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
    
    # Obtener el modelo de inventario dinámicamente para evitar Error Circular
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
            # 🌟 CORRECCIÓN: Permite números enteros y decimales con punto (ej: 25000.50)
            precio_limpio = re.sub(r'[^\d.]', '', precio.replace(',', '.'))
            valor = Decimal(precio_limpio)
        except (InvalidOperation, TypeError):
            valor = Decimal('0.00')

        producto.precio = valor
        producto.save()

        # 🌟 Variantes (Estructura en Sesión)
        tallas_nuevas = request.POST.getlist('tallas_seleccionadas[]')
        colores_nuevos = request.POST.getlist('colores_nuevos[]')
        colores_limpios = [c.strip().lower() for c in colores_nuevos if c.strip()]

        if 'variaciones_productos' not in request.session:
            request.session['variaciones_productos'] = {}

        id_str = str(producto.id_produc)
        request.session['variaciones_productos'][id_str] = {
            'tallas': tallas_nuevas if tallas_nuevas else ["S", "M", "L"],
            'colores': colores_limpios if colores_limpios else ["blanco"]
        }
        request.session.modified = True

        # 🌟 Materia Prima (Guardado en Base de Datos)
        material_ids = request.POST.getlist('material_ids[]')
        cantidades = request.POST.getlist('cantidades[]')

        # Eliminamos los materiales anteriores para reescribir los nuevos
        Det_mov_matp.objects.filter(producto=producto).delete()

        for id_mat, cant in zip(material_ids, cantidades):
            if id_mat and cant:
                try:
                    # Buscamos la instancia real antes de guardarla
                    insumo = Movimiento_matp.objects.get(pk=id_mat)
                    Det_mov_matp.objects.create(
                        producto=producto,
                        materia_prima=insumo,
                        cantidad_usada=Decimal(cant)
                    )
                except (Movimiento_matp.DoesNotExist, ValueError, InvalidOperation):
                    continue

        return redirect('ventas:lista_producto_admin')
        
    # --- GET: Cargar datos guardados ---
    materiales_db = Movimiento_matp.objects.all()  
    detalles_materiales = Det_mov_matp.objects.filter(producto=producto).select_related('materia_prima')

    id_str = str(producto.id_produc)
    variaciones = request.session.get('variaciones_productos', {}).get(id_str, {})
    
    tallas_actuales = variaciones.get('tallas', ["S", "M", "L"])
    colores_actuales = variaciones.get('colores', ["blanco"])

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
    if request.method == 'POST':
        producto.delete()
        return redirect('ventas:lista_producto_admin')
    return render(request, 'ventas/producto/eliminar_producto.html', {'producto':producto})

#----------------- PRODUCTO SIN VARIACION ---------------------
@login_requerido_custom
def producto_sin_personalizar(request, producto_id):
    producto = get_object_or_404(Producto, id_produc=producto_id)
    
    # Para evitar el aislamiento de sesiones Admin/Cliente, buscamos en la sesión activa.
    variaciones_globales = request.session.get('variaciones_productos', {})
    datos_producto = variaciones_globales.get(str(producto.id_produc), None)
    
    if datos_producto:
        tallas = datos_producto['tallas']
        colores = datos_producto['colores']
    else:
        # Si el cliente entra desde otra sesión, le mostramos valores base lógicos
        tallas = ["S", "M", "L"]
        colores = ["blanco", "negro"]
    
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

            variacion = Variacion.objects.create(
                talla_var=talla, 
                cant_soli=cantidad, 
                color_var=color,
                mat_var="Algodón", 
                costo_var=producto.precio, 
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
    # 1. Obtener el cliente de la sesión actual
    cliente = obtener_cliente_actual(request)
    if not cliente:
        return redirect('usuarios:login')
    
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
            'estado': pedido.estado_ped, # Para mostrar en qué parte del proceso va (ej: 'En confección', 'Enviado')
            'foto': primer_item.id_prod_fk_detval.imagen_product.url if primer_item and primer_item.id_prod_fk_detval.imagen_product else None,
            'total': total_pedido,
            'abonado': total_abonado,
            'saldo': max(0, saldo_pendiente),
            'bloqueado': bloqueado 
        })

    # 4. Renderizar la plantilla con la lista limpia
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

def gestionar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    
    if request.method == "POST":
        accion = request.POST.get('accion')
        
        if accion == "cancelar":
            with transaction.atomic():
                pedido.estado_ped = "Cancelado"
                pedido.save()
                
                try:
                    correo_cliente = pedido.id_clien_fk.correo_clien
                    
                    asunto = f"Actualización de tu Pedido #{pedido.id_pedido} - Luxy Fashion"
                    cuerpo_mensaje = (
                        f"Hola {pedido.id_clien_fk.nom_clien|default:'Cliente'},\n\n"
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
                    
                    messages.success(request, "El pedido ha sido cancelado y se notificó al cliente.")
                
                except Exception as e:
                    print("\n" + "="*50)
                    print(f"ERROR DETECTADO EN GMAIL: {str(e)}")
                    print("="*50 + "\n")
                    messages.error(request, f"Error al enviar el correo: {e}")
            
            return redirect('ventas:lista_pedidos_cliente')
            
        elif accion == "entregado":
            # Control de seguridad: Si no es del personal, lo saca
            if not request.user.is_staff:
                messages.error(request, "No tienes permisos para confirmar entregas.")
                return redirect('usuarios:login')

            pedido.estado_ped = "Entregado"
            pedido.save()
            
            try:
                correo_cliente = pedido.id_clien_fk.correo_clien
                email = EmailMessage(
                    subject=f"¡Tu pedido #{pedido.id_pedido} ha sido entregado! 🎉",
                    body=f"Hola, confirmamos que tu pedido ha sido entregado exitosamente.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[correo_cliente],
                )
                email.send(fail_silently=False)
                messages.success(request, "¡Entrega confirmada y correo enviado!")
            except Exception as e:
                print(f"🚨 ERROR EN ENTREGA: {str(e)}")
                messages.error(request, f"Entrega guardada, pero el correo falló: {e}")
            
            return redirect('ventas:lista_pedido')

    return redirect('ventas:lista_pedido')
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
                        # 🌟 GUARDAMOS EL PEDIDO: Marcamos de dónde viene el movimiento y cambiamos el tipo
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
                return JsonResponse({'success': False, 'message': 'No hay productos en la solicitud'})

            # Obtener nombre del empleado desde la sesión
            nombre_empleado = request.session.get('username', 'Empleado Sistema')

            # =========================
            # CREAR PEDIDO
            # =========================
            pedido = Pedido.objects.create(
                subtotal_ped = 0,
                valor_ped = 0,
                estado_ped = 'Confirmado',
                metodo_pago = metodo_pago,
                id_clien_fk = None  # Venta física directa
            )

            total = Decimal('0')

            # =========================
            # RECORRER PRODUCTOS
            # =========================
            for item in productos:
                producto = Producto.objects.get(id_produc = item['id'])
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
                    tipo_pedido = f"Venta Empleado: {nombre_empleado}",
                    id_ped_fk_detval = pedido,
                    id_var_fk_detval = variacion,
                    id_prod_fk_detval = producto
                )

                total += subtotal

            # =========================
            # ACTUALIZAR TOTALES DEL PEDIDO
            # =========================
            pedido.subtotal_ped = total
            pedido.valor_ped = total
            pedido.save()

            # =========================
            # ABONO AUTOMÁTICO
            # =========================
            Abono.objects.create(
                monto_abono = total,
                metodo_pago = metodo_pago,
                descripcion = f"Venta registrada por {nombre_empleado}",
                id_pedido_fk_abono = pedido
            )

            # =========================
            # DESCONTAR INVENTARIO (CORREGIDO)
            # =========================
            try:
                # Aquí llamamos directamente a tu función importada en el archivo
                gestionar_inventario(pedido, 'RESTAR')
            except NameError:
                # Si la función está en otro archivo (por ejemplo utilidades.py o admin.py), 
                # asegúrate de importarla arriba en tu views.py como:
                # from .utils import gestionar_inventario
                pass

            return JsonResponse({'success': True, 'message': 'Pago realizado correctamente'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Método no permitido'})