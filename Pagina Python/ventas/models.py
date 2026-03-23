from django.db import models
from usuarios.models import Cliente 
from inventario.models import Estampado, Movimiento_matp
from django.db.models import Sum
    

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
    #carpeta en donde se guardara las imagines
    imagen_product = models.ImageField(upload_to='producto/', max_length=500)
    #para duplicados, guarda la imagen en capacidad de pixeles 
    imagen_hash = models.CharField(max_length=64, unique=True, editable=False, null=True)
    nom_produc = models.CharField(max_length=50)
    desc_produc = models.CharField(max_length=200)
    categoria_produc = models.CharField(max_length=50)
    estado_produc = models.CharField(max_length=50)
    dias_produccion = models.PositiveIntegerField(default=1)
    tipo_matp = models.CharField(max_length=200)
    cant_gast_matp = models.PositiveIntegerField(default=1)

class Det_mov_matp(models.Model) : 
    id_movi_mtp_fk_id_produc = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_abono_fk_pedido = models.ForeignKey(Movimiento_matp, on_delete=models.CASCADE, null=True, blank=True)

class Det_valor(models.Model):
    id_det_valor = models.AutoField(primary_key=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=0)
    cant = models.DecimalField(max_digits=12, decimal_places=2)
    tipo_pedido = models.CharField(max_length=200)
    estado_pago = models.CharField(max_length=50)
    id_var_fk_detval = models.ForeignKey(Variacion, on_delete=models.CASCADE)
    id_prod_fk_detval = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Abono(models.Model):
    id_abono = models.AutoField(primary_key=True)
    #El auto es para que el sistema llene por si solo la fecha (Se guarda solo una vez), no es necesario meterlo en la vista 
    #Para que guarde cada vez que se haga una modificación se usa auto_now
    #Si se quiere que el sistema lo guarde pero tambien se pueda modificar se usa el default= timezone.now (siempre va entre los parentesis)
    fecha_abono = models.DateField(auto_now_add=True)  
    monto_abono = models.BigIntegerField()
    metodo_pago = models.CharField(max_length=50)
    '''Coloque Text para que tenga mas espacio el cliente de escribir, de igual forma, como ese campo no es obligatorio, le coloque 
    Blank para que no salga error en el formulario y default, para que en la BD se guarde vacio y no genere error a futuro, igual si se quiere 
    colocar opcional en la BD se coloca null= True.
    '''
    descripcion = models.TextField( blank=True, default= "")
    id_detvalor_fk_abono = models.ForeignKey(Det_valor, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        total_abono = Abono.objects.filter(
            id_detvalor_fk_abono = self.id_detvalor_fk_abono
            #aggregate es para traer todo el conjunto de datos de una forma mas facil y que no utilice tanto almacenamiento 
        ).aggregate(Sum('monto'))['monto__sum'] or 0

        if total_abono >= self.id_detvalor_fk_abono.valor_total:
            self.id_detvalor_fk_abono.estado_pago = 'PAGADO'
        else: 
            self.id_detvalor_fk_abono.estado_pago = 'PENDIENTE'

        self.id_detvalor_fk_abono.save()
        id_abono_fk_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True, blank=True)

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    nom_ped = models.CharField(max_length=100)
    talla_ped = models.CharField(max_length=50)
    color_ped = models.CharField(max_length=50)
    categoria_ped = models.CharField(max_length=50)
    material_ped = models.CharField(max_length=100)
    cant_ped = models.DecimalField(max_digits=10, decimal_places=2)
    desc_ped = models.CharField(max_length=200)
    fecha_ped = models.DateField(auto_now_add=True)
    subtotal_ped = models.DecimalField(max_digits=12, decimal_places= 2)
    def save(self, *args, **kwargs):
        if self.cant_ped and self.valor_ped and self.cant_ped > 1: 
            self.subtotal_ped = self.cant_ped * self.valor_ped
        else: 
            self.subtotal_ped = self.valor_ped
        
        super().save(*args, **kwargs)
        
    valor_ped = models.DecimalField(max_digits=12, decimal_places=2)
    estado_ped = models.CharField(max_length=50)
    metodo_pago = models.CharField(max_length= 50)
    fecha_entrega = models.DateField(blank=True, null=True)
    id_clien_fk = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)