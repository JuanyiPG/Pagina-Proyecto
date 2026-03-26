from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'ventas'

urlpatterns = [
    path('lista_abono/', views.lista_abono, name='lista_abono'),
    path('form_abono/',  views.crear_abono, name='form_abono'),
    path('eliminar_abono/<int:pk>', views.eliminar_abono, name='elim_abono'),
    path('lista_product/', views.lista_producto, name='lista_product'),
    path('eliminar_producto/<int:product_id>', views.eliminar_producto, name='eliminar_producto'),
    path('editar_producto/<int:id>', views.editar_producto, name='editar_producto'),
    path('form_producto/', views.crear_producto, name='form_producto'),
    path('producto_sin_personalizar/<int:producto_id>/', views.producto_sin_personalizar, name='producto_sin_personalizar'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('factura/', views.finalizar_pedido, name='finalizar_compra')
]