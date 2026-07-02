import hashlib
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.cache import never_cache

# Imports de modelos unificados y ordenados
from inventario.models import Proveedor
from ventas.models import Producto
from .models import Cliente, Empleado, Rol, Usuario

# ================================================================
# 🛡️ DECORADORES DE SEGURIDAD CUSTOM
# ================================================================

def login_requerido_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            messages.info(request, "Debes iniciar sesión para acceder a esta sección.")
            return redirect('usuarios:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def solo_personal(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('usuarios:login')
        
        rol = str(request.session.get('rol', '')).strip().capitalize()
        if rol in ['Administrador', 'Empleado']:
            return view_func(request, *args, **kwargs)
        
        messages.warning(request, "No tienes permisos para acceder.")
        return redirect('index') 
    return _wrapped_view


# ================================================================
# 🎭 CRUD DE ROLES 
# ================================================================

@never_cache
@solo_personal
def lista_roles(request):
    roles = Rol.objects.all()
    return render(request, 'usuarios/roles/lista.html', {'roles': roles})


@solo_personal
def crear_rol(request):
    if request.method == 'POST':
        nom_rol = request.POST.get('nom_rol', '').strip()
        if not nom_rol:
            messages.error(request, "El nombre del rol no puede estar vacío.")
            return redirect('usuarios:crear_rol') # O donde quieras redirigir

        if Rol.objects.filter(nom_rol__iexact=nom_rol).exists():
            messages.error(request, "El nombre del rol ya existe.")
        else:
            Rol.objects.create(nom_rol=nom_rol)
            messages.success(request, "Rol guardado con éxito")
            return redirect('usuarios:lista_roles')
    return render(request, 'usuarios/roles/crear.html')


@solo_personal
def editar_rol(request, id):
    rol = get_object_or_404(Rol, id_rol=id)
    if request.method == 'POST':
        rol.nom_rol = request.POST.get('nom_rol', '').strip()
        rol.save()
        messages.success(request, "Rol Actualizado con éxito")
        return redirect('usuarios:lista_roles')
    return render(request, 'usuarios/roles/editar.html', {'rol': rol})


@solo_personal
def eliminar_rol(request, id):
    rol = get_object_or_404(Rol, id_rol=id)
    try:
        rol.delete()
        messages.success(request, "Rol eliminado correctamente.")
    except Exception as e:
        messages.error(request, f"No se puede eliminar el rol porque está en uso: {e}")
    return redirect('usuarios:lista_roles')


# ================================================================
# 👤 CRUD DE USUARIOS
# ================================================================

@never_cache
@solo_personal
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    roles = Rol.objects.all()
    return render(request, 'usuarios/usuario/lista.html', {'usuarios': usuarios, 'roles': roles})


@solo_personal
def crear_usuario(request):
    roles = Rol.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        contrasena = request.POST.get('contrasena')
        id_rol = request.POST.get('id_rol')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, f"El nombre de usuario '{username}' ya existe.")
            return render(request, 'usuarios/usuario/lista.html', {'roles': roles})

        rol = get_object_or_404(Rol, id_rol=id_rol)
        Usuario.objects.create(
            username=username,
            contrasena=make_password(contrasena),
            id_rol_fk=rol
        )
        messages.success(request, "Usuario guardado con éxito")
        return redirect('usuarios:lista_usuarios')
    return render(request, 'usuarios/usuario/lista.html', {'roles': roles})


