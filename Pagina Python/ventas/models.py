from django.db import models
from usuarios.models import Cliente 
# Eliminamos la importación física de inventario para evitar el Error Circular
# from inventario.models import Movimiento_matp 
from django.db.models import Sum

    

class Variacion(models.Model):
    id_var = models.AutoField(primary_key=True)
    talla_var = models.CharField(max_length=50)
    cant_soli = models.IntegerField()
    color_var = models.CharField(max_length=100)
    mat_var = models.CharField(max_length=200)
    costo_var = models.DecimalField(max_digits=12, decimal_places=2)
    id_estam_fk_var = models.ForeignKey('inventario.Estampado', on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

class Producto(models.Model):
    id_produc = models.AutoField(primary_key=True)
    imagen_product = models.ImageField(upload_to='producto/', max_length=500)
    imagen_hash = models.CharField(max_length=64, unique=True, editable=False, null=True)
    nom_produc = models.CharField(max_length=50)
    gen_produc = models.CharField(max_length=50)
    desc_produc = models.CharField(max_length=200)
    categoria_produc = models.CharField(max_length=50)
    estado_produc = models.CharField(max_length=50)
    dias_produccion = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.nom_produc

class Det_mov_matp(models.Model): 
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    # Referencia por string para evitar que Django se bloquee al cargar
    materia_prima = models.ForeignKey('inventario.Movimiento_matp', on_delete=models.CASCADE)
    cantidad_usada = models.DecimalField(max_digits=10, decimal_places=2)
    
    
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_ped = models.DateField(auto_now_add=True)
    subtotal_ped = models.DecimalField(max_digits=12, decimal_places=2)
    valor_ped = models.DecimalField(max_digits=12, decimal_places=2)
    estado_ped = models.CharField(max_length=50)
    metodo_pago = models.CharField(max_length=50)
    fecha_entrega = models.DateField(blank=True, null=True)
    id_clien_fk = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)

class Abono(models.Model):
    id_abono = models.AutoField(primary_key=True)
    fecha_abono = models.DateField(auto_now_add=True)  
    monto_abono = models.BigIntegerField()
    metodo_pago = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, default="")
    id_pedido_fk_abono = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.id_pedido_fk_abono:
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
    tipo_pedido = models.CharField(max_length=200)
    id_ped_fk_detval = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_var_fk_detval = models.ForeignKey(Variacion, on_delete=models.CASCADE, null=True)
    id_prod_fk_detval = models.ForeignKey(Producto, on_delete=models.CASCADE)

    
    id_personalizacion_3d = models.ForeignKey('inventario.PedidoPersonalizado', on_delete=models.CASCADE, null=True, blank=True)
