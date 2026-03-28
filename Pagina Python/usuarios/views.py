from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from .models import Rol, Usuario, Empleado, Cliente
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.contrib import messages
from django.views.decorators.cache import never_cache

# ================================================================
# 🛡️ DECORADORES DE SEGURIDAD CUSTOM (SIN USAR AUTH DE DJANGO)
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
        
        rol = request.session.get('rol')
        if rol in ['Administrador', 'Empleado']:
            return view_func(request, *args, **kwargs)
        
        # Si es un cliente intentando entrar a gestión interna
        messages.warning(request, "No tienes permisos para acceder a esta sección.")
        return redirect('index') 
    return _wrapped_view


# ================================================================
# 🎭 CRUD DE ROLES
# ================================================================

@never_cache
@login_requerido_custom
@solo_personal
def lista_roles(request):
    roles = Rol.objects.all()
    return render(request, 'usuarios/roles/lista.html', {'roles': roles})


@login_requerido_custom
@solo_personal
def crear_rol(request):
    if request.method == 'POST':
        nom_rol = request.POST['nom_rol']
        Rol.objects.create(nom_rol=nom_rol)
        return redirect('usuarios:lista_roles') # Se agregó el prefijo usuarios:
    return render(request, 'usuarios/roles/crear.html')


@login_requerido_custom
@solo_personal
def editar_rol(request, id):
    rol = get_object_or_404(Rol, id_rol=id)

    if request.method == 'POST':
        rol.nom_rol = request.POST['nom_rol']
        rol.save()
        return redirect('usuarios:lista_roles')

    return render(request, 'usuarios/roles/editar.html', {'rol': rol})


@login_requerido_custom
@solo_personal
def eliminar_rol(request, id):
    rol = get_object_or_404(Rol, id_rol=id)
    rol.delete()
    return redirect('usuarios:lista_roles')


# ================================================================
# 👤 CRUD DE USUARIOS
# ================================================================

@never_cache
@login_requerido_custom
@solo_personal
def lista_usuarios(request): # Se cambió @login_required nativo por el tuyo
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/usuario/lista.html', {'usuarios': usuarios})


@login_requerido_custom
@solo_personal
def crear_usuario(request):
    roles = Rol.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        contrasena = request.POST['contrasena']
        id_rol = request.POST['id_rol']

        rol = Rol.objects.get(id_rol=id_rol)

        Usuario.objects.create(
            username=username,
            contrasena=make_password(contrasena),
            id_rol_fk=rol
        )
        return redirect('usuarios:lista_usuarios')

    return render(request, 'usuarios/usuario/crear.html', {'roles': roles})


@login_requerido_custom
@solo_personal
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id_usuario=id)
    roles = Rol.objects.all()

    if request.method == 'POST':
        usuario.username = request.POST['username']
        nueva_contra = request.POST['contrasena']
        if nueva_contra and not nueva_contra.startswith('pbkdf2_sha256$'):
            usuario.contrasena = make_password(nueva_contra)

        usuario.id_rol_fk = Rol.objects.get(id_rol=request.POST['id_rol'])
        usuario.save()

        return redirect('usuarios:lista_usuarios')

    return render(request, 'usuarios/usuario/editar.html', {
        'usuario': usuario,
        'roles': roles
    })


@login_requerido_custom
@solo_personal
def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id_usuario=id)
    usuario.delete()
    return redirect('usuarios:lista_usuarios')


# ================================================================
# 👷 CRUD DE EMPLEADOS
# ================================================================

@never_cache
@login_requerido_custom
@solo_personal
def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'usuarios/empleados/lista.html', {'empleados': empleados})


@login_requerido_custom
@solo_personal
def crear_empleado(request):
    usuarios = Usuario.objects.all()

    if request.method == 'POST':
        id_usuario_seleccionado = request.POST.get('id_usuario_fk_emple')
        
        Empleado.objects.create(
            nom_emple=request.POST['nom_emple'],
            tel_emple=request.POST['tel_emple'], 
            correo_emple=request.POST['correo_emple'],
            dir_emple=request.POST['dir_emple'],
            rh_emple=request.POST['rh_emple'],
            fecha_naci_emple=request.POST['fecha_naci_emple'],
            tipo_ident=request.POST['tipo_ident'],
            num_ident=request.POST['num_ident'],
            fecha_ing_emple=request.POST['fecha_ing_emple'],
            salari_emple=request.POST['salari_emple'],
            estado_emple=request.POST['estado_emple'],
            id_usuario_fk=Usuario.objects.get(id_usuario=id_usuario_seleccionado)
        )

        return redirect('usuarios:lista_empleados')

    return render(request, 'usuarios/empleados/crear.html', {'usuarios': usuarios})


