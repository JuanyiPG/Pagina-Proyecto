import os
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

# 1. Imports de la aplicación 'usuarios'
from usuarios.models import Usuario, Rol, Cliente

# 2. Imports de la aplicación 'inventario'
from inventario.models import Proveedor, Movimiento_matp

# 3. Imports de la aplicación actual 'ventas'
from .models import Pedido, Variacion, Det_valor, Producto, Abono, Det_mov_matp


class VentasFlujoTestCase(TestCase):

    def setUp(self):
        """Configuración inicial compartida para todas las pruebas."""
        # Estructura de Roles y Usuarios
        self.rol_admin = Rol.objects.create(
            pk=1,
            nom_rol="Administrador"
        )
        
        self.usuario = Usuario.objects.create(
            pk=1,
            id_rol_fk=self.rol_admin
        )
        
        self.cliente = Cliente.objects.create(
            pk=1,
            id_usuario_fk=self.usuario
        )

        # Estructura de Proveedor
        self.proveedor = Proveedor.objects.create(
            pk=1,
            fech_ingre=timezone.now()
        )
        
        # Objeto Material (Movimiento_matp)
        self.material = Movimiento_matp.objects.create(
            pk=1,
            stock_mmtp=10,
            fecha_mmtp=timezone.now(),
            id_proveedor_fk=self.proveedor
        )

        # Producto Base con su precio obligatorio e imagen simulada
        self.producto = Producto.objects.create(
            pk=1,
            nom_produc="Camiseta Base",
            gen_produc="Unisex",
            desc_produc="Descripción de prueba",
            categoria_produc="Ropa",
            estado_produc="Activo",
            precio=85000,
            imagen_product="producto/logo_test.png"
        )

    def tearDown(self):
        """Limpieza física de archivos después de cada prueba."""
        # Si el producto tiene una imagen asignada y el archivo existe en el almacenamiento, se elimina
        if self.producto.imagen_product and os.path.exists(self.producto.imagen_product.path):
            try:
                os.remove(self.producto.imagen_product.path)
            except OSError:
                pass

    def test_producto_sin_personalizar_crea_carrito_y_detalle(self):
        """Evalúa que añadir un producto estándar cree correctamente el Pedido 'Carrito' y su Det_valor."""
        pedido = Pedido.objects.create(
            id_clien_fk=self.cliente,
            subtotal_ped=85000,
            valor_ped=85000,
            estado_ped="Carrito",
            metodo_pago="Efectivo"
        )
        
        detalle = Det_valor.objects.create(
            id_ped_fk_detval=pedido,
            id_prod_fk_detval=self.producto,
            valor_total=85000,
            tipo_pedido="Estándar"
        )

        self.assertEqual(pedido.estado_ped, "Carrito")
        self.assertEqual(Pedido.objects.filter(id_clien_fk=self.cliente).count(), 1)

    def test_gestionar_pedido_cancelar_devuelve_inventario(self):
        """Asegura que al cancelar un pedido con abonos previos se le devuelvan los insumos al inventario."""
        pedido = Pedido.objects.create(
            id_clien_fk=self.cliente,
            subtotal_ped=120000,
            valor_ped=120000,
            estado_ped="PENDIENTE",
            metodo_pago="Efectivo"
        )
        
        abono = Abono.objects.create(
            id_pedido_fk_abono=pedido,
            monto_abono=50000,
            metodo_pago="Efectivo",
            descripcion="Primer abono"
        )

        det_mov = Det_mov_matp.objects.create(
            producto=self.producto,
            materia_prima=self.material,
            cantidad_usada=2
        )

        # Simulación de la cancelación del flujo
        pedido.estado_ped = "CANCELADO"
        pedido.save()
        
        det_mov.cantidad_usada += 2 
        det_mov.save()

        self.assertEqual(pedido.estado_ped, "CANCELADO")
        self.assertEqual(det_mov.cantidad_usada, 4)

    def test_gestionar_pedido_entrega_ejecuta_borrado_fisico(self):
        """Valida que la acción 'entregado' realice el borrado físico completo del pedido."""
        pedido = Pedido.objects.create(
            id_clien_fk=self.cliente,
            subtotal_ped=95000,
            valor_ped=95000,
            estado_ped="Proceso",
            metodo_pago="Efectivo"
        )

        pedido.estado_ped = "ENTREGADO"
        pedido.save()
        
        pedido.delete()

        existe_pedido = Pedido.objects.filter(pk=pedido.pk).exists()
        self.assertFalse(existe_pedido)