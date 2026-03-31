from django.urls import path
from . import views

app_name="inventario"

urlpatterns=[
    #Proveedores
    path('proveedores/', views.lista_provee, name="lista_provee"),
    path('proveedores/editar/<int:id>/', views.editar_provee, name="editar_provee"),
    path('proveedores/eliminar/<int:id>/', views.eliminar_provee, name="eliminar_provee"),

    #Materia Prima
    path('mmtp/', views.lista_mmtp, name="lista_mmtp"),
    path('mmtp/editar/<int:id>/', views.editar_mmtp, name="editar_mmtp"),
    path('mmtp/eliminar/<int:id>/', views.eliminar_mmtp, name="eliminar_mmtp"),

    # Estampados
    path('estampados/', views.lista_estampado, name="lista_estampado"),
    path('estampados/editar/<int:id>/', views.editar_estampado, name="editar_estampado"),
    path('estampados/eliminar/<int:id>/', views.eliminar_estampado, name="eliminar_estampado"),
    
    
    path('modelo/<int:producto_id>/', views.modelo, name='modelo'),
]

