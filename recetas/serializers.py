from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Receta, RecetaIngrediente


class ConflictoDeVersion(APIException):
    status_code = 409
    default_detail = (
        "La receta fue modificada por otra persona. "
        "Recarga los datos y vuelve a intentarlo."
    )
    default_code = "conflicto_de_version"


class RecetaIngredienteSerializer(serializers.ModelSerializer):
    ingrediente_nombre = serializers.CharField(
        source="ingrediente.nombre", read_only=True
    )

    class Meta:
        model = RecetaIngrediente
        fields = ["id", "ingrediente", "ingrediente_nombre", "cantidad", "unidad"]

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que 0.")
        return value


class RecetaSerializer(serializers.ModelSerializer):
    # Se expone como "ingredientes" para que coincida con los datos del mock
    ingredientes = RecetaIngredienteSerializer(
        many=True, source="items", required=False
    )
    categoria_nombre = serializers.CharField(
        source="categoria.nombre", read_only=True
    )

    class Meta:
        model = Receta
        fields = [
            "id",
            "nombre",
            "descripcion",
            "instrucciones",
            "tiempo_preparacion",
            "porciones",
            "fecha_creacion",
            "categoria",
            "categoria_nombre",
            "ingredientes",
            "version",
        ]
        read_only_fields = ["fecha_creacion"]
        extra_kwargs = {"version": {"required": False}}

    # --- Validaciones personalizadas ---
    def validate_nombre(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )
        return value

    def validate_tiempo_preparacion(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "El tiempo de preparación debe ser de al menos 1 minuto."
            )
        return value

    def validate_porciones(self, value):
        if value < 1:
            raise serializers.ValidationError("Debe haber al menos 1 porción.")
        return value

    def validate_ingredientes(self, items):
        ids = [item["ingrediente"].id for item in items]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError(
                "No puedes repetir un ingrediente en la misma receta."
            )
        return items

    # --- Crear y actualizar ---
    @transaction.atomic
    def create(self, validated_data):
        items = validated_data.pop("items", [])
        validated_data.pop("version", None)  # siempre empieza en 1
        receta = Receta.objects.create(**validated_data)
        for item in items:
            RecetaIngrediente.objects.create(receta=receta, **item)
        return receta

    @transaction.atomic
    def update(self, instance, validated_data):
        version_cliente = validated_data.pop("version", None)
        items = validated_data.pop("items", None)

        # Se bloquea la fila mientras dura la transacción
        receta = Receta.objects.select_for_update().get(pk=instance.pk)

        # Bloqueo optimista: la versión enviada debe ser la actual
        if version_cliente != receta.version:
            raise ConflictoDeVersion()

        for campo, valor in validated_data.items():
            setattr(receta, campo, valor)
        receta.version += 1
        receta.save()

        if items is not None:
            receta.items.all().delete()
            for item in items:
                RecetaIngrediente.objects.create(receta=receta, **item)
        return receta