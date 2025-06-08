from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PadariaViewSet, FornadaViewSet, InscricaoViewSet

router = DefaultRouter()
router.register(r'padarias', PadariaViewSet)
router.register(r'fornadas', FornadaViewSet)
router.register(r'inscricoes', InscricaoViewSet)

urlpatterns = [
    path('', include(router.urls))
]
