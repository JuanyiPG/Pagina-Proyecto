<<<<<<< Updated upstream
=======
import hashlib
from decimal import Decimal
from datetime import date, timedelta
>>>>>>> Stashed changes
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

# Importación de modelos según la estructura de tus vistas
from .models import Pedido, Variacion, Det_valor, Producto, Cliente, Abono, Det_mov_matp
from inventario.models import Estampado, Movimiento_matp

User = get_user_model()

class VentasFlujoTestCase(TestCase):

    def setUp(self):
        """Configuración inicial del entorno de prueba (Fixtures)"""
        # 1. Crear un usuario de Django y su perfil de Cliente asociado
        self.user = User.objects.create_user(username='cliente_test', password='password123')
        self.cliente = Cliente.objects.create(
            id_usuario_fk=self.user.id
            # Añade aquí más campos si tu modelo Cliente los requiere como obligatorios
        )

        # 2. Configurar el cliente de pruebas simulando la sesión activa del usuario
        self.client = Client()
        session = self.client.session
        session['usuario_id'] = self.user.id
        session.save()

        # 3. Crear productos base para las pruebas
        self.producto = Producto.objects.create(
            nom_produc="Camiseta Luxy Premium",
            precio=Decimal('60000.00'),
            dias_produccion=6,
            estado_produc="Activo"
        )

        # 4. Crear estampados para pruebas de personalización
        self.estampado = Estampado.objects.create(
            nom_estam="Diseño Minimalista",
            costo_adi=Decimal('15000.00')
        )

        # 5. Configurar insumos en el inventario
        self.material = Movimiento_matp.objects.create(
            mat_mmtp="Algodón Perchado",
            color_mmtp="negro",
            stock_mmtp=50.0,
            tipo_mmtp="ENTRADA"
        )

        # 6. Asignar la receta (materia prima que usa el producto)
        self.receta = Det_mov_matp.objects.create(
            producto=self.producto,
            materia_prima=self.material,
            cantidad_usada=2.0  # Consume 2 unidades por cada prenda armada
        )

    def test_producto_sin_personalizar_crea_carrito_y_detalle(self):
        """Evalúa que añadir un producto estándar cree correctamente el Pedido 'Carrito' y su Det_valor"""
        url = reverse('ventas:producto_sin_personalizar', args=[self.producto.id_produc])
        data = {
            'talla': 'L',
            'color': 'negro',
            'cantidad': 3
        }
        
        response = self.client.post(url, data)
        
        # Debe redireccionar a la lista de productos
        self.assertEqual(response.status_code, 302)
        
        # Validar la existencia del pedido en estado Carrito
        pedido = Pedido.objects.filter(id_clien_fk=self.cliente, estado_ped='Carrito').first()
        self.assertIsNotNone(pedido)
        
        # Validar el Det_valor calculado: precio_producto (60000) * cantidad (3) = 180000
        detalle = Det_valor.objects.filter(id_ped_fk_detval=pedido).first()
        self.assertIsNotNone(detalle)
        self.assertEqual(detalle.valor_total, 180000)
        self.assertEqual(detalle.tipo_pedido, 'Estandar')

    def test_crear_variacion_personalizada_con_estampado(self):
        """Prueba la vista crear_variacion adjuntando un costo de estampado adicional"""
        # Creamos un pedido base simulando que ya existe un carrito activo
        pedido_carrito = Pedido.objects.create(id_clien_fk=self.cliente, estado_ped='Carrito')
        
        url = reverse('ventas:crear_variacion', args=[self.producto.id_produc, pedido_carrito.id_pedido])
        data = {
            'id_estam': self.estampado.id_estam,
            'talla_var': 'M',
            'cant_soli': 2,
            'color_var': 'gris',
            'mat_var': 'Poliéster'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        # El detalle debe calcular: (precio_producto (60000) + costo_adi (15000)) * cant (2) = 150000
        detalle = Det_valor.objects.filter(id_ped_fk_detval=pedido_carrito).first()
        self.assertIsNotNone(detalle)
        self.assertEqual(detalle.valor_total, 150000)
        self.assertEqual(detalle.tipo_pedido, 'Personalizado')

    def test_crear_abono_parcial_y_afectacion_inventario(self):
        """Verifica que el primer abono disminuya las existencias físicas del inventario de insumos"""
        pedido = Pedido.objects.create(id_clien_fk=self.cliente, estado_ped='Carrito')
        variacion = Variacion.objects.create(talla_var='S', cant_soli=5, color_var='negro')
        Det_valor.objects.create(
            id_ped_fk_detval=pedido, id_prod_fk_detval=self.producto,
            id_var_fk_detval=variacion, valor_total=300000, tipo_pedido='Estandar'
        )

        # Stock inicial del material antes de la operación = 50.0
        url = reverse('ventas:crear_abono', args=[pedido.id_pedido])
        data = {
            'monto_abono': '100000',  # Abono parcial
            'metodo_pago': 'Nequi',
            'descripcion': 'Primer pago'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        # Al ser el primer abono, debió llamar a gestionar_inventario('RESTAR')
        # Consumo: cantidad_usada (2.0) * cant_soli (5) = 10 unidades consumidas.
        self.material.refresh_from_db()
        self.assertEqual(self.material.stock_mmtp, 40.0)

<<<<<<< Updated upstream
        # Como es abono parcial, el estado del pedido no debe cambiar a Confirmado aún
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado_ped, 'Carrito')

    def test_finalizar_pedido_completo_con_pago_total(self):
        """Prueba el flujo de pagar el 100% mediante finalizar_pedido actualizando fechas y estados"""
        pedido = Pedido.objects.create(id_clien_fk=self.cliente, estado_ped='Carrito')
        variacion = Variacion.objects.create(talla_var='M', cant_soli=1, color_var='negro')
        Det_valor.objects.create(
            id_ped_fk_detval=pedido, id_prod_fk_detval=self.producto,
            id_var_fk_detval=variacion, valor_total=60000, tipo_pedido='Estandar'
        )

        url = reverse('ventas:finalizar_pedido', args=[pedido.id_pedido])
        data = {
            'tipo_pago': 'total',  # Envía flujo diferente a 'abono'
            'metodo_pago': 'Efectivo'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        pedido.refresh_from_db()
        # Verificaciones de actualización de metadatos del pedido
        self.assertEqual(pedido.estado_ped, 'Confirmado')
        self.assertEqual(pedido.subtotal_ped, Decimal('60000.00'))
        self.assertEqual(pedido.fecha_entrega, timezone.now().date() + timedelta(days=self.producto.dias_produccion))

        # Comprobar la creación automática del abono por el 100%
        abono = Abono.objects.filter(id_pedido_fk_abono=pedido).first()
        self.assertIsNotNone(abono)
        self.assertEqual(abono.monto_abono, Decimal('60000.00'))

    def test_gestionar_pedido_cancelar_devuelve_inventario(self):
        """Asegura que al cancelar un pedido con abonos previos se le devuelvan los insumos al inventario"""
        pedido = Pedido.objects.create(id_clien_fk=self.cliente, estado_ped='Confirmado')
        variacion = Variacion.objects.create(talla_var='L', cant_soli=2, color_var='negro')
        Det_valor.objects.create(
            id_ped_fk_detval=pedido, id_prod_fk_detval=self.producto,
            id_var_fk_detval=variacion, valor_total=120000, tipo_pedido='Estandar'
        )
        # Simulamos que ya poseía un abono registrado
        Abono.objects.create(id_pedido_fk_abono=pedido, monto_abono=60000, metodo_pago='Efectivo')

        # Simulamos stock en 46.0 (imaginando que ya se habían restado 4 unidades correspondientes al pedido)
        self.material.stock_mmtp = 46.0
        self.material.save()

        url = reverse('ventas:gestionar_pedido', args=[pedido.id_pedido])
        response = self.client.post(url, {'accion': 'cancelar'})
        self.assertEqual(response.status_code, 302)

        # El pedido cambia su estado a Cancelado
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado_ped, 'Cancelado')

        # Se debe ejecutar gestionar_inventario('SUMAR'): 46.0 + (2.0 receta * 2 cantidad) = 50.0
        self.material.refresh_from_db()
        self.assertEqual(self.material.stock_mmtp, 50.0)

    def test_gestionar_pedido_entrega_ejecuta_borrado_fisico(self):
        """Valida que la acción 'entregado' realice el borrado físico completo del pedido"""
        pedido = Pedido.objects.create(id_clien_fk=self.cliente, estado_ped='Confirmado')
        
        url = reverse('ventas:gestionar_pedido', args=[pedido.id_pedido])
        response = self.client.post(url, {'accion': 'entregado'})
        self.assertEqual(response.status_code, 302)

        # Se verifica que el registro fue destruido físicamente de la base de datos
        with self.assertRaises(Pedido.DoesNotExist):
            Pedido.objects.get(id_pedido=pedido.id_pedido)

    def test_eliminar_del_carrito_y_borrado_de_variacion(self):
        """Garantiza que eliminar un ítem del carrito remueva también su variación en cascada"""
        pedido = Pedido.objects.create(id_clien_fk=self.cliente, estado_ped='Carrito')
        variacion = Variacion.objects.create(talla_var='S', cant_soli=1, color_var='azul')
        detalle = Det_valor.objects.create(
            id_ped_fk_detval=pedido, id_prod_fk_detval=self.producto,
            id_var_fk_detval=variacion, valor_total=60000, tipo_pedido='Estandar'
        )

        url = reverse('ventas:eliminar_del_carrito', args=[detalle.id_det_valor])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        # Tanto el detalle como la variación asociada no deben existir
        with self.assertRaises(Det_valor.DoesNotExist):
            Det_valor.objects.get(id_det_valor=detalle.id_det_valor)

        with self.assertRaises(Variacion.DoesNotExist):
            Variacion.objects.get(id_var=variacion.id_var)
=======
        # No debe existir un segundo producto guardado con el nombre "Clon de Hodie"
        self.assertFalse(Producto.objects.filter(nom_produc='Clon de Hodie').exists())
>>>>>>> Stashed changes
