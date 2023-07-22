from rest_framework.routers import DefaultRouter

from apps.audiovisual.api.views import *

router = DefaultRouter()
router.register(r'pelicula', PeliculaViewSet, basename='PeliculaViewSet'),
router.register(r'serie', SerieViewSet, basename='PeliculaViewSet'),
router.register(r'novela', NovelaViewSet, basename='NovelaViewSet'),
router.register(r'temporada', TemporadaViewSet, basename='TemporadaViewSet'),
router.register(r'capitulo', CapituloViewSet, basename='CapituloViewSet'),
router.register(r'comentario', ComentarioViewSet, basename='ComentarioViewSet'),

urlpatterns = router.urls