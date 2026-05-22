<<<<<<< Updated upstream
from django.test import TestCase

# Create your tests here.
=======
import hashlib
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils import timezone

from .models import Pedido, Producto, Variacion, Det_valor, Abono, Cliente, Rol, Usuario, Det_mov_matp
from inventario.models import Estampado, Movimiento_matp

class VentasYPedidosViewsTestCase(TestCase):

    def setUp(self):
        """
        Configuración inicial del entorno de pruebas.
        Crea roles, usuarios, clientes, productos, estampados e insumos.
        """
        self.client = Client()

        # 1. Creación de Roles y Usuarios de control
        self.rol_cliente = Rol.objects.create(nom_rol='Cliente')
        self.rol_admin = Rol.objects.create(nom_rol='Administrador')

        self.user_cliente = Usuario.objects.create(
            username='comprador_luxy',
            contrasena='hash_fake_123',
            id_rol_fk=self.rol_cliente
        )
        self.user_admin = Usuario.objects.create(
            username='admin_ventas',
            contrasena='hash_fake_admin',
            id_rol_fk=self.rol_admin
        )

        # 2. Creación del perfil del Cliente asociado al usuario
        self.cliente = Cliente.objects.create(
            id_usuario_fk=self.user_cliente,
            nom_clien='Esteban Quito',
            tel_clien='3157778899',
            correo_clien='esteban@correo.com'
        )

        # 3. Creación de insumos de Materia Prima en Inventario para la receta
        self.material_insumo = Movimiento_matp.objects.create(
            mat_mmtp='Algodón Perchado',
            color_mmtp='Negro',
            stock_mmtp=100,  # Inicial con 100 unidades en stock
            tipo_mmtp='ENTRADA'
        )

        # 4. Creación de un Producto estándar
        self.producto = Producto.objects.create(
            nom_produc='Hodie Oversize Luxy',
            gen_produc='Unisex',
            desc_produc='Hodie premium de alta costura.',
            categoria_produc='Prendas Superiores',
            estado_produc='Activo',
            precio=Decimal('85000.00'),
            dias_produccion=8,
            imagen_hash='abc123hashoriginal'
        )

        # Asociar la receta al producto (Usa 2 unidades de Algodón Negro por prenda)
        self.receta = Det_mov_matp.objects.create(
            producto=self.producto,
            materia_prima=self.material_insumo,
            cantidad_usada=2
        )

        # 5. Creación de un Estampado para personalizaciones
        self.estampado = Estampado.objects.create(
            nom_estam='Cyberpunk Glow 3D',
            costo_adi=Decimal('15000.00')
        )

    # ================================================================
    # 🛒 PRUEBAS DEL CARRITO Y VARIACIONES (PERSONALIZACIÓN)
    # ================================================================

    def test_crear_variacion_personalizada_calcula_total(self):
        """
        Valida que al crear una variación con estampado, el Det_valor
        calcule el total aplicando la fórmula: (Precio + Costo Adicional) * Cantidad.
        """
        # Iniciar sesión como Cliente
        session = self.client.session
        session['usuario_id'] = self.user_cliente.id_usuario
        session.save()

        # Crear un pedido base en estado 'Carrito'
        pedido_cart = Pedido.objects.create(
            id_clien_fk=self.cliente,
            estado_ped='Carrito',
            subtotal_ped=0,
            valor_ped=0
        )

        data_post = {
            'talla_var': 'M',
            'cant_soli': '2',
            'color_var': 'Negro',
            'mat_var': 'Algodón',
            'id_estam': self.estampado.id_estam
        }

        url = reverse('ventas:crear_variacion', args=[self.producto.id_produc, pedido_cart.id_pedido])
        response = self.client.post(url, data=data_post)

        # Debe redirigir al carrito tras añadir el artículo
        self.assertRedirects(response, reverse('ventas:ver_carrito'))

        # Validaciones de Base de Datos
        variacion_creada = Variacion.objects.get(talla_var='M', color_var='Negro')
        detalle_creado = Det_valor.objects.get(id_ped_fk_detval=pedido_cart)

        # Formula: (85,000 precio + 15,000 estampado) * 2 cant = 200,000
        self.assertEqual(variacion_creada.costo_var, self.estampado.costo_adi)
        self.assertEqual(detalle_creado.valor_total, Decimal('200000.00'))
        self.assertEqual(detalle_creado.tipo_pedido, 'Personalizado')

    def test_producto_sin_personalizar_crea_carrito_automatico(self):
        """
        Valida que al añadir una prenda estándar por POST, el sistema
        cree el Pedido en estado 'Carrito' si el usuario no tenía uno activo.
        """
        session = self.client.session
        session['usuario_id'] = self.user_cliente.id_usuario
        session.save()

        data_post = {
            'talla': 'L',
            'color': 'gris',
            'cantidad': '3'
        }

        url = reverse('ventas:producto_sin_personalizar', args=[self.producto.id_produc])
        response = self.client.post(url, data=data_post)

        self.assertRedirects(response, reverse('ventas:lista_product'))

        # Comprobar la existencia del pedido 'Carrito' autogenerado
        pedido_auto = Pedido.objects.get(id_clien_fk=self.cliente, estado_ped='Carrito')
        detalle_auto = Det_valor.objects.get(id_ped_fk_detval=pedido_auto)

        # Formula estándar: 85,000 * 3 = 255,000
        self.assertEqual(detalle_auto.valor_total, Decimal('255000.00'))
        self.assertEqual(detalle_auto.tipo_pedido, 'Estandar')

    # ================================================================
    # ⚙️ VALIDACIÓN DE CONTROL DE INVENTARIO (RECETA DE PRODUCCIÓN)
    # ================================================================

    def test_gestionar_inventario_resta_stock_al_finalizar_pedido(self):
        """
        Prueba la función nuclear `gestionar_inventario`. Al procesar un pedido
        de 3 prendas, debe descontar del stock físico (3 prendas * 2 unidades de insumo = 6).
        """
        session = self.client.session
        session['usuario_id'] = self.user_cliente.id_usuario
        session.save()

        # Configurar un pedido con ítems listos en el carrito
        pedido = Pedido.objects.create(id_clien_fk=self.cliente, estado_ped='Carrito')
        var = Variacion.objects.create(talla_var='S', cant_soli=3, color_var='Negro', costo_var=0)
        Det_valor.objects.create(
            id_ped_fk_detval=pedido, id_prod_fk_detval=self.producto,
            id_var_fk_detval=var, valor_total=self.producto.precio * 3, cant=3
        )

        # Ejecutamos el flujo de finalización por 100% pago directo
        data_post = {
            'tipo_pago': 'total',
            'metodo_pago': 'Nequi'
        }
        url = reverse('ventas:finalizar_pedido', args=[pedido.id_pedido])
        self.client.post(url, data=data_post)

        # Refrescar stock de la base de datos
        self.material_insumo.refresh_from_db()
        
        # Stock inicial: 100 -> Menos 6 usados = 94 unidades restantes
        self.assertEqual(self.material_insumo.stock_mmtp, 94)

    # ================================================================
    # 💰 PRUEBAS DEL SISTEMA DE ABONOS Y FINANZAS
    # ================================================================

    def test_crear_abono_excede_saldo_pendiente_arroja_error(self):
        """
        Garantiza la seguridad financiera de Luxy Fashion: Evita que un cliente
        registre un abono mayor al dinero que resta por pagar del pedido.
        """
        session = self.client.session
        session['usuario_id'] = self.user_cliente.id_usuario
        session.save()

        # Pedido de $85.000 pesos colombianos
        pedido = Pedido.objects.create(id_clien_fk=self.cliente, estado_ped='Confirmado')
        var = Variacion.objects.create(talla_var='M', cant_soli=1, color_var='Negro', costo_var=0)
        Det_valor.objects.create(
            id_ped_fk_detval=pedido, id_prod_fk_detval=self.producto,
            id_var_fk_detval=var, valor_total=Decimal('85000.00'), cant=1
        )

        # Intentar abonar $90.000 (Excede el saldo de $85.000)
        data_post = {
            'monto_abono': '90000',
            'metodo_pago': 'Efectivo',
            'descripcion': 'Abono sospechoso'
        }
        url = reverse('ventas:crear_abono', args=[pedido.id_pedido])
        response = self.client.post(url, data=data_post)

        # Comprobar que redirige de nuevo al formulario por el fallo de validación
        self.assertRedirects(response, url)

        # Verificar el mensaje de error personalizado en el request
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("supera el saldo" in str(m) for m in messages))

        # El abono NO debió crearse en la base de datos
        self.assertFalse(Abono.objects.filter(id_pedido_fk_abono=pedido).exists())

    # ================================================================
    # 🛡️ SEGURIDAD DE ARCHIVOS Y DUPLICIDAD (SISTEMA DE HASHING SHA-256)
    # ================================================================

    def test_subir_prenda_duplicada_por_hash_bloquea_registro(self):
        """
        Asegura que el administrador no pueda subir dos veces la misma prenda
        física basándose en la huella SHA-256 del archivo binario.
        """
        # Forzar sesión como administrador
        session = self.client.session
        session['usuario_id'] = self.user_admin.id_usuario
        session['rol'] = 'Administrador'
        session.save()

        # Simulamos un archivo que genera exactamente el mismo hash de control del setUp
        from django.core.files.uploadedfile import SimpleUploadedFile
        imagen_duplicada = SimpleUploadedFile(
            "prenda_nueva.png", 
            b"contenido_binario_de_ejemplo_de_imagen", 
            content_type="image/png"
        )

        # Calculamos manualmente el hash para inyectarlo en la simulación del test
        hasher = hashlib.sha256()
        hasher.update(b"contenido_binario_de_ejemplo_de_imagen")
        hash_calculado = hasher.hexdigest()

        # Modificamos temporalmente el hash de nuestro producto existente para forzar la coincidencia
        self.producto.imagen_hash = hash_calculado
        self.producto.save()

        data_post = {
            'nom_produc': 'Clon de Hodie',
            'gen_produc': 'Hombre',
            'desc_produc': 'Intento de duplicación',
            'cat_produc': 'Prendas Superiores',
            'estado_produc': 'Activo',
            'precio': '85000',
            'dias_produccion': '10',
            'imagen_produc': imagen_duplicada,
            'material_ids[]': [self.material_insumo.id_mmtp],
            'cantidades[]': [2]
        }

        url = reverse('ventas:lista_producto_admin')
        response = self.client.post(url, data=data_post)

        # Debe responder con el render de la plantilla mostrando el error en pantalla
        self.assertEqual(response.status_code, 200)
        self.assertIn('ERROR: Esta prenda ya ha sido subida anteriormente.', response.content.decode('utf-8'))

        # No debe existir un segundo producto guardado con el nombre "Clon de Hodie"
        self.assertFalse(Producto.objects.filter(nom_produc='Clon de Hodie').exists())
>>>>>>> Stashed changes
