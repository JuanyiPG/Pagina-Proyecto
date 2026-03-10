from django.db import models

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nom_rol = models.CharField(max_length=200)
def __str__(self):
        return self.nom_rol

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=255)
    id_rol_fk = models.ForeignKey(Rol, on_delete=models.CASCADE)

def __str__(self):
        return self.username

class Empleado(models.Model):
    id_emple = models.AutoField(primary_key=True)
    nom_emple = models.CharField(max_length=50)
    tele_emple = models.CharField(max_length=20)
    correo_emple = models.CharField(max_length=100)
    dir_emple = models.CharField(max_length=100)
    rh_emple = models.CharField(max_length=20)
    fecha_naci_emple= models.DateField()
    tipo_ident = models.CharField(max_length=100)
    num_ident = models.CharField(max_length=30)
    fecha_ing_emple = models.DateField()
    salari_emple = models.DecimalField(max_digits=10, decimal_places=2)
    estado_emple =models.CharField(max_length=50)
    id_usuario_fk = models.ForeignKey(Usuario, on_delete=models.CASCADE)

def __str__(self):
        return f"{self.nom_emple} (Empleado)"

class Cliente(models.Model):
    id_clien = models.AutoField(primary_key=True)
    nom_clien = models.CharField(max_length=50)
    dir_clien = models.CharField(max_length=100)
    tel_clien = models.CharField( max_length=20)
    correo_clien = models.CharField(max_length=100)
    id_usuario_fk = models.ForeignKey(Usuario, on_delete=models.CASCADE)

def __str__(self):
        return f"{self.nom_clien} (Cliente)"