from django.db import models


class Receta(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    instrucciones = models.TextField()
    tiempo_preparacion = models.PositiveIntegerField(help_text="Minutos")
    porciones = models.PositiveIntegerField(default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Una categoria tiene muchas recetas (ForeignKey, uno a muchos)
    categoria = models.ForeignKey(
        "catalogo.Categoria",
        on_delete=models.PROTECT,
        related_name="recetas",
    )

    # Una receta tiene muchos ingredientes y viceversa (ManyToMany),
    # pasando por la tabla intermedia RecetaIngrediente
    ingredientes = models.ManyToManyField(
        "catalogo.Ingrediente",
        through="RecetaIngrediente",
        related_name="recetas",
    )

    # Campo para el control de concurrencia (bloqueo optimista)
    version = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.nombre


class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(
        Receta, on_delete=models.CASCADE, related_name="items"
    )
    ingrediente = models.ForeignKey(
        "catalogo.Ingrediente", on_delete=models.PROTECT
    )
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)
    unidad = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["receta", "ingrediente"],
                name="ingrediente_unico_por_receta",
            )
        ]

    def __str__(self):
        return f"{self.cantidad} {self.unidad} de {self.ingrediente} en {self.receta}"

# Create your models here.