@solo_personal
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id_usuario=id)
    roles = Rol.objects.all()

    if request.method == 'POST':
        username_nuevo = request.POST.get('username', '').strip()
        # Capturamos el campo 'password' (el nombre del input nuevo)
        nueva_contra = request.POST.get('password')

        if Usuario.objects.filter(username=username_nuevo).exclude(id_usuario=id).exists():
            messages.error(request, "Ese nombre de usuario ya está en uso.")
            return redirect('usuarios:editar_usuario', id=id)

        usuario.username = username_nuevo
        
        # Lógica: Solo encriptar si el campo no está vacío
        if nueva_contra and len(nueva_contra) >= 8: # Añade tus validaciones de longitud
            usuario.contrasena = make_password(nueva_contra)

        rol_id = request.POST.get('id_rol')
        if rol_id:
            usuario.id_rol_fk = Rol.objects.get(id_rol=rol_id)
            
        usuario.save()
        messages.success(request, "Usuario actualizado con éxito")
        return redirect('usuarios:lista_usuarios')

    return render(request, 'usuarios/usuario/editar.html', {'usuario': usuario, 'roles': roles})


@solo_personal
def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id_usuario=id)
    usuario.delete()
    return redirect('usuarios:lista_usuarios')


# ================================================================
# 👷 CRUD DE EMPLEADOS
# ================================================================

@never_cache
@solo_personal
def lista_empleados(request):
    empleados = Empleado.objects.all()
    roles = Rol.objects.all()
    
    hoy = date.today()
    f_nac_max = (hoy - timedelta(days=18*365.25)).strftime('%Y-%m-%d')
    f_nac_min = (hoy - timedelta(days=70*365.25)).strftime('%Y-%m-%d')

    f_ing_max = hoy.strftime('%Y-%m-%d')
    f_ing_min = (hoy - timedelta(days=90)).strftime('%Y-%m-%d')

    context = {
        'empleados': empleados,
        'roles': roles,
        'f_nac_min': f_nac_min,
        'f_nac_max': f_nac_max,
        'f_ing_min': f_ing_min,
        'f_ing_max': f_ing_max,
    }
    return render(request, 'usuarios/empleados/lista.html', context)