@login_requerido_custom
@solo_personal
def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id_emple=id)
    usuarios = Usuario.objects.all()

    if request.method == 'POST':
        empleado.nom_emple = request.POST['nom_emple']
        empleado.tel_emple = request.POST['tel_emple']
        empleado.correo_emple = request.POST['correo_emple']
        empleado.dir_emple = request.POST['dir_emple']
        empleado.rh_emple = request.POST['rh_emple']
        empleado.fecha_naci_emple = request.POST['fecha_naci_emple']
        empleado.tipo_ident = request.POST['tipo_ident']
        empleado.num_ident = request.POST['num_ident']
        empleado.fecha_ing_emple = request.POST['fecha_ing_emple']
        empleado.salari_emple = request.POST['salari_emple']
        empleado.estado_emple = request.POST['estado_emple']
        

        id_usuario = request.POST.get('id_usuario_fk')
        if id_usuario:
            empleado.id_usuario_fk = Usuario.objects.get(id_usuario=id_usuario)
        empleado.save()

        return redirect('usuarios:lista_empleados')
    return render(request, 'usuarios/empleados/editar.html', {
        'empleado': empleado,
        'usuarios': usuarios
    })


@login_requerido_custom
@solo_personal
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id_emple=id)
    empleado.delete()
    return redirect('usuarios:lista_empleados')


# ================================================================
# 🛍️ CRUD DE CLIENTES
# ================================================================

@never_cache
@login_requerido_custom
@solo_personal
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'usuarios/clientes/lista.html', {'clientes': clientes})


@login_requerido_custom
@solo_personal
def crear_cliente(request):
    usuarios = Usuario.objects.all()

    if request.method == 'POST':
        id_usuario_seleccionado = request.POST.get('id_usuario_fk_clien')

        Cliente.objects.create(
            nom_clien=request.POST['nom_clien'],
            dir_clien=request.POST['dir_clien'],
            tel_clien=request.POST['tel_clien'],
            correo_clien=request.POST['correo_clien'],
            id_usuario_fk=Usuario.objects.get(id_usuario=id_usuario_seleccionado)
        )

        return redirect('usuarios:lista_clientes')

    return render(request, 'usuarios/clientes/crear.html', {'usuarios': usuarios})


@login_requerido_custom
@solo_personal
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id_clien=id)
    usuarios = Usuario.objects.all()

    if request.method == 'POST':
        cliente.nom_clien = request.POST['nom_clien']
        cliente.dir_clien = request.POST['dir_clien']
        cliente.tel_clien = request.POST['tel_clien']
        cliente.correo_clien = request.POST['correo_clien']

        id_usuario = request.POST.get('id_usuario_fk_clien')
        if id_usuario:
            cliente.id_usuario_fk = Usuario.objects.get(id_usuario=id_usuario)

        cliente.save()
        return redirect('usuarios:lista_clientes')

    return render(request, 'usuarios/clientes/editar.html', {
        'cliente': cliente,
        'usuarios': usuarios
    })


@login_requerido_custom
@solo_personal
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id_clien=id)
    cliente.delete()
    return redirect('usuarios:lista_clientes')


# ================================================================
# 🔐 AUTENTICACIÓN (LOGIN, LOGOUT, REGISTRO)
# ================================================================

def login_view(request):
    if request.method == 'POST':
        user_post = request.POST.get('username')
        pass_post = request.POST.get('password')
        
        try:
            usuario = Usuario.objects.get(username=user_post)
            
            if check_password(pass_post, usuario.contrasena):
                request.session.flush() 

                request.session['usuario_id'] = usuario.id_usuario
                request.session['rol'] = usuario.id_rol_fk.nom_rol

                messages.success(request, f"Bienvenido, {usuario.username}")

                if usuario.id_rol_fk.nom_rol in ['Administrador', 'Empleado']:
                    return redirect('usuarios:lista_roles')
                else:
                    return redirect('index') 

            else:
                messages.error(request, "Contraseña incorrecta.")
                
        except Usuario.DoesNotExist:
            messages.error(request, "El usuario no existe.")
            
    return render(request, 'usuarios/login.html')


def logout_view(request):
    request.session.flush() # Elimina TODO de la sesión (Seguridad máxima)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('usuarios:login')


def registro_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        usuario_val = request.POST.get('username')
        contra = request.POST.get('password')

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