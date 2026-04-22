from rest_framework import serializers
from .models import Movimiento_matp,Proveedor

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento_matp
        fields = ['tipo_mmtp', 'color_mmtp', 'fecha_mmtp','stock_mmtp','mat_mmtp','id_proveedor_fk']

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'