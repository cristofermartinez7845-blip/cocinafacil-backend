from rest_framework import viewsets

from .models import Receta
from .serializers import RecetaSerializer

class RecetaViewSet(viewsets.ModelViewSet):
    serializer_class = RecetaSerializer

    def get_queryset(self):
        queryset = Receta.objects.select_related("categoria").prefetch_related("items__ingrediente")

        categoria = self.request.query_params.get("categoria")
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)

        texto = self.request.query_params.get("q")
        if texto:
            queryset = queryset.filter(nombre__icontains=texto)

        return queryset

# Create your views here.
