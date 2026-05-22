from django.test import TestCase
<<<<<<< Updated upstream

# Create your tests here.
=======
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from decimal import Decimal
import json

# Importamos los modelos reales de tu aplicación
from .models import Proveedor, Movimiento_matp, Estampado, PedidoPersonalizado
from ventas.models import Producto, Cliente  # Necesarios para la prueba del Carrito/3D

class InventarioViewsTest(TestCase):

    def setUp(self):
        # 1. Crear datos base de prueba para las relaciones
        self.proveedor = Proveedor.objects.create(
            nom_provee='Proveedor Textil S.A.S',
            fech_ingre=timezone.now().date().isoformat(),
            num_tel='3101234567'
        )

        self.materia_prima = Movimiento_matp.objects.create(
            tipo_mmtp='ENTRADA',
            color_mmtp='#FFFFFF',
            fecha_mmtp=timezone.now().date().isoformat(),
            stock_mmtp=50,
            mat_mmtp='Algodón Perchado',
            id_proveedor_fk=self.proveedor
        )

        self.estampado = Estampado.objects.create(
            nombre_estamp='Calavera Aesthetic',
            costo_adi=Decimal('15000.00'),
            tipo_estamp='Frente',
            imagen_hash='hash_falso_de_prueba_123'
        )

        # Necesarios para la prueba del diseño 3D
        self.producto = Producto.objects.create(
            id_produc=1,
            nombre='Camiseta Oversize',
            precio=Decimal('45000.00')
        )
        
        # Simulamos un usuario cliente en sesión
        self.cliente = Cliente.objects.create(
            id_clien=1,
            nombre_completo='Juan Test'
        )

    # ==========================================
    # PRUEBAS DE PROVEEDORES
    # ==========================================
    
    def test_lista_proveedores_view(self):
        """Verifica que la vista cargue el catálogo de proveedores correctamente"""
        response = self.client.get(reverse('inventario:lista_provee'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventario/proveedor/lista.html')
        self.assertIn('proveedor', response.context)

    def test_registrar_proveedor_exitoso(self):
        """Prueba la creación manual de un proveedor mediante formulario POST"""
        response = self.client.post(
            reverse('inventario:lista_provee'),
            {
                'nom_provee': 'Distribuidora de Telas',
                'fech_ingre': timezone.now().date().isoformat(),
                'num_tel': '3159876543'
            }
        )
        # Verifica redirección exitosa tras guardar
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Proveedor.objects.count(), 2)

    def test_eliminar_proveedor(self):
        """Prueba que el borrado por ID funcione en la base de datos"""
        response = self.client.get(
            reverse('inventario:eliminar_provee', args=[self.proveedor.id_provee])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Proveedor.objects.count(), 0)

    # ==========================================
    # PRUEBAS DE MATERIA PRIMA (MOVIMIENTOS)
    # ==========================================

    def test_lista_materia_prima_view(self):
        """Verifica que se listen los movimientos y cargue el modal de historial"""
        response = self.client.get(reverse('inventario:lista_mmtp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventario/movimiento_matp/lista.html')
        self.assertIn('mmtp', response.context)

    def test_registrar_materia_prima_control_negativos(self):
        """Prueba tu corrección de lógica: si meten stock negativo debe volverse 0"""
        response = self.client.post(
            reverse('inventario:lista_mmtp'),
            {
                'tipo_mmtp': 'ENTRADA',
                'color_mmtp': '#000000',
                'fecha_mmtp': timezone.now().date().isoformat(),
                'stock_mmtp': '-15',  # Valor negativo erróneo
                'mat_mmtp': 'Lino',
                'id_proveedor_fk': self.proveedor.id_provee
            }
        )
        self.assertEqual(response.status_code, 302)
        # Buscamos el movimiento creado para ver si la lógica lo forzó a 0
        movimiento_creado = Movimiento_matp.objects.get(mat_mmtp='Lino')
        self.assertEqual(movimiento_creado.stock_mmtp, 0)

    # ==========================================
    # PRUEBAS DE ESTAMPADOS (DUPLICADOS POR HASH)
    # ==========================================

    def test_lista_estampados_busqueda(self):
        """Prueba que la consulta de búsqueda por parámetros de texto responda bien"""
        response = self.client.get(reverse('inventario:lista_estampado'), {'q': 'Aesthetic'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('estampados', response.context)

    def test_evitar_estampado_duplicado(self):
        """Prueba que el sistema rechace un estampado si el hash de imagen ya existe"""
        # Simulamos un archivo de imagen cargado
        archivo_imagen = SimpleUploadedFile(
            "logo_test.png", 
            b"contenido_binario_falso", 
            content_type="image/png"
        )
        
        # Intentamos registrar un estampado duplicando a propósito el hash existente
        # Nota: En tu vista real, si encuentra el hash devuelve un render con error directo
        # en lugar de redirigir.
        response = self.client.post(
            reverse('inventario:lista_estampado'),
            {
                'nombre_estamp': 'Calavera Aesthetic Copia',
                'costo_adi': '15000',
                'tipo_estamp': 'Frente',
                'archivo_imagen': archivo_imagen
            }
        )
        
        # Debe responder con éxito 200 pintando la alerta en la misma plantilla, sin duplicar en DB
        self.assertEqual(response.status_code, 200)
        self.assertIn('¡Atención! Este diseño ya existe.', response.context.get('error', ''))

    # ==========================================
    # PRUEBAS DEL MÓDULO DE PERSONALIZACIÓN 3D
    # ==========================================

    def test_guardar_diseno_3d_metodo_invalido(self):
        """Verifica que si la petición al diseño no es POST, lance error 405"""
        response = self.client.get(reverse('inventario:guardar_diseno_3d'))
        self.assertEqual(response.status_code, 405)

    def test_guardar_diseno_3d_sin_sesion(self):
        """Valida que si no hay un cliente en sesión responda con error 401"""
        # Enviamos una estructura JSON vacía imitando la petición Fetch de JavaScript
        response = self.client.post(
            reverse('inventario:guardar_diseno_3d'),
            json.dumps({}),
            content_type='application/json'
        )
        # Al no mockear la sesión del cliente, tu función `obtener_cliente_actual` dará None
        self.assertEqual(response.status_code, 401)
>>>>>>> Stashed changes
