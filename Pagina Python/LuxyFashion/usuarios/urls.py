from django.urls import path
from . import views

urlpatterns = [

path('roles/', views.lista_roles, name='lista_roles'),
path('roles/crear/', views.crear_rol, name='crear_rol'),
path('roles/editar/<int:id>/', views.editar_rol, name='editar_rol'),
path('roles/eliminar/<int:id>/', views.eliminar_rol, name='eliminar_rol'),


path('usuario/', views.lista_usuarios, name='lista_usuarios'),
path('usuario/crear/', views.crear_usuario, name='crear_usuario'),
path('usuario/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
path('usuario/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),


path('empleados/', views.lista_empleados, name='lista_empleados'),
path('empleados/crear/', views.crear_empleado, name='crear_empleado'),
path('empleados/editar/<int:id>/', views.editar_empleado, name='editar_empleado'),
path('empleados/eliminar/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),


path('clientes/', views.lista_clientes, name='lista_clientes'),
path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

]