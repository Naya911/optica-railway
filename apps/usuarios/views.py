from django.shortcuts import render
from .models import Usuario
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from .forms import UsuarioForm
from django.contrib.auth.hashers import make_password

def index(request):
    query = request.GET.get('q','') 
    if query:
        lista_usuarios = Usuario.objects.filter(
            Q(first_name__icontains=query) |  
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(ci__icontains=query) 
        ).order_by('-fecha_registro')  
    else:
        lista_usuarios = Usuario.objects.all().order_by('-fecha_registro')  
    paginacion=Paginator(lista_usuarios,6)
    numero_pagina=request.GET.get('page')
    pagina_actual=paginacion.get_page(numero_pagina)
    context={
        "banner_title":"Usuarios",
        "pagina_actual":pagina_actual,
        "total_registros": lista_usuarios.count(),
        "query": query
        
    }
    return render(request, 'admin/usuarios/index.html',context=context)

def eliminarusuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    try:
        usuario.delete()
    except Exception as e:
        print(f"Error al eliminar el usuario: {str(e)}")
    
    return redirect('usuarios')

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = make_password(form.cleaned_data['password'])  # Cifrar contraseña
            usuario.save()
            return redirect('usuarios')
        return redirect('usuarios')
    else:
        form = UsuarioForm()

    context = {
        'form': form,
        'banner_title': 'Crear Usuario'
    }

    return render(request, 'admin/usuarios/index.html', context)