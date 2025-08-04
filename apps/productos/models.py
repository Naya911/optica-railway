from django.db import models
import uuid
import boto3
from botocore.client import Config
from django.conf import settings
import os
from urllib.parse import urlparse, quote_plus
from apps.categorias.models import Categoria


class Producto(models.Model):
    id_producto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cover = models.URLField(null=True, blank=True)
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos',
        verbose_name='Categoría'
    )
    tipo = models.CharField(max_length=50, choices=[
        ('monofocal', 'Monofocal'),
        ('bifocal', 'Bifocal'),
        ('progresivo', 'Progresivo'),
        ('fotocromatico', 'Fotocromático'),
        ('antirreflejo', 'Antirreflejo'),
        ('otro', 'Otro')
    ])
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_lente_ar = models.URLField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo} para {self.nombre}"
    
    class Meta:
        db_table = 'producto'

    def save(self, *args, **kwargs):
        s3_client = boto3.client(
            's3',
            endpoint_url=settings.CLOUDFLARE_R2_BUCKET_ENDPOINT,
            aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY,
            aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )

        if self.cover and hasattr(self.cover, 'file') and not str(self.cover).startswith('http'):
            file_name = os.path.basename(self.cover.name)
            s3_client.upload_fileobj(
                self.cover.file,
                settings.CLOUDFLARE_R2_BUCKET,
                f'covers/{file_name}',
                ExtraArgs={'ACL': 'public-read'}
            )
            self.cover = f"https://caterbot.vsion.art/covers/{quote_plus(file_name)}"

        if self.imagen_lente_ar and hasattr(self.imagen_lente_ar, 'file') and not str(self.imagen_lente_ar).startswith('http'):
            file_name = os.path.basename(self.imagen_lente_ar.name)
            s3_client.upload_fileobj(
                self.imagen_lente_ar.file,
                settings.CLOUDFLARE_R2_BUCKET,
                f'lentes_ar/{file_name}',
                ExtraArgs={'ACL': 'public-read'}
            )
            self.imagen_lente_ar = f"https://caterbot.vsion.art/lentes_ar/{quote_plus(file_name)}"

        super().save(*args, **kwargs)



