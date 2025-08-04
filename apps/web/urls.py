
from django.urls import path,include
from .views import index,login_view,panel,probador_ar
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', index, name='inicio'),
    path('panel', panel, name='panel'),
    path('panel/usuarios/', include('apps.usuarios.urls')),
    path('panel/pacientes/', include('apps.pacientes.urls')),
    path('panel/reportes/', include('apps.reportes.urls')),
    path('panel/productos/', include('apps.productos.urls')),
    path('panel/categorias/', include('apps.categorias.urls')),
    path('login', login_view, name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('probador-ar/', probador_ar, name='probador_ar'), 
]