@solo_personal
def crear_empleado(request):
    if request.method == 'POST':
        num_ident_val = request.POST.get('num_ident', '').strip()
        user_val = request.POST.get('username', '').strip()
        pass_val = request.POST.get('contrasena')
        rol_id = request.POST.get('id_rol')
        foto = request.FILES.get('foto_perfil')

        # Validaciones de unicidad y obligatoriedad
        if Empleado.objects.filter(num_ident=num_ident_val).exists():
            messages.error(request, f"La identificación {num_ident_val} ya está registrada.")
            return redirect('usuarios:lista_empleados')

        if Usuario.objects.filter(username=user_val).exists():
            messages.error(request, f" El nombre de usuario '{user_val}' ya existe.")
            return redirect('usuarios:lista_empleados')

        if not user_val or not pass_val:
            messages.error(request, "Debes configurar el usuario y la contraseña.")
            return redirect('usuarios:lista_empleados')

        foto_hash = None
        if foto:
            content = foto.read()
            foto_hash = hashlib.sha256(content).hexdigest()
            foto.seek(0)
            if Empleado.objects.filter(hash_foto=foto_hash).exists():
                messages.error(request, "Esta fotografía ya está registrada.")
                return redirect('usuarios:lista_empleados')

        f_nac_str = request.POST.get('fecha_naci_emple')
        f_ing_str = request.POST.get('fecha_ing_emple')

        if not f_nac_str or not f_ing_str:
            messages.error(request, "⚠️ Las fechas de nacimiento e ingreso son obligatorias.")
            return redirect('usuarios:lista_empleados')

        try:
            f_nac = date.fromisoformat(f_nac_str)
            f_ing = date.fromisoformat(f_ing_str)
            hoy = date.today()
        except ValueError:
            messages.error(request, "El formato de las fechas ingresadas no es válido.")
            return redirect('usuarios:lista_empleados')

        # Reglas de Negocio de Fechas
        edad = hoy.year - f_nac.year - ((hoy.month, hoy.day) < (f_nac.month, f_nac.day))
        if edad < 18 or edad > 70:
            messages.error(request, "❌ Error: El empleado debe tener entre 18 y 70 años.")
            return redirect('usuarios:lista_empleados')

        if f_ing > hoy:
            messages.error(request, "❌ Error: La fecha de ingreso no puede ser futura.")
            return redirect('usuarios:lista_empleados')

        limite_tres_meses = hoy - timedelta(days=90)
        if f_ing < limite_tres_meses:
            messages.error(request, "❌ Error: La fecha de ingreso no puede ser menor a tres meses atrás.")
            return redirect('usuarios:lista_empleados')

        if f_ing <= f_nac:
            messages.error(request, "❌ Error: La fecha de ingreso debe ser posterior al nacimiento.")
            return redirect('usuarios:lista_empleados')

        try:
            with transaction.atomic():
                try:
                    rol_obj = Rol.objects.get(id_rol=rol_id) if rol_id else Rol.objects.get(nom_rol='Empleado')
                except Rol.DoesNotExist:
                    rol_obj = Rol.objects.create(nom_rol='Empleado')

                nuevo_usuario = Usuario.objects.create(
                    username=user_val,
                    contrasena=make_password(pass_val),
                    id_rol_fk=rol_obj
                )

                Empleado.objects.create(
                    nom_emple=request.POST.get('nom_emple'),
                    tel_emple=request.POST.get('tel_emple'), 
                    correo_emple=request.POST.get('correo_emple'),
                    dir_emple=request.POST.get('dir_emple'),
                    rh_emple=request.POST.get('rh_emple'),
                    fecha_naci_emple=f_nac,
                    tipo_ident=request.POST.get('tipo_ident'),
                    num_ident=num_ident_val,
                    fecha_ing_emple=f_ing,
                    salari_emple=request.POST.get('salari_emple') or 0,
                    estado_emple=request.POST.get('estado_emple', 'Activo'),
                    foto_perfil=foto,
                    hash_foto=foto_hash,
                    id_usuario_fk=nuevo_usuario 
                )

            messages.success(request, "✅ Empleado y usuario creados con éxito.")
        except Exception as e:
            messages.error(request, f"Error crítico al registrar en la base de datos: {e}")
            
    return redirect('usuarios:lista_empleados')


