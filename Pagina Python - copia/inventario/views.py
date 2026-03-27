from django.shortcuts import render
from .models import Estampado, Proveedor, Movimiento_matp
#proveedor
def lista_provee(request):
    proveedor= Proveedor.objects.all()
    return render(request, )
