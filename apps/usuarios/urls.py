
from django.urls import path
from .views import index,eliminarusuario,registrar_usuario

urlpatterns = [
    path('', index, name='usuarios'),
    path('registrar/', registrar_usuario, name='registrar_usuario'),
    path('eliminar/<uuid:id_usuario>/', eliminarusuario, name='eliminar_usuario'),
]
