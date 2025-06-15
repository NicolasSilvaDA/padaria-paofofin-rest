from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views as core_views

router = DefaultRouter()
router.register(r'padarias', core_views.PadariaViewSet)
router.register(r'fornadas', core_views.FornadaViewSet)
router.register(r'inscricoes', core_views.InscricaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('padarias/<int:padaria_id>/inscrever/', core_views.inscrever_usuario_padaria, name='inscrever'),
    path('padarias/<int:padaria_id>/desinscrever/', core_views.desinscrever_usuario_padaria, name='desinscrever'),
    path('fornadas/criar/', core_views.criar_fornada, name='criar_fornada'),
]
