from rest_framework import serializers
from .models import Movimiento_matp

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento_matp
        fields = ['tipo_mmtp', 'color_mmtp', 'fecha_mmtp','stock_mmtp','mat_mmtp','id_proveedor_fk']