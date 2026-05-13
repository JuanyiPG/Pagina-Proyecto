from functools import wraps
import hashlib 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Rol, Usuario, Empleado, Cliente
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.contrib import messages
from django.views.decorators.cache import never_cache
from usuarios.models import Empleado, Cliente
from inventario.models import Proveedor
from ventas.models import Producto

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
        
        rol = request.session.get('rol')
        if rol in ['Administrador', 'Empleado', 'empleado']:
            
            return view_func(request, *args, **kwargs)
        
        messages.warning(request, "No tienes permisos para acceder.")
        return redirect('index') 
    return _wrapped_view

# ================================================================
# 🎭 CRUD DE ROLES (Sin cambios necesarios)
# ================================================================

@never_cache
@solo_personal
def lista_roles(request):
    roles = Rol.objects.all()
    return render(request, 'usuarios/roles/lista.html', {'roles': roles})

@solo_personal
def crear_rol(request):
    if request.method == 'POST':
        nom_rol = request.POST['nom_rol']
        Rol.objects.create(nom_rol=nom_rol)
        return redirect('usuarios:lista_roles')
    return render(request, 'usuarios/roles/crear.html')

@solo_personal
def editar_rol(request, id):
    rol = get_object_or_404(Rol, id_rol=id)
    if request.method == 'POST':
        rol.nom_rol = request.POST['nom_rol']
        rol.save()
        return redirect('usuarios:lista_roles')
    return render(request, 'usuarios/roles/editar.html', {'rol': rol})

@solo_personal
def eliminar_rol(request, id):
    rol = get_object_or_404(Rol, id_rol=id)
    rol.delete()
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
        username = request.POST['username']
        contrasena = request.POST['contrasena']
        id_rol = request.POST['id_rol']
        rol = Rol.objects.get(id_rol=id_rol)

        # IMPLEMENTACIÓN DE MAKE_PASSWORD
        Usuario.objects.create(
            username=username,
            contrasena=make_password(contrasena), # Encriptado
            id_rol_fk=rol
        )
        return redirect('usuarios:lista_usuarios')
    return render(request, 'usuarios/usuario/crear.html', {'roles': roles})

@solo_personal
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id_usuario=id)
    roles = Rol.objects.all()

    if request.method == 'POST':
        usuario.username = request.POST['username']
        nueva_contra = request.POST['contrasena']
        
        # LÓGICA DE ACTUALIZACIÓN DE CONTRASEÑA
        # Solo encriptamos si el campo no está vacío y no parece ya un hash
        if nueva_contra and not nueva_contra.startswith('pbkdf2_sha256$'):
            usuario.contrasena = make_password(nueva_contra)

        usuario.id_rol_fk = Rol.objects.get(id_rol=request.POST['id_rol'])
        usuario.save()
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
    return render(request, 'usuarios/empleados/lista.html', {'empleados': empleados, 'roles': roles})

@solo_personal
def crear_empleado(request):
    if request.method == 'POST':

        num_ident_val = request.POST.get('num_ident')
        user_val = request.POST.get('username')
        pass_val = request.POST.get('contrasena')
        rol_id = request.POST.get('id_rol')
        foto = request.FILES.get('foto_perfil')

        # --- SECCIÓN DE VALIDACIONES  ---

        if Empleado.objects.filter(num_ident=num_ident_val).exists():
            messages.error(request, f"⚠️ La identificación {num_ident_val} ya está registrada. No se creó ni el empleado ni el usuario.")
            return redirect('usuarios:lista_empleados')

        if Usuario.objects.filter(username=user_val).exists():
            messages.error(request, f"⚠️ El nombre de usuario '{user_val}' ya existe.")
            return redirect('usuarios:lista_empleados')

        # C. Validar credenciales vacías
        if not user_val or not pass_val:
            messages.error(request, "⚠️ Debes configurar el usuario.")
            return redirect('usuarios:lista_empleados')

        # D. Validar si la foto ya existe (Hash)
        foto_hash = None
        if foto:
            content = foto.read()
            foto_hash = hashlib.sha256(content).hexdigest()
            foto.seek(0)
            if Empleado.objects.filter(hash_foto=foto_hash).exists():
                messages.error(request, "⚠️ Esta fotografía ya está registrada.")
                return redirect('usuarios:lista_empleados')

        # --- SECCIÓN DE GUARDADO (Solo llegamos aquí si todo lo anterior pasó) ---
        try:
            with transaction.atomic():
                # Buscamos o creamos el Rol
                try:
                    if rol_id:
                        rol_obj = Rol.objects.get(id_rol=rol_id)
                    else:
                        rol_obj = Rol.objects.get(nom_rol='Empleado')
                except Rol.DoesNotExist:
                    rol_obj = Rol.objects.create(nom_rol='Empleado')

                # 1. Crear el Usuario
                nuevo_usuario = Usuario.objects.create(
                    username=user_val,
                    contrasena=make_password(pass_val),
                    id_rol_fk=rol_obj
                )

                # 2. Crear el Empleado vinculado al usuario
                Empleado.objects.create(
                    nom_emple=request.POST.get('nom_emple'),
                    tel_emple=request.POST.get('tel_emple'), 
                    correo_emple=request.POST.get('correo_emple'),
                    dir_emple=request.POST.get('dir_emple'),
                    rh_emple=request.POST.get('rh_emple'),
                    fecha_naci_emple=request.POST.get('fecha_naci_emple'),
                    tipo_ident=request.POST.get('tipo_ident'),
                    num_ident=num_ident_val,
                    fecha_ing_emple=request.POST.get('fecha_ing_emple'),
                    salari_emple=request.POST.get('salari_emple'),
                    estado_emple=request.POST.get('estado_emple'),
                    foto_perfil=foto,
                    hash_foto=foto_hash,
                    id_usuario_fk=nuevo_usuario 
                )
                
                messages.success(request, "✅ Empleado y usuario creados con éxito.")
                
        except Exception as e:
            messages.error(request, f"Error crítico al registrar: {e}")
            
    return redirect('usuarios:lista_empleados')

@solo_personal
def editar_empleado(request, id):
    # 1. Traemos al empleado. El objeto se llama 'empleado'
    empleado = get_object_or_404(Empleado, id_emple=id)
    roles = Rol.objects.all()
    
    if request.method == 'POST':
        foto_nueva = request.FILES.get('foto_perfil')
        
        if foto_nueva:
            content = foto_nueva.read()
            nuevo_hash = hashlib.sha256(content).hexdigest()
            foto_nueva.seek(0)
            if Empleado.objects.filter(hash_foto=nuevo_hash).exclude(id_emple=id).exists():
                messages.error(request, "⚠️ Esta foto ya pertenece a otro empleado.")
                return redirect('usuarios:editar_empleado', id=id)
            empleado.foto_perfil = foto_nueva
            empleado.hash_foto = nuevo_hash

        try:
            with transaction.atomic():
                # --- CAMPOS DEL EMPLEADO ---
                # Importante: Asegúrate que en el HTML el atributo 'name' sea igual a estos
                empleado.nom_emple = request.POST.get('nom_emple')
                empleado.tel_emple = request.POST.get('tel_emple')
                empleado.correo_emple = request.POST.get('correo_emple')
                empleado.dir_emple = request.POST.get('dir_emple')
                
                # Campos de identificación (se mantienen aunque sean readonly en el HTML)
                empleado.rh_emple = request.POST.get('rh_emple')
                empleado.tipo_ident = request.POST.get('tipo_ident')
                empleado.num_ident = request.POST.get('num_ident')
                empleado.fecha_naci_emple = request.POST.get('fecha_naci_emple')
                
                empleado.fecha_ing_emple = request.POST.get('fecha_ing_emple')
                empleado.salari_emple = request.POST.get('salari_emple')
                empleado.estado_emple = request.POST.get('estado_emple')
                
                # --- CAMPOS DEL USUARIO (RELACIONADO) ---
                # En tu modelo la relación es id_usuario_fk
                usuario = empleado.id_usuario_fk 
                usuario.username = request.POST.get('username')
                
                nueva_contra = request.POST.get('password')
                
                # Si el admin escribió algo y NO es el hash que ya existía, lo encriptamos
                if nueva_contra and not nueva_contra.startswith('pbkdf2_sha256$'):
                    usuario.contrasena = make_password(nueva_contra)
                
                rol_id = request.POST.get('id_rol')
                if rol_id:
                    usuario.id_rol_fk = Rol.objects.get(id_rol=rol_id)
                
                # Guardamos ambos
                usuario.save()
                empleado.save()

                messages.success(request, "✅ Información actualizada con éxito.")
                return redirect('usuarios:lista_empleados')

        except Exception as e:
            messages.error(request, f"Error al editar: {e}")
            
    # El objeto se pasa como 'empleado'
    return render(request, 'usuarios/empleados/editar.html', {'empleado': empleado, 'roles': roles})


@solo_personal
def eliminar_empleado(request, id):
    # 1. Buscamos el empleado por su ID
    empleado = get_object_or_404(Empleado, id_emple=id)
    
    try:
        # Usamos transaction.atomic para que si falla el borrado de uno, no se borre ninguno
        with transaction.atomic():
            # 2. Accedemos al usuario relacionado usando el nombre correcto del campo: id_usuario_fk
            usuario_relacionado = empleado.id_usuario_fk
            
            # 3. Borramos primero el empleado (opcional, el orden depende de tu DB, 
            # pero usualmente borramos el perfil y luego la cuenta)
            empleado.delete()
            
            # 4. Borramos el usuario
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
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/clientes/lista.html', {
        'clientes': clientes,
        'usuarios': usuarios
    })


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


@solo_personal
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id_clien=id)
    cliente.delete()
    return redirect('usuarios:lista_clientes')


# ================================================================
# 🔐 AUTENTICACIÓN (LOGIN, LOGOUT, REGISTRO)
# ================================================================

from django.contrib import messages # Asegúrate de tener la importación

def login_view(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        user_post = request.POST.get('username')
        pass_post = request.POST.get('password')
        
        try:
            usuario = Usuario.objects.get(username=user_post)
            
            if check_password(pass_post, usuario.contrasena):
                # --- SOLUCIÓN AL ERROR DE NOTIFICACIONES ---
                # 1. Consumimos los mensajes existentes para limpiar la cola
                storage = messages.get_messages(request)
                for _ in storage:
                    pass 
                
                # 2. Limpiamos la sesión
                request.session.flush() 

                # 3. Guardamos los nuevos datos
                request.session['usuario_id'] = usuario.id_usuario
                request.session['username'] = usuario.username
                request.session['rol'] = usuario.id_rol_fk.nom_rol

                # 4. Ahora el único mensaje en cola será el de éxito
                messages.success(request, f"Bienvenido, {usuario.username}")

                # Redirecciones según el rol
                if usuario.id_rol_fk.nom_rol == 'Administrador':
                    return redirect('usuarios:estadisticas_admin')
                elif usuario.id_rol_fk.nom_rol == 'Empleado':
                    return redirect('usuarios:editar_perfil')
                elif usuario.id_rol_fk.nom_rol == 'Cliente':
                    return redirect('ventas:lista_product')
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

@solo_personal
def panel_empleado(request):
    return render(request, 'ventas/abono/lista_abono_e.html')
@solo_personal
def estadisticas_admin(request):

    total_empleados = Empleado.objects.count()
    total_clientes = Cliente.objects.count()
    total_productos = Producto.objects.count()
    total_proveedores = Proveedor.objects.count()

    context = {
        'total_empleados': total_empleados,
        'total_clientes': total_clientes,
        'total_productos': total_productos,
        'total_proveedores': total_proveedores,
    }

    return render(request, 'usuarios/empleados/estadisticas.html', context)
@solo_personal
def editar_perfil(request):
    usuario_id = request.session.get('usuario_id')
    

    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
    

    empleado = Empleado.objects.filter(id_usuario_fk=usuario).first()

    if request.method == 'POST':
        user_val = request.POST.get('username')
        pass_val = request.POST.get('contrasena')
        nueva_foto = request.FILES.get('foto_perfil')


        if user_val:
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

