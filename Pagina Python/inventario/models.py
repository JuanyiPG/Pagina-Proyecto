from django.db import models

class Estampado(models.Model):
    id_estam = models.AutoField(primary_key=True)
    nombre_estam = models.CharField(max_length=100)
    link_estam = models.CharField(max_length=500)
    costo_adi = models.FloatField()
    tipo_estam = models.CharField(max_length=200)

class Proveedor(models.Model):
    id_prove = models.AutoField(primary_key=True)
    nom_provee = models.CharField(max_length=100)
    fech_ingre = models.DateField()
    num_tel = models.IntegerField()

class Movimiento_matp(models.Model):
    id_movi_mtp = models.AutoField(primary_key=True)
    tipo_movi_mtp = models.CharField(max_length=100)
    talla_movi_mtp = models.CharField(max_length=50)
    color_movi_mtp = models.CharField(max_length=100)
    fecha_movi_mtp = models.DateField()
    stock_movi_mtp = models.DecimalField(max_digits=10, decimal_places=2)
    id_estam_fk_invent = models.ForeignKey(Estampado, on_delete=models.CASCADE)
    id_proveedor_fk = models.ForeignKey(Proveedor, on_delete=models.CASCADE)