from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm
from django.core.paginator import Paginator
from django.db.models import Q
from apps.categorias.models import Categoria
from django.core.files.uploadedfile import UploadedFile
import boto3
from django.conf import settings
from botocore.client import Config
from urllib.parse import quote_plus



def index(request):
    query = request.GET.get('q', '') 
    if query:
        lista_productos = Producto.objects.filter(
            Q(nombre__icontains=query) |
            Q(tipo__icontains=query) |
            Q(descripcion__icontains=query)
        ).order_by('-fecha_registro')  
    else:
        lista_productos = Producto.objects.all().order_by('-fecha_registro')  

    paginacion = Paginator(lista_productos, 6)
    numero_pagina = request.GET.get('page')
    pagina_actual = paginacion.get_page(numero_pagina)

    form = ProductoForm()  

    categorias = Categoria.objects.all().order_by('nombre') 

    TIPOS_PRODUCTO = [
        ('monofocal', 'Monofocal'),
        ('bifocal', 'Bifocal'),
        ('progresivo', 'Progresivo'),
        ('fotocromatico', 'Fotocromático'),
        ('antirreflejo', 'Antirreflejo'),
        ('otro', 'Otro'),
    ]

    context = {
        "banner_title": "Productos",
        "pagina_actual": pagina_actual,
        "total_registros": lista_productos.count(),
        "query": query,
        "categorias": categorias,
        "tipos": TIPOS_PRODUCTO,
        'form': form,
    }

    return render(request, 'admin/productos/index.html', context=context)


def eliminar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    try:
        producto.delete()
    except Exception as e:
        print(f"Error al eliminar el producto: {str(e)}")
    
    return redirect('productos')


def registrar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos')
        return redirect('productos')
    else:
        form = ProductoForm()

    context = {
        'form': form,
        'banner_title': 'Crear Producto'
    }

    return render(request, 'admin/productos/index.html', context)


def producto_editar(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)

            s3_client = boto3.client(
                's3',
                endpoint_url=settings.CLOUDFLARE_R2_BUCKET_ENDPOINT,
                aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY,
                aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_KEY,
                config=Config(signature_version='s3v4')
            )

            if 'cover' in request.FILES:
                cover_file = request.FILES['cover']
                filename = cover_file.name
                s3_client.upload_fileobj(
                    cover_file,
                    settings.CLOUDFLARE_R2_BUCKET,
                    f'covers/{filename}',
                    ExtraArgs={'ACL': 'public-read'}
                )
                producto.cover = f"https://caterbot.vsion.art/covers/{quote_plus(filename)}"

            if 'imagen_lente_ar' in request.FILES:
                ar_file = request.FILES['imagen_lente_ar']
                filename = ar_file.name
                s3_client.upload_fileobj(
                    ar_file,
                    settings.CLOUDFLARE_R2_BUCKET,
                    f'lentes_ar/{filename}',
                    ExtraArgs={'ACL': 'public-read'}
                )
                producto.imagen_lente_ar = f"https://caterbot.vsion.art/lentes_ar/{quote_plus(filename)}"

            producto.save()
            return redirect('productos')

    else:
        form = ProductoForm(instance=producto)

    categorias = Categoria.objects.all()
    tipos = dict(Producto._meta.get_field('tipo').choices)

    return render(request, 'admin/productos/index.html', {
        'form': form,
        'categorias': categorias,
        'tipos': tipos,
        'producto': producto,
    })