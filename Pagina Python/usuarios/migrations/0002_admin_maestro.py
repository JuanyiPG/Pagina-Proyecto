from django.db import migrations
from django.contrib.auth.hashers import make_password

def administrador_maestro(apps, schema_editor):
    # Traemos los modelos desde el historial de Django para evitar conflictos
    Rol = apps.get_model('usuarios', 'Rol')
    Usuario = apps.get_model('usuarios', 'Usuario')

    # 1. Crear el Rol de Administrador de manera segura
    rol_admin, _ = Rol.objects.get_or_create(nom_rol='Administrador')
    
    # 2. Crear el Usuario Administrador (solo si no existe ya)
    if not Usuario.objects.filter(username='admin_maestro').exists():
        Usuario.objects.create(
            username='admin_maestro',
            contrasena=make_password('Luxy2026*'),
            id_rol_fk=rol_admin
        )

class Migration(migrations.Migration):

    # CRUCIAL: Este bloque le dice a Django el orden correcto de ejecución
    dependencies = [
        ('usuarios', '0001_initial'), # <-- Si tu archivo inicial se llama diferente, cámbialo aquí
    ]

    operations = [
        migrations.RunPython(administrador_maestro),
    ]