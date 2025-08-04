from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
import json

from apps.productos.models import Producto

def index(request):
    # === 1. Productos con imagen AR ===
    productos_ar = Producto.objects.filter(imagen_lente_ar__isnull=False).exclude(imagen_lente_ar='')

    # a) Top productos AR (puedes ajustar si hay una métrica de popularidad)
    chart_productos_ar = {
        'labels': [p.nombre for p in productos_ar[:10]],
        'series': [1 for _ in productos_ar[:10]],
    }

    # === 2. Cantidad de productos por categoría ===
    productos_por_categoria = Producto.objects.values('categoria__nombre') \
                                              .annotate(total=Count('id_producto')) \
                                              .order_by('-total')
    chart_categorias_ar = {
        'labels': [c['categoria__nombre'] for c in productos_por_categoria],
        'series': [c['total'] for c in productos_por_categoria],
    }

    # === 3. Cantidad de productos por tipo ===
    productos_por_tipo = Producto.objects.values('tipo') \
                                         .annotate(total=Count('id_producto')) \
                                         .order_by('-total')
    chart_tipos_ar = {
        'labels': [p['tipo'].capitalize() for p in productos_por_tipo],
        'series': [p['total'] for p in productos_por_tipo],
    }

    # === 4. Nuevos productos en los últimos 30 días ===
    fecha_limite = datetime.now() - timedelta(days=30)
    nuevos_productos = Producto.objects.filter(fecha_registro__gte=fecha_limite) \
                                       .annotate(fecha=TruncDate('fecha_registro')) \
                                       .values('fecha') \
                                       .annotate(total=Count('id_producto')) \
                                       .order_by('fecha')
    chart_nuevos_productos = {
        'labels': [p['fecha'].strftime('%Y-%m-%d') for p in nuevos_productos],
        'series': [p['total'] for p in nuevos_productos],
    }

    # === 5. Productos con y sin AR ===
    con_ar = productos_ar.count()
    sin_ar = Producto.objects.filter(imagen_lente_ar__isnull=True).count() + \
             Producto.objects.filter(imagen_lente_ar='').count()
    chart_segmentacion_ar = {
        'categorias': ['Con AR', 'Sin AR'],
        'cantidad': [con_ar, sin_ar],
    }

    # Serialización
    context = {
        'chart_productos_ar_json': json.dumps(chart_productos_ar),
        'chart_categorias_ar_json': json.dumps(chart_categorias_ar),
        'chart_tipos_ar_json': json.dumps(chart_tipos_ar),
        'chart_nuevos_productos_json': json.dumps(chart_nuevos_productos),
        'chart_segmentacion_ar_json': json.dumps(chart_segmentacion_ar),
    }

    return render(request, 'admin/reportes/index.html', context)
