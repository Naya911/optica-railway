from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='categorias'),
    path('registrar/', views.registrar_categoria, name='registrar_categoria'),
    path('eliminar/<uuid:id_categoria>/', views.eliminar_categoria, name='eliminar_categoria'),
]
