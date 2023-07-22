from django.contrib import admin

from apps.audiovisual.models import *

class PeliculaAdmin(admin.ModelAdmin):
    search_fields = ['titulo']
    list_display = ('id', 'titulo', 'image', 'url_thriller')

class SerieAdmin(admin.ModelAdmin):
    search_fields = ['titulo']
    list_display = ('id', 'titulo', 'image')

class NovelaAdmin(admin.ModelAdmin):
    search_fields = ['titulo']
    list_display = ('id', 'titulo', 'image')

class TemporadaAdmin(admin.ModelAdmin):
    search_fields = ['fk_serie__titulo']
    list_display = ('id', 'fk_serie', 'numero', 'url_thriller')

class ComentarioAdmin(admin.ModelAdmin):
    search_fields = ['fechaCreado']
    list_display = ('id', 'nombre', 'fechaCreado')

class CapituloAdmin(admin.ModelAdmin):
    search_fields = ['fk_temporada__fk_serie__titulo', 'fk_novela__titulo' ]
    # list_display = ('id', 'fk_temporada_fk_serie_titulo', 'fk_novela_titulo')

admin.site.register(Pelicula, PeliculaAdmin)
admin.site.register(Serie, SerieAdmin)
admin.site.register(Novela, NovelaAdmin)
admin.site.register(Temporada, TemporadaAdmin)
admin.site.register(Capitulo, CapituloAdmin)
admin.site.register(Comentario, ComentarioAdmin)