@solo_personal
def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id_emple=id)
    roles = Rol.objects.all()
    hoy = timezone.now().date()
    
    hace_dos_meses = hoy - relativedelta(months=2)
    if hace_dos_meses.year < hoy.year:
        hace_dos_meses = date(hoy.year, 1, 1)
        
    f_nac_max_val = hoy - relativedelta(years=18)
    f_nac_min_val = hoy - relativedelta(years=70)

    if request.method == 'POST':
        num_ident_nuevo = request.POST.get('num_ident', '').strip()
        username_nuevo = request.POST.get('username', '').strip()
        foto_nueva = request.FILES.get('foto_perfil')
        
        # Validaciones de colisión de datos únicos en la edición
        if Empleado.objects.filter(num_ident=num_ident_nuevo).exclude(id_emple=id).exists():
            messages.error(request, "⚠️ Esta identificación ya pertenece a otro empleado.")
            return redirect('usuarios:editar_empleado', id=id)

        if Usuario.objects.filter(username=username_nuevo).exclude(id_usuario=empleado.id_usuario_fk.id_usuario).exists():
            messages.error(request, "⚠️ Este nombre de usuario ya está en uso.")
            return redirect('usuarios:editar_empleado', id=id)

        if foto_nueva:
            content = foto_nueva.read()
            nuevo_hash = hashlib.sha256(content).hexdigest()
            foto_nueva.seek(0)
            if Empleado.objects.filter(hash_foto=nuevo_hash).exclude(id_emple=id).exists():
                messages.error(request, "⚠️ Esta foto ya pertenece a otro empleado.")
                return redirect('usuarios:editar_empleado', id=id)
            empleado.foto_perfil = foto_nueva
            empleado.hash_foto = nuevo_hash

        f_nac_str = request.POST.get('fecha_naci_emple')
        f_ing_str = request.POST.get('fecha_ing_emple')

        if not f_nac_str or not f_ing_str:
            messages.error(request, "⚠️ Las fechas son obligatorias.")
            return redirect('usuarios:editar_empleado', id=id)

        f_nac = date.fromisoformat(f_nac_str)
        f_ing = date.fromisoformat(f_ing_str)

        if f_ing > hoy or f_ing < hace_dos_meses:
            messages.error(request, "Error: La fecha de ingreso está fuera de los rangos permitidos.")
            return redirect('usuarios:editar_empleado', id=id)

        edad_empleado = relativedelta(hoy, f_nac).years
        if edad_empleado < 18 or edad_empleado > 70 or f_ing <= f_nac:
            messages.error(request, "Error: Las fechas ingresadas son incoherentes con la normativa.")
            return redirect('usuarios:editar_empleado', id=id)

        try:
            with transaction.atomic():
                empleado.nom_emple = request.POST.get('nom_emple')
                empleado.tel_emple = request.POST.get('tel_emple')
                empleado.correo_emple = request.POST.get('correo_emple')
                empleado.dir_emple = request.POST.get('dir_emple')
                empleado.rh_emple = request.POST.get('rh_emple')
                empleado.tipo_ident = request.POST.get('tipo_ident')
                empleado.num_ident = num_ident_nuevo
                empleado.fecha_naci_emple = f_nac
                empleado.fecha_ing_emple = f_ing
                empleado.salari_emple = request.POST.get('salari_emple')
                empleado.estado_emple = request.POST.get('estado_emple')
                
                usuario = empleado.id_usuario_fk 
                usuario.username = username_nuevo
                
                # CORREGIDO: Uso de 'contrasena' consistente con tus formularios tradicionales
                nueva_contra = request.POST.get('contrasena')
                if nueva_contra and not nueva_contra.startswith('pbkdf2_sha256$'):
                    usuario.contrasena = make_password(nueva_contra)
                
                rol_id = request.POST.get('id_rol')
                if rol_id:
                    usuario.id_rol_fk = Rol.objects.get(id_rol=rol_id)
                
                usuario.save()
                empleado.save()

            messages.success(request, "Información actualizada con éxito.")
            return redirect('usuarios:lista_empleados')

        except Exception as e:
            messages.error(request, f"Error al editar en la base de datos: {e}")
            return redirect('usuarios:editar_empleado', id=id)
            
    return render(request, 'usuarios/empleados/editar.html', {
        'empleado': empleado, 
        'roles': roles,
        'f_ing_max': hoy.isoformat(),
        'f_ing_min': hace_dos_meses.isoformat(),
        'f_nac_max': f_nac_max_val.isoformat(),
        'f_nac_min': f_nac_min_val.isoformat()
    })


@solo_personal
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id_emple=id)
    try:
        with transaction.atomic():
            usuario_relacionado = empleado.id_usuario_fk
            empleado.delete()
            if usuario_relacionado:
                usuario_relacionado.delete()
            
            messages.success(request, "✅ Empleado y sus credenciales de acceso eliminados correctamente.")
    except Exception as e:
        messages.error(request, f"❌ Error al intentar eliminar: {e}")

    return redirect('usuarios:lista_empleados')


# ================================================================
#  CRUD DE CLIENTES
# ================================================================

@never_cache
@solo_personal
def lista_clientes(request):
    clientes = Cliente.objects.all()
    usuarios = Usuario.objects.exclude(id_rol_fk__nom_rol__icontains='administrador')
    return render(request, 'usuarios/clientes/lista.html', {'clientes': clientes, 'usuarios': usuarios})


