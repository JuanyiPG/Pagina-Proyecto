from django.db import models
from LuxyFashion.usuarios.models import Cliente 
from LuxyFashion.inventario.models import Estampado


class Abono(models.Model):
    id_abono = models.AutoField(primary_key=True)
    fecha_abono = models.DateField()
    monto_abono = models.BigIntegerField()
    metodo_pago = models.CharField(max_length=50)
    estado_abono = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    nom_ped = models.CharField(max_length=100)
    talla_ped = models.CharField(max_length=50)
    color_ped = models.CharField(max_length=50)
    categoria_ped = models.CharField(max_length=50)
    material_ped = models.CharField(max_length=100)
    cant_ped = models.DecimalField(max_digits=10, decimal_places=2)
    desc_ped = models.CharField(max_length=200)
    fecha_ped = models.DateField()
    subtotal_ped = models.DecimalField(max_digits=12, decimal_places= 2)
    valor_ped = models.DecimalField(max_digits=12, decimal_places=2)
    estado_ped = models.CharField(max_length=50)
    metodo_pago = models.CharField(max_length= 50)
    id_abono_fk_pedido = models.ForeignKey(Abono, on_delete=models.CASCADE)
    id_clien_fk = models.ForeignKey(Cliente, on_delete=models.CASCADE)


class Variacion(models.Model) :
    id_var = models.AutoField(primary_key=True)
    talla_var = models.CharField(max_length=50)
    cant_soli = models.IntegerField()
    color_var = models.CharField(max_length=100)
    mat_var = models.CharField(max_length=200)
    costo_var = models.DecimalField(max_digits=12, decimal_places=2)
    id_estam_fk_var = models.ForeignKey(Estampado, on_delete=models.CASCADE)

class Producto(models.Model) :
    id_produc= models.AutoField(primary_key=True)
    link_produc = models.CharField(max_length=500)
    nom_produc = models.CharField(max_length=50)
    desc_produc = models.CharField(max_length=200)
    categoria_produc = models.CharField(max_length=50)
    estado_produc = models.CharField(max_length=50)

class Det_valor(models.Model):
    id_det_valor = models.AutoField(primary_key=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=0)
    cant = models.DecimalField(max_digits=12, decimal_places=2)
    tipo_pedido = models.CharField(max_length=200)
    id_var_fk_detval = models.ForeignKey(Variacion, on_delete=models.CASCADE)
    id_prod_fk_detval = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_abono_fk_detval = models.ForeignKey(Abono, on_delete=models.CASCADE)