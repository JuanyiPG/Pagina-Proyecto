import datetime
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Proveedor, Movimiento_matp, Estampado
from ventas.models import Producto

class InventarioCompletoTest(TestCase):

    def setUp(self):
        """
        Configuración inicial: Creamos datos de prueba en la base de datos temporal
        para que las vistas tengan información con la cual trabajar.
        """
        # 1. Proveedor de prueba
        self.proveedor = Proveedor.objects.create(
            nom_provee="Textiles del Tolima",
            fech_ingre="2026-01-15",
            num_tel="3201234567"
        )

        # 2. Materia prima asociada al proveedor
        self.movimiento = Movimiento_matp.objects.create(
            tipo_mmtp="ENTRADA",
            color_mmtp="#FFFFFF",
            fecha_mmtp="2026-05-20",
            stock_mmtp=50,
            mat_mmtp="Algodón Perchado",
            id_proveedor_fk=self.proveedor
        )

        # 3. Producto base en catálogo (Necesario para la vista del modelo 3D)
        self.producto = Producto.objects.create(
            id_produc=1,
            nom_produc="Camiseta Oversize",
            precio=40000,
            stock=20
        )

        # 4. Estampado de prueba con una imagen simulada en memoria
        self.imagen_prueba = SimpleUploadedFile(
            name='test_logo.png',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b',
            content_type='image/png'
        )
        self.estampado = Estampado.objects.create(
            nombre_estamp="Logo Cyberpunk",
            costo_adi=5000.00,
            tipo_estamp="Frente",
            imagen_estamp=self.imagen_prueba,
            imagen_hash="hash_falso_de_prueba_123"
        )

    # --- PRUEBAS DE PROVEEDORES ---

    def test_vista_lista_proveedores(self):
        """Verifica que la página de listar proveedores cargue y muestre los datos."""
        response = self.client.get(reverse('inventario:lista_provee'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventario/proveedor/lista.html")
        self.assertIn('proveedor', response.context)

    def test_crear_proveedor_POST(self):
        """Verifica que el formulario guarde un proveedor válido y redirija."""
        response = self.client.post(reverse('inventario:lista_provee'), {
            'nom_provee': 'Botones y Cremalleras SAS',
            'fech_ingre': '2026-05-21',
            'num_tel': '3159876543'
        })
        self.assertEqual(Proveedor.objects.count(), 2)
        self.assertEqual(response.status_code, 302)  # Redirección exitosa

    # --- PRUEBAS DE MOVIMIENTOS MATP (MATERIA PRIMA) ---

    def test_vista_lista_materia_prima(self):
        """Verifica el acceso a la lista de insumos y que cargue el historial calculado."""
        response = self.client.get(reverse('inventario:lista_mmtp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventario/movimiento_matp/lista.html")

    def test_control_stock_negativo_POST(self):
        """PRUEBA DE REGRESIÓN: Verifica tu lógica para evitar stock negativo."""
        response = self.client.post(reverse('inventario:lista_mmtp'), {
            'tipo_mmtp': 'ENTRADA',
            'color_mmtp': '#FF0000',
            'fecha_mmtp': '2026-05-21',
            'stock_mmtp': '-10',  # Mandamos un número negativo a propósito
            'mat_mmtp': 'Lino',
            'id_proveedor_fk': self.proveedor.id_provee
        })
        # Buscamos el material que se acaba de crear
        nuevo_material = Movimiento_matp.objects.get(mat_mmtp='Lino')
        # Tu backend debe haberlo transformado en 0 automáticamente
        self.assertEqual(nuevo_material.stock_mmtp, 0)

    # --- PRUEBAS DE ESTAMPADOS ---

    def test_vista_lista_estampados(self):
        """Verifica que cargue la galería de diseños correctamente."""
        response = self.client.get(reverse('inventario:lista_estampado'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventario/estampado/lista.html")

    def test_evitar_estampado_duplicado_POST(self):
        """PRUEBA DE SEGURIDAD: Comprueba que el validador por HASH bloquee imágenes idénticas."""
        # Intentamos subir exactamente la misma imagen que configuramos en el setUp
        imagen_duplicada = SimpleUploadedFile(
            name='test_logo.png',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b',
            content_type='image/png'
        )
        
        # Simulamos que el usuario llena el formulario con el mismo archivo
        response = self.client.post(reverse('inventario:lista_estampado'), {
            'nombre_estamp': 'Clon Logo',
            'costo_adi': '5000',
            'tipo_estamp': 'Frente',
            'archivo_imagen': imagen_duplicada
        })
        
        # Como el código calcula el hash SHA-256 y ve que ya existe, no debe añadir otro registro
        self.assertEqual(Estampado.objects.count(), 1) 

    # --- PRUEBAS DEL VISOR 3D ---

    def test_vista_modelo_3d(self):
        """Verifica que el entorno tridimensional enlace bien el producto y los estampados."""
        response = self.client.get(reverse('inventario:modelo', kwargs={'producto_id': self.producto.id_produc}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventario/modelo/index.html')
        self.assertEqual(response.context['producto'], self.producto)