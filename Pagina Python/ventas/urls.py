from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'ventas'

urlpatterns = [

    #---------------- ABONO -------------------------------------------
    path('lista_abono/', views.lista_abono, name='lista_abono'),
    path('form_abono/',  views.crear_abono, name='form_abono'),
    path('eliminar_abono/<int:pk>', views.eliminar_abono, name='elim_abono'),
    path('abono/<int:pedido_id>', views.crear_abono, name="crear_abono"),

    #--------------------- PRODUCTOS -----------------------------------------------
    path('lista_product/', views.lista_producto, name='lista_product'),
    path('lista_producto/admin', views.lista_producto_admin, name='lista_producto_admin'),
    path('eliminar_producto/<int:product_id>', views.eliminar_producto, name='eliminar_producto'),
    path('editar_producto/<int:id>', views.editar_producto, name='editar_producto'),
    path('producto_sin_personalizar/<int:producto_id>/', views.producto_sin_personalizar, name='producto_sin_personalizar'),

    #----------------------- CARRITO ---------------------------------------------------------
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('factura/<int:pedido_id>/', views.finalizar_pedido, name='finalizar_compra'),
    path('elim_carrito/<int:id_det_valor>/', views.eliminar_del_carrito, name='eliminar_carrito'),
    path('editar_carrito/<int:id_det_valor>/', views.editar_carrito, name='editar_carrito'),
    path('lista_pedido/', views.lista_pedido, name='lista_pedido'),
    path('abonos/', views.lista_abono_e, name='lista_abono_e'),
    path('productos-empleado/', views.lista_producto_e, name='lista_producto_e'),
    path('pedidos-empleado/', views.lista_pedido_e, name='lista_pedido_e'),
    
] 