@solo_personal
def crear_cliente(request):
    usuarios = Usuario.objects.exclude(id_rol_fk__nom_rol__icontains='administrador')

    if request.method == 'POST':
        id_usuario_seleccionado = request.POST.get('id_usuario_fk_clien')

        Cliente.objects.create(
            nom_clien=request.POST['nom_clien'],
            dir_clien=request.POST['dir_clien'],
            tel_clien=request.POST['tel_clien'],
            correo_clien=request.POST['correo_clien'],
            id_usuario_fk=Usuario.objects.get(id_usuario=id_usuario_seleccionado)
        )

        messages.success(request, "Cliente guardado con éxito")
        return redirect('usuarios:lista_clientes')

    return render(request, 'usuarios/clientes/crear.html', {'usuarios': usuarios})


@solo_personal
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id_clien=id)
    usuarios = Usuario.objects.exclude(id_rol_fk__nom_rol__icontains='administrador')

    if request.method == 'POST':
        cliente.nom_clien = request.POST['nom_clien']
        cliente.dir_clien = request.POST['dir_clien']
        cliente.tel_clien = request.POST['tel_clien']
        cliente.correo_clien = request.POST['correo_clien']

        id_usuario = request.POST.get('id_usuario_fk_clien')
        if id_usuario:
            cliente.id_usuario_fk = Usuario.objects.get(id_usuario=id_usuario)

        cliente.save()
        messages.success(request, "Cliente actualizado con éxito")
        return redirect('usuarios:lista_clientes')

    return render(request, 'usuarios/clientes/editar.html', {'cliente': cliente, 'usuarios': usuarios})


@solo_personal
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id_clien=id)
    cliente.delete()
    messages.success(request, "Cliente eliminado con éxito.")
    return redirect('usuarios:lista_clientes')


# ================================================================
# 🔐 AUTENTICACIÓN (LOGIN, LOGOUT, REGISTRO)
# ================================================================

def login_view(request):
    # Limpieza inicial de alertas previas colgadas
    storage = messages.get_messages(request)
    storage.used = True
    
    if request.method == 'POST':
        user_post = request.POST.get('username')
        pass_post = request.POST.get('password')
        
        try:
            usuario = Usuario.objects.get(username=user_post)
            
            # 🌟 DEBUG: Mira tu consola de comandos al presionar "Ingresar"
            print("\n" + "="*40)
            print(f"DEBUG LOGIN FOR: {user_post}")
            print(f"Clave escrita en formulario: '{pass_post}'")
            print(f"Hash guardado en Base de Datos: '{usuario.contrasena}'")
            
            es_valida = check_password(pass_post, usuario.contrasena)
            print(f"¿La contraseña coincide en Django?: {es_valida}")
            print("="*40 + "\n")
            
            if es_valida:
                # 1. Primero destruimos y recreamos la sesión de forma segura
                request.session.flush() 

                # 2. Asignamos los datos del usuario a la nueva sesión limpia
                request.session['usuario_id'] = usuario.id_usuario
                request.session['username'] = usuario.username
                request.session['rol'] = usuario.id_rol_fk.nom_rol

                # 3. Agregamos el mensaje de éxito DESPUÉS del flush
                messages.success(request, f"Bienvenido, {usuario.username}")

                # Estandarización de desvíos lógicos basados en rol normalizado
                rol_normalizado = str(usuario.id_rol_fk.nom_rol).strip().capitalize()
                
                if rol_normalizado == 'Administrador':
                    return redirect('usuarios:estadisticas_admin')
                elif rol_normalizado == 'Empleado':
                    return redirect('usuarios:editar_perfil')
                elif rol_normalizado == 'Cliente':
                    return redirect('ventas:lista_product')
                else:
                    return redirect('index') 

            else:
                messages.error(request, "Contraseña incorrecta.")
                
        except Usuario.DoesNotExist:
            messages.error(request, "El usuario no existe.")
            
    return render(request, 'usuarios/login.html')


def logout_view(request):
    request.session.flush() 
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('usuarios:login')


