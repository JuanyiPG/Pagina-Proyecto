from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500 

from LuxyFashion import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ventas/', include('ventas.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('inventario/', include('inventario.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'LuxyFashion.views.error_404'
handler500 = 'LuxyFashion.views.error_500'
    
