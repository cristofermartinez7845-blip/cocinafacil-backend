from django.db.models import ProtectedError
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Categoria, Ingrediente
from .serializers import CategoriaSerializer, IngredienteSerializer


class ProtegidoMixin:
    """Si el elemento esta en uso por una receta, responde 409 en vez de un
    error 500 al intentar eliminarlo."""

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "No se puede eliminar: esta en uso por una o mas recetas."},
                status=status.HTTP_409_CONFLICT,
            )


class CategoriaViewSet(ProtegidoMixin, viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class IngredienteViewSet(ProtegidoMixin, viewsets.ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer