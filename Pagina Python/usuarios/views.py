from django.shortcuts import render, redirect, get_object_or_404
from .models import Rol, Usuario, Empleado, Cliente



def lista_roles(request):
    roles = Rol.objects.all()
    return render(request, 'usuarios/roles/lista.html', {'roles': roles})

def crear_rol(request):
    if request.method == 'POST':
        nom_rol = request.POST['nom_rol']
        Rol.objects.create(nom_rol=nom_rol)
        return redirect('lista_roles')
    return render(request, 'usuarios/roles/crear.html')

def editar_rol(request, id):
    rol = get_object_or_404(Rol, id_rol=id)

    if request.method == 'POST':
        rol.nom_rol = request.POST['nom_rol']
        rol.save()
        return redirect('lista_roles')

    return render(request, 'usuarios/roles/editar.html', {'rol': rol})

def eliminar_rol(request, id):
    rol = get_object_or_404(Rol, id_rol=id)
    rol.delete()
    return redirect('lista_roles')


def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/usuario/lista.html', {'usuarios': usuarios})

def crear_usuario(request):
    roles = Rol.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        contrasena = request.POST['contrasena']
        id_rol = request.POST['id_rol']

        rol = Rol.objects.get(id_rol=id_rol)

        Usuario.objects.create(
            username=username,
            contrasena=contrasena,
            id_rol_fk=rol
        )

        return redirect('lista_usuarios')

    return render(request, 'usuarios/usuario/crear.html', {'roles': roles})

def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id_usuario=id)
    roles = Rol.objects.all()

    if request.method == 'POST':
        usuario.username = request.POST['username']
        usuario.contrasena = request.POST['contrasena']
        usuario.id_rol_fk = Rol.objects.get(id_rol=request.POST['id_rol'])
        usuario.save()

        return redirect('lista_usuarios')

    return render(request, 'usuarios/usuario/editar.html', {
        'usuario': usuario,
        'roles': roles
    })

def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id_usuario=id)
    usuario.delete()
    return redirect('lista_usuarios')




def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'usuarios/empleados/lista.html', {'empleados': empleados})

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

        return redirect('lista_empleados')

    return render(request, 'usuarios/empleados/crear.html', {'usuarios': usuarios})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado, Usuario

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

        return redirect('lista_empleados')
    return render(request, 'usuarios/empleados/editar.html', {
        'empleado': empleado,
        'usuarios': usuarios
    })
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id_emple=id)
    empleado.delete()
    return redirect('lista_empleados')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Usuario

# 🔹 LISTAR
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'usuarios/clientes/lista.html', {'clientes': clientes})


# 🔹 CREAR
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

        return redirect('lista_clientes')

    return render(request, 'usuarios/clientes/crear.html', {'usuarios': usuarios})


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
        return redirect('lista_clientes')

    return render(request, 'usuarios/clientes/editar.html', {
        'cliente': cliente,
        'usuarios': usuarios
    })


# 🔹 ELIMINAR
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id_clien=id)
    cliente.delete()
    return redirect('lista_clientes')