from rest_framework.routers import DefaultRouter

from .views import RecetaViewSet

router = DefaultRouter()
router.register("recetas", RecetaViewSet, basename="receta")

urlpatterns = router.urls