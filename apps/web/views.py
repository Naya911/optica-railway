from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.productos.models import Producto

def index(request):
    return render(request, 'index.html')

def panel(request):
    return render(request, 'admin/_base.html')

def probador_ar(request):
    productos = Producto.objects.filter(imagen_lente_ar__isnull=False).exclude(imagen_lente_ar='')  # Solo con imagen AR
    return render(request, 'probador_ar.html', {'productos': productos})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.rol == 'Administrador':
            return redirect('productos')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.rol == 'Administrador':
                return redirect('productos')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
