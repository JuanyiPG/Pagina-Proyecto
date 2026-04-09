from django.db import models
class Estampado(models.Model):
    id_estamp = models.AutoField(primary_key=True)
    nombre_estamp = models.CharField(max_length=100)
    imagen_estamp = models.ImageField(upload_to='estampados/', null=True, blank=True)
    imagen_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    costo_adi = models.DecimalField(max_digits=12, decimal_places=3)
    tipo_estamp = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_estamp

class Proveedor(models.Model):
    id_provee = models.AutoField(primary_key=True)
    nom_provee = models.CharField(max_length=100)
    fech_ingre = models.DateField()
    num_tel = models.IntegerField()

class Movimiento_matp(models.Model):
    id_mmtp = models.AutoField(primary_key=True)
    tipo_mmtp = models.CharField(max_length=100)
    mat_mmtp = models.CharField(max_length=100)
    fecha_mmtp = models.DateField()
    color_mmtp = models.CharField(max_length=100)
    stock_mmtp = models.DecimalField(max_digits=10, decimal_places=2)
    id_proveedor_fk = models.ForeignKey(Proveedor, on_delete=models.CASCADE)