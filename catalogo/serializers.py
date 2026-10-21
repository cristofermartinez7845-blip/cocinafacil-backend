from rest_framework import serializers
from .models import Categoria, Ingrediente


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre"]

    def validate_nombre(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )
        return value


class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ["id", "nombre", "unidad_por_defecto"]

    def validate_nombre(self, value):
        return value.strip()