from django.db import models

class Estampado(models.Model):
    id_estamp = models.AutoField(primary_key=True)
    nombre_estamp = models.CharField(max_length=100)
    link_estamp = models.CharField(max_length=500)
    costo_adi = models.FloatField()
    tipo_estamp = models.CharField(max_length=200)

class Proveedor(models.Model):
    id_provee = models.AutoField(primary_key=True)
    nom_provee = models.CharField(max_length=100)
    fech_ingre = models.DateField()
    num_tel = models.IntegerField()

class Movimiento_matp(models.Model):
    id_mmtp = models.AutoField(primary_key=True)
    tipo_mmtp = models.CharField(max_length=100)
    talla_mmtp = models.CharField(max_length=50)
    color_mmtp = models.CharField(max_length=100)
    fecha_mmtp = models.DateField()
    stock_mmtp = models.DecimalField(max_digits=10, decimal_places=2)
    id_estamp_fk_invent = models.ForeignKey(Estampado, on_delete=models.CASCADE)
    id_proveedor_fk = models.ForeignKey(Proveedor, on_delete=models.CASCADE)