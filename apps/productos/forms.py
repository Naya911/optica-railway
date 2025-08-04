from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'cover',
            'nombre',
            'categoria',
            'tipo',
            'descripcion',
            'precio',
            'imagen_lente_ar',
        ]