def registro_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono', '').strip() # Quitamos espacios en blanco extras
        correo = request.POST.get('correo')
        usuario_val = request.POST.get('username', '').strip()
        contra = request.POST.get('password')

        if telefono:
            telefono = telefono.replace(" ", "").replace("-", "")
            
            if not telefono.startswith('+57'):
                if telefono.startswith('57') and len(telefono) > 10:
                    telefono = '+' + telefono
                else:
                    telefono = '+57' + telefono

        if Usuario.objects.filter(username=usuario_val).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return render(request, 'usuarios/login.html')

        try:
            with transaction.atomic():
                rol_cliente, _ = Rol.objects.get_or_create(nom_rol='Cliente')

                nuevo_perfil = Usuario.objects.create(
                    username=usuario_val,
                    contrasena=make_password(contra), 
                    id_rol_fk=rol_cliente
                )

                Cliente.objects.create(
                    nom_clien=nombre,
                    dir_clien=direccion,
                    tel_clien=telefono, 
                    correo_clien=correo,
                    id_usuario_fk=nuevo_perfil
                )

            messages.success(request, '¡Registro exitoso! Ya puedes iniciar sesión.')
            return redirect('usuarios:login')

        except Exception as e:
            messages.error(request, 'Error al registrar: ' + str(e))
            
    return render(request, 'usuarios/login.html')


# ================================================================
# 📊 PANELES GENERALES
# ================================================================

@solo_personal
def panel_empleado(request):
    return render(request, 'ventas/abono/lista_abono_e.html')


@solo_personal
def estadisticas_admin(request):
    context = {
        'total_empleados': Empleado.objects.count(),
        'total_clientes': Cliente.objects.count(),
        'total_productos': Producto.objects.count(),
        'total_proveedores': Proveedor.objects.count(),
    }
    return render(request, 'usuarios/empleados/estadisticas.html', context)


@solo_personal
def editar_perfil(request):
    usuario_id = request.session.get('usuario_id')
    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
    empleado = Empleado.objects.filter(id_usuario_fk=usuario).first()

    if request.method == 'POST':
        user_val = request.POST.get('username', '').strip()
        pass_val = request.POST.get('contrasena')
        nueva_foto = request.FILES.get('foto_perfil')

        if user_val:
            if Usuario.objects.filter(username=user_val).exclude(id_usuario=usuario_id).exists():
                messages.error(request, "Ese nombre de usuario ya se encuentra ocupado.")
                return redirect('usuarios:editar_perfil')
            usuario.username = user_val
            
        if pass_val:
            usuario.contrasena = make_password(pass_val)
        usuario.save()

        if empleado and nueva_foto:
            empleado.foto_perfil = nueva_foto
            empleado.save()
        
        messages.success(request, "Perfil actualizado con éxito.")
        return redirect('usuarios:editar_perfil')

    return render(request, 'usuarios/usuario/editar_perfil.html', {
        'usuario': usuario,
        'empleado': empleado
    })


def perfil_cliente(request, id):
    usuario_id = request.session.get('usuario_id')
    usuario = get_object_or_404(Usuario, id_usuario=id)

    if not usuario_id:
        return redirect('usuarios:login')

    cliente = get_object_or_404(Cliente, id_usuario_fk__id_usuario=usuario_id)
    if request.method == 'POST':
        cliente.nom_clien = request.POST.get('nom_clien')
        cliente.correo_clien = request.POST.get('correo_clien')
        cliente.tel_clien = request.POST.get('tel_clien')
        cliente.dir_clien = request.POST.get('dir_clien')
        usuario.username_nuevo = request.POST.get('username', '').strip()
        usuario.nueva_contra = request.POST.get('password')

        cliente.save()

        return redirect('ventas:lista_product')

    return render(request, 'usuarios/clientes/Perfil_Cliente.html', {
        'cliente': cliente
    })