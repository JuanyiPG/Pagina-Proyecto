import hashlib
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.hashers import make_password
from .models import Rol, Usuario, Empleado, Cliente

class UsuariosCustomAuthTest(TestCase):

    def setUp(self):
        """Configuración de roles y credenciales iniciales en la base de datos."""
        # 1. Creamos los roles obligatorios del sistema
        self.rol_admin = Rol.objects.create(nom_rol='Administrador')
        self.rol_empleado = Rol.objects.create(nom_rol='Empleado')
        self.rol_cliente = Rol.objects.create(nom_rol='Cliente')

        # 2. Creamos un usuario administrador de prueba (Clave: admin123)
        self.usuario_admin = Usuario.objects.create(
            username='admin_luxy',
            contrasena=make_password('admin123'),
            id_rol_fk=self.rol_admin
        )

        # 3. Creamos un usuario cliente de prueba (Clave: cliente123)
        self.usuario_cliente = Usuario.objects.create(
            username='carlos_cliente',
            contrasena=make_password('cliente123'),
            id_rol_fk=self.rol_cliente
        )

        # 4. Imagen de prueba simulada en memoria para fotos de perfil
        self.foto_test = SimpleUploadedFile(
            name='avatar.png',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00',
            content_type='image/png'
        )

    def simular_login_session(self, usuario, nombre_rol):
        """Método auxiliar para bypass de tus decoradores custom (@solo_personal)"""
        session = self.client.session
        session['usuario_id'] = usuario.id_usuario
        session['username'] = usuario.username
        session['rol'] = nombre_rol
        session.save()

    # --- 1. PRUEBAS DE SEGURIDAD Y DECORADORES ---

    def test_decorador_login_requerido_bloquea_anonimo(self):
        """Verifica que si no hay sesión iniciada, redirija al login."""
        response = self.client.get(reverse('usuarios:lista_roles'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('usuarios:login'))

    def test_decorador_solo_personal_bloquea_clientes(self):
        """Verifica que un Rol 'Cliente' no pueda entrar al CRUD de roles."""
        self.simular_login_session(self.usuario_cliente, 'Cliente')
        response = self.client.get(reverse('usuarios:lista_roles'))
        self.assertEqual(response.status_code, 302)  # Redirige al index por falta de permisos

    # --- 2. PRUEBAS DEL FLUJO DE AUTENTICACIÓN (LOGIN/LOGOUT) ---

    def test_login_exitoso_post(self):
        """Verifica el inicio de sesión correcto y la creación de variables en request.session."""
        response = self.client.post(reverse('usuarios:login'), {
            'username': 'admin_luxy',
            'password': 'admin123'
        })
        # Al ser Administrador, tu vista redirige a 'estadisticas_admin'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('usuarios:estadisticas_admin'))
        # Comprobamos las variables que inyectas con request.session.flush()
        self.assertEqual(self.client.session['usuario_id'], self.usuario_admin.id_usuario)
        self.assertEqual(self.client.session['rol'], 'Administrador')

    def test_login_fallido_contrasena_erronea(self):
        """Verifica el rechazo de credenciales falsas sin romper la sesión."""
        response = self.client.post(reverse('usuarios:login'), {
            'username': 'admin_luxy',
            'password': 'clave_incorrecta_sena'
        })
        self.assertEqual(response.status_code, 200)  # Se queda en la misma plantilla de login
        self.assertNotIn('usuario_id', self.client.session)

    def test_logout_limpia_sesion(self):
        """Verifica que logout_view borre todo rastro de la sesión."""
        self.simular_login_session(self.usuario_admin, 'Administrador')
        response = self.client.get(reverse('usuarios:logout'))
        self.assertEqual(response.status_code, 302)
        # El diccionario de sesión debe quedar vacío tras el flush()
        self.assertNotIn('usuario_id', self.client.session)

    # --- 3. PRUEBAS DE REGRESIÓN: REGLAS DE NEGOCIO EN EMPLEADOS ---

    def test_crear_empleado_menor_de_edad_invalido(self):
        """PRUEBA DE REGRESIÓN: Comprueba que bloquee el registro si es menor de 18 años."""
        self.simular_login_session(self.usuario_admin, 'Administrador')
        
        response = self.client.post(reverse('usuarios:crear_empleado'), {
            'num_ident': '10023456',
            'username': 'nuevo_menor',
            'contrasena': 'empleado123',
            'id_rol': self.rol_empleado.id_rol,
            'nom_emple': 'Juanito Perez',
            'fecha_naci_emple': '2015-05-20',  # Nació en 2015, tiene menos de 18 en 2026
            'fecha_ing_emple': '2026-05-20',
            'salari_emple': '1300000',
            'estado_emple': 'Activo'
        })
        
        # Debe rebotar impidiendo que se guarde el registro en la base de datos
        self.assertFalse(Empleado.objects.filter(num_ident='10023456').exists())

    def test_crear_empleado_fecha_ingreso_futura_error(self):
        """PRUEBA DE REGRESIÓN: Bloquea si la fecha de vinculación es posterior a hoy."""
        self.simular_login_session(self.usuario_admin, 'Administrador')
        
        response = self.client.post(reverse('usuarios:crear_empleado'), {
            'num_ident': '998877',
            'username': 'empleado_futuro',
            'contrasena': 'empleado123',
            'id_rol': self.rol_empleado.id_rol,
            'nom_emple': 'Felipe',
            'fecha_naci_emple': '1995-05-20',
            'fecha_ing_emple': '2030-12-31',  # Fecha en el futuro lejano
            'salari_emple': '1500000',
            'estado_emple': 'Activo'
        })
        self.assertFalse(Empleado.objects.filter(num_ident='998877').exists())

    def test_evitar_empleado_foto_duplicada_SHA256(self):
        """PRUEBA DE INTEGRIDAD: Verifica el bloqueo criptográfico de fotos repetidas."""
        self.simular_login_session(self.usuario_admin, 'Administrador')
        
        # Calculamos el hash de nuestra foto de prueba tal como lo hace tu views.py
        self.foto_test.seek(0)
        content = self.foto_test.read()
        hash_calculado = hashlib.sha256(content).hexdigest()
        self.foto_test.seek(0)

        # Registramos un primer empleado con esa foto directamente
        usuario_emp1 = Usuario.objects.create(username='emp1', contrasena='1', id_rol_fk=self.rol_empleado)
        Empleado.objects.create(
            num_ident='1111', nom_emple='Emp Uno', fecha_naci_emple='1990-01-01',
            fecha_ing_emple='2025-01-01', hash_foto=hash_calculado, id_usuario_fk=usuario_emp1
        )

        # Intentamos registrar un SEGUNDO empleado mandando el mismo archivo por POST
        self.foto_test.seek(0)
        response = self.client.post(reverse('usuarios:crear_empleado'), {
            'num_ident': '2222',
            'username': 'emp2',
            'contrasena': '123',
            'id_rol': self.rol_empleado.id_rol,
            'nom_emple': 'Emp Dos',
            'fecha_naci_emple': '1992-01-01',
            'fecha_ing_emple': '2025-05-01',
            'foto_perfil': self.foto_test
        })

        # Comprobamos que el segundo empleado NO fue creado debido al filtro por hash_foto
        self.assertEqual(Empleado.objects.count(), 1)