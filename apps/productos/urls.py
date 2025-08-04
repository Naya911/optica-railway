from django.urls import path
from .views import index, eliminar_producto, registrar_producto,producto_editar

urlpatterns = [
    path('', index, name='productos'),
    path('registrar/', registrar_producto, name='registrar_producto'),
    path('eliminar/<uuid:id_producto>/', eliminar_producto, name='eliminar_producto'),
    path('editar/<uuid:id_producto>/', producto_editar, name='producto_editar'),
]
