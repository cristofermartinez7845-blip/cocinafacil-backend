from rest_framework.routers import DefaultRouter

from .views import CategoriaViewSet, IngredienteViewSet

router = DefaultRouter()
router.register("categorias", CategoriaViewSet)
router.register("ingredientes", IngredienteViewSet)

urlpatterns = router.urls