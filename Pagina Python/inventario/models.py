from django.db import models
from simple_history.models import HistoricalRecords 

class PedidoPersonalizado(models.Model):
    # 'ventas.Producto' le dice a Django: 
    # Busca el modelo 'Producto' dentro de la carpeta 'ventas'
    producto = models.ForeignKey('ventas.Producto', on_delete=models.CASCADE)
    estampado = models.ForeignKey('Estampado', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Datos de la personalización
    color_hex = models.CharField(max_length=7, default="#ffffff")
    tipo_personalizacion = models.CharField(max_length=20) 
    
    # Los 3 Renders del Modelo 3D
    foto_frente = models.ImageField(upload_to='renders_3d/', null=True, blank=True)
    foto_espalda = models.ImageField(upload_to='renders_3d/', null=True, blank=True)
    foto_lateral = models.ImageField(upload_to='renders_3d/', null=True, blank=True)
    
    precio_final = models.DecimalField(max_digits=12, decimal_places=3)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Personalización de {self.producto} - {self.id}"

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
    num_tel = models.CharField(max_length=50)

class Movimiento_matp(models.Model):
    id_mmtp = models.AutoField(primary_key=True)
    tipo_mmtp = models.CharField(max_length=100)
    mat_mmtp = models.CharField(max_length=100)
    fecha_mmtp = models.DateField()
    color_mmtp = models.CharField(max_length=100)
    stock_mmtp = models.DecimalField(max_digits=10, decimal_places=2)
    id_proveedor_fk = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    history = HistoricalRecords() #Crea el historial automaticamente