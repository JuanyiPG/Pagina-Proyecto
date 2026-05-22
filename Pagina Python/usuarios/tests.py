<<<<<<< Updated upstream
from django.test import TestCase

# Create your tests here.
=======
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.hashers import check_password
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from .models import Rol, Usuario, Empleado, Cliente

class UsuariosYEmpleadosViewsTestCase(TestCase):

    def setUp(self):
        """
        Configuración inicial para las pruebas.
        Se crean los roles básicos y usuarios de prueba.
        """
        self.client = Client()
        
        # 1. Creación de Roles necesarios
        self.rol_admin = Rol.objects.create(nom_rol='Administrador')
        self.rol_empleado = Rol.objects.create(nom_rol='Empleado')
        self.rol_cliente = Rol.objects.create(nom_rol='Cliente')

        # 2. Creación de Usuarios con contraseñas encriptadas
        # (Se usa una clave genérica para la simulación de login)
        from django.contrib.auth.hashers import make_password
        
        self.user_admin = Usuario.objects.create(
            username='admin_test',
            contrasena=make_password('admin123'),
            id_rol_fk=self.rol_admin
        )
        
        self.user_empleado = Usuario.objects.create(
            username='empleado_test',
            contrasena=make_password('empleado123'),
            id_rol_fk=self.rol_empleado
        )

        self.user_cliente = Usuario.objects.create(
            username='cliente_test',
            contrasena=make_password('cliente123'),
            id_rol_fk=self.rol_cliente
        )

    # ================================================================
    # 🛡️ PRUEBAS DE DECORADORES Y SEGURIDAD
    # ================================================================

    def test_decorador_login_requerido(self):
        """
        Valida que si un usuario anónimo intenta acceder a una ruta protegida
        sea redirigido al login y reciba un mensaje informativo.
        """
        response = self.client.get(reverse('usuarios:lista_roles'))
        self.assertRedirects(response, reverse('usuarios:login'))
        
        # Verificar mensaje de advertencia de sesión
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Debes iniciar sesión" in str(m) for m in messages))

    def test_decorador_solo_personal_bloquea_cliente(self):
        """
        Valida que un usuario con rol 'Cliente' no pueda ingresar a rutas de personal
        (como lista_empleados) y sea redirigido al index con una advertencia.
        """
        # Forzar sesión como Cliente
        session = self.client.session
        session['usuario_id'] = self.user_cliente.id_usuario
        session['username'] = self.user_cliente.username
        session['rol'] = self.user_cliente.id_rol_fk.nom_rol
        session.save()

        response = self.client.get(reverse('usuarios:lista_empleados'))
        self.assertRedirects(response, reverse('index'))
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("No tienes permisos" in str(m) for m in messages))

    def test_decorador_solo_personal_permite_admin_y_empleado(self):
        """
        Asegura que tanto 'Administrador' como 'Empleado' (y 'empleado' en minúscula)
        puedan pasar el decorador exitosamente sin redirecciones forzadas al index.
        """
        # Probar con Administrador
        session = self.client.session
        session['usuario_id'] = self.user_admin.id_usuario
        session['username'] = self.user_admin.username
        session['rol'] = 'Administrador'
        session.save()
        response = self.client.get(reverse('usuarios:lista_empleados'))
        self.assertEqual(response.status_code, 200)

        # Probar con Empleado (minúscula como lo soporta tu lista de validaciones)
        session['rol'] = 'empleado'
        session.save()
        response = self.client.get(reverse('usuarios:lista_empleados'))
        self.assertEqual(response.status_code, 200)

    # ================================================================
    # 👷 PRUEBAS DE CREACIÓN DE EMPLEADOS Y TRANSACCIONES
    # ================================================================

    def test_crear_empleado_exitoso_y_hashing(self):
        """
        Valida el flujo exitoso de creación de un empleado junto con su usuario,
        y comprueba que la contraseña se guarde encriptada (make_password).
        """
        # Loguearse como administrador para tener permisos
        session = self.client.session
        session['usuario_id'] = self.user_admin.id_usuario
        session['rol'] = 'Administrador'
        session.save()

        hoy = date.today()
        f_nac = (hoy - timedelta(days=25*365.25)).strftime('%Y-%m-%d') # 25 años de edad
        f_ing = hoy.strftime('%Y-%m-%d')

        data_post = {
            'num_ident': '10203040',
            'username': 'nuevo_empleado_dev',
            'contrasena': 'securepass123',
            'id_rol': self.rol_empleado.id_rol,
            'fecha_naci_emple': f_nac,
            'fecha_ing_emple': f_ing,
            'nom_emple': 'Juan Perez',
            'tel_emple': '3001234567',
            'correo_emple': 'juan@luxy.com',
            'dir_emple': 'Calle 10 #20-30',
            'rh_emple': 'O+',
            'tipo_ident': 'CC',
            'salari_emple': '1500000',
            'estado_emple': 'Activo'
        }

        response = self.client.post(reverse('usuarios:crear_empleado'), data=data_post)
        
        # Debe redirigir de vuelta a la lista de empleados
        self.assertRedirects(response, reverse('usuarios:lista_empleados'))

        # Verificar persistencia en base de datos
        usuario_creado = Usuario.objects.get(username='nuevo_empleado_dev')
        empleado_creado = Empleado.objects.get(num_ident='10203040')

        self.assertEqual(empleado_creado.id_usuario_fk, usuario_creado)
        # Verificar el candado de encriptación
        self.assertTrue(check_password('securepass123', usuario_creado.contrasena))

    def test_crear_empleado_rollback_por_usuario_duplicado(self):
        """
        Valida que si el nombre de usuario ya existe en el sistema,
        la transacción falle impidiendo la creación del Empleado (Atomicidad).
        """
        session = self.client.session
        session['usuario_id'] = self.user_admin.id_usuario
        session['rol'] = 'Administrador'
        session.save()

        # 'admin_test' ya existe en el setUp
        data_post = {
            'num_ident': '9999999',
            'username': 'admin_test', 
            'contrasena': 'clave789',
            'fecha_naci_emple': '1995-05-15',
            'fecha_ing_emple': '2026-01-01',
            'nom_emple': 'Intruso Lógico'
        }

        response = self.client.post(reverse('usuarios:crear_empleado'), data=data_post)
        
        # Validar que NO se haya guardado el empleado con esa cédula por el error preventivo
        empleado_existe = Empleado.objects.filter(num_ident='9999999').exists()
        self.assertFalse(empleado_existe)

    # ================================================================
    # 📅 PRUEBAS DE VALIDACIONES DE REGLAS DE NEGOCIO (FECHAS)
    # ================================================================

    def test_validacion_empleado_menor_de_edad(self):
        """
        Prueba que el sistema rechace el registro de empleados menores de 18 años
        con el mensaje de error correspondiente.
        """
        session = self.client.session
        session['usuario_id'] = self.user_admin.id_usuario
        session['rol'] = 'Administrador'
        session.save()

        hoy = date.today()
        # Nació hace 15 años (menor de edad)
        f_nac_menor = (hoy - timedelta(days=15*365.25)).strftime('%Y-%m-%d')

        data_post = {
            'num_ident': '1111222',
            'username': 'menor_edad_user',
            'contrasena': 'pass123',
            'fecha_naci_emple': f_nac_menor,
            'fecha_ing_emple': hoy.strftime('%Y-%m-%d'),
            'nom_emple': 'Carlos Junior'
        }

        response = self.client.post(reverse('usuarios:crear_empleado'), data=data_post)
        messages = list(get_messages(response.wsgi_request))
        
        # Validar que arroje tu mensaje exacto del backend
        self.assertTrue(any("El empleado debe ser mayor de edad (mínimo 18 años)" in str(m) for m in messages))
        self.assertFalse(Empleado.objects.filter(num_ident='1111222').exists())

    def test_validacion_fecha_ingreso_futura_y_limite_tres_meses(self):
        """
        Valida que la fecha de ingreso no pueda ser una fecha futura
        ni mayor a los 3 meses estipulados hacia atrás.
        """
        session = self.client.session
        session['usuario_id'] = self.user_admin.id_usuario
        session['rol'] = 'Administrador'
        session.save()

        hoy = date.today()
        f_nac_valida = (hoy - timedelta(days=30*365.25)).strftime('%Y-%m-%d')
        f_ing_futura = (hoy + timedelta(days=5)).strftime('%Y-%m-%d')

        # Escenario A: Fecha Futura
        data_post_futura = {
            'num_ident': '555555',
            'username': 'user_futuro',
            'contrasena': 'pass123',
            'fecha_naci_emple': f_nac_valida,
            'fecha_ing_emple': f_ing_futura,
            'nom_emple': 'Test Futuro'
        }
        response = self.client.post(reverse('usuarios:crear_empleado'), data=data_post_futura)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("La fecha de ingreso no puede ser una fecha futura" in str(m) for m in messages))

        # Escenario B: Mayor a 3 meses atrás (ej: 120 días atrás)
        f_ing_antigua = (hoy - timedelta(days=120)).strftime('%Y-%m-%d')
        data_post_antigua = {
            'num_ident': '666666',
            'username': 'user_antiguo',
            'contrasena': 'pass123',
            'fecha_naci_emple': f_nac_valida,
            'fecha_ing_emple': f_ing_antigua,
            'nom_emple': 'Test Antiguo'
        }
        response = self.client.post(reverse('usuarios:crear_empleado'), data=data_post_antigua)
        messages_2 = list(get_messages(response.wsgi_request))
        self.assertTrue(any("La fecha de ingreso no puede ser menor a tres meses atrás" in str(m) for m in messages_2))

    # ================================================================
    # 🔄 PRUEBAS DE EDICIÓN Y CONFIGURACIÓN EN CALIENTE
    # ================================================================

    def test_editar_usuario_no_duplica_hashing(self):
        """
        Garantiza que la validación `.startswith('pbkdf2_sha256$')` evite
        volver a encriptar un hash existente cuando la contraseña no se cambia.
        """
        session = self.client.session
        session['usuario_id'] = self.user_admin.id_usuario
        session['rol'] = 'Administrador'
        session.save()

        hash_original = self.user_empleado.contrasena

        # Enviamos el mismo hash simulando que el template lo cargó tal cual en el input
        data_post = {
            'username': 'empleado_test_modificado',
            'contrasena': hash_original,
            'id_rol': self.rol_empleado.id_rol
        }

        self.client.post(reverse('usuarios:editar_usuario', args=[self.user_empleado.id_usuario]), data=data_post)
        
        self.user_empleado.refresh_from_db()
        # El hash debe permanecer IDÉNTICO, no debe re-encriptarse
        self.assertEqual(self.user_empleado.contrasena, hash_original)

    def test_editar_perfil_actualiza_sesion_en_caliente(self):
        """
        Comprueba el candado de experiencia de usuario: al cambiar el username
        en editar_perfil, la variable de sesión request.session['username']
        debe actualizarse de inmediato para los menús y la navegación.
        """
        # Forzar sesión de empleado
        session = self.client.session
        session['usuario_id'] = self.user_empleado.id_usuario
        session['username'] = 'empleado_test'
        session['rol'] = 'Empleado'
        session.save()

        data_post = {
            'username': 'nuevo_nombre_navbar',
            'contrasena': '' # Vacío para no cambiar clave
        }

        response = self.client.post(reverse('usuarios:editar_perfil'), data=data_post)
        
        # Comprobar la sesión activa en el cliente de pruebas
        self.assertEqual(self.client.session['username'], 'nuevo_nombre_navbar')
>>>>>>> Stashed changes
