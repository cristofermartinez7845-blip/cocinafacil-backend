from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    unidad_por_defecto = models.CharField(max_length=20, default="unidad")

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

# Create your models here.
