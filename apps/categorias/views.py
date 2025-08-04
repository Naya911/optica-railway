from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Categoria
from .forms import CategoriaForm


def index(request):
    query = request.GET.get('q', '')
    if query:
        categorias = Categoria.objects.filter(
            Q(nombre__icontains=query) | 
            Q(descripcion__icontains=query)
        ).order_by('nombre')
    else:
        categorias = Categoria.objects.all().order_by('nombre')

    paginacion = Paginator(categorias, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    context = {
        'banner_title': 'Categorías',
        'pagina_actual': pagina_actual,
        'total_registros': categorias.count(),
        'query': query
    }

    return render(request, 'admin/categorias/index.html', context)

def registrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')
        return redirect('categorias')
    else:
        form = CategoriaForm()

    context = {
        'form': form,
        'banner_title': 'Registrar Categoría'
    }

    return render(request, 'admin/categorias/index.html', context)

def eliminar_categoria(request, id_categoria):
    categoria = get_object_or_404(Categoria, id_categoria=id_categoria)
    try:
        categoria.delete()
    except Exception as e:
        print(f"Error al eliminar la categoría: {str(e)}")
    return redirect('categorias')

