from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'ventas'

urlpatterns = [
    path('lista_abono/', views.lista_abono, name='lista_abono'),
    path('form_abono/',  views.crear_abono, name='form_abono'),
    path('eliminar_abono/', views.eliminar_abono, name='elim_abono'),
    path('lista_product/', views.lista_producto, name='lista_product'),
    path('eliminar_producto/', views.eliminar_producto, name='elim_product'),
    path('editar_producto/', views.editar_producto, name='editar_producto'),
    path('form_producto/', views.crear_producto, name='form_producto')
]