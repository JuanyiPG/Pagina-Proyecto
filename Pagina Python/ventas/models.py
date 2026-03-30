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
    gen_produc = models.CharField(max_length=50)
    desc_produc = models.CharField(max_length=200)
    categoria_produc = models.CharField(max_length=50)
    estado_produc = models.CharField(max_length=50)
    dias_produccion = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=12, decimal_places= 3)


class Det_mov_matp(models.Model) : 
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    materia_prima = models.ForeignKey(Movimiento_matp, on_delete=models.CASCADE)
    cantidad_usada = models.DecimalField(max_digits=10, decimal_places=2)

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_ped = models.DateField(auto_now_add=True)
    subtotal_ped = models.DecimalField(max_digits=12, decimal_places= 2)
    valor_ped = models.DecimalField(max_digits=12, decimal_places=3)
    estado_ped = models.CharField(max_length=50)
    metodo_pago = models.CharField(max_length= 50)
    fecha_entrega = models.DateField(blank=True, null=True)
    id_clien_fk = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)


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
    id_pedido_fk_abono = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        total_abono = Abono.objects.filter(
            id_pedido_fk_abono=self.id_pedido_fk_abono
        ).aggregate(total=Sum('monto_abono'))['total'] or 0

        if total_abono >= self.id_pedido_fk_abono.valor_ped:
            self.id_pedido_fk_abono.estado_ped = 'PAGADO'
        else: 
            self.id_pedido_fk_abono.estado_ped = 'PENDIENTE'

        self.id_pedido_fk_abono.save()


class Det_valor(models.Model):
    id_det_valor = models.AutoField(primary_key=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=0)
    cant = models.DecimalField(max_digits=12, decimal_places=2)
    talla = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    tipo_pedido = models.CharField(max_length=200)
    id_ped_fk_detval = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_var_fk_detval = models.ForeignKey(Variacion, on_delete=models.CASCADE, null=True)
    id_prod_fk_detval = models.ForeignKey(Producto, on_delete=models.CASCADE)