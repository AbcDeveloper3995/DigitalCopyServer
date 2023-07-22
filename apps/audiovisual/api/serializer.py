from rest_framework import serializers

from apps.audiovisual.models import *
from apps.utils import get_cant_comentarios

# SERIALIZADOR PELICULA
class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = '__all__'
        generos = {
            '1': 'Accion',
            '2': 'Comedia',
            '3': 'Terror',
            '4': 'Drama/Suspenso',
            '5': 'Policiaco',
            '6': 'Ciencia/Ficcion',
            '7': 'Basada en hechos reales',
        }

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'titulo': instance.titulo,
            'sinopsis': instance.sinopsis,
            'img': instance.image.url,
            'imgUrl': instance.image_url,
            'genero': self.Meta.generos.get(instance.genero),
            'url_thriller': instance.url_thriller,
            'likes': instance.likes,
            'ano_lanzamiento': instance.ano_lanzamiento,
            'tiempo': instance.tiempo,
            'elenco_principal': instance.elenco_principal,
            'cant_comentarios': get_cant_comentarios(instance.id, 1)
        }

# SERIALIZADOR SERIE
class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serie
        fields = '__all__'
        generos = {
            '1': 'Accion',
            '2': 'Comedia',
            '3': 'Terror',
            '4': 'Drama/Suspenso',
            '5': 'Policiaco',
            '6': 'Ciencia/Ficcion',
            '7': 'Basada en hechos reales',
        }
        estado = {
            '1': 'En transmision',
            '2': 'Finzalizada',
        }

    def get_cant_temporadas(self, id):
        query = Temporada.objects.filter(fk_serie_id=id).count()
        return query

    def get_temporadas(self, id):
        query = Temporada.objects.filter(fk_serie_id=id).values('id','numero','url_thriller')
        return query

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'titulo': instance.titulo,
            'sinopsis': instance.sinopsis,
            'img': instance.image.url,
            'imgUrl': instance.image_url,
            'genero': self.Meta.generos.get(instance.genero),
            'estado': self.Meta.estado.get(instance.estado),
            'likes': instance.likes,
            'ano_lanzamiento': instance.ano_lanzamiento,
            'tiempo': instance.tiempo,
            'elenco_principal': instance.elenco_principal,
            'cant_comentarios': get_cant_comentarios(instance.id, 2),
            'cant_temporada': self.get_cant_temporadas(instance.id),
            'temporadas': self.get_temporadas(instance.id),
        }

# SERIALIZADOR NOVELA
class NovelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novela
        fields = '__all__'
        estado = {
            '1': 'En transmision',
            '2': 'Finzalizada',
        }

    def get_capitulos(self, id):
        query = Capitulo.objects.filter(fk_novela_id=id).values('id','numero')
        return query

    def get_cant_capitulos(self, id):
        query = Capitulo.objects.filter(fk_novela_id=id).count()
        return query

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'titulo': instance.titulo,
            'sinopsis': instance.sinopsis,
            'img': instance.image.url,
            'imgUrl': instance.image_url,
            'estado': self.Meta.estado.get(instance.estado),
            'likes': instance.likes,
            'ano_lanzamiento': instance.ano_lanzamiento,
            'tiempo': instance.tiempo,
            'elenco_principal': instance.elenco_principal,
            'cant_comentarios': get_cant_comentarios(instance.id, 3),
            'pais': instance.pais,
            'capitulos': self.get_capitulos(instance.id),
            'cant_capitulos': self.get_cant_capitulos(instance.id),
        }

# SERIALIZADOR TEMPORADA
class TemporadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temporada
        fields = '__all__'

    def get_capitulos(self, id):
        query = Capitulo.objects.filter(fk_temporada_id=id).values('id','numero')
        return query

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fk_serie': instance.fk_serie.titulo,
            'numero': instance.numero,
            'url_thriller': instance.get_url(),
            'capitulos': self.get_capitulos(instance.id),
        }

# SERIALIZADOR CAPITULO
class CapituloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitulo
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'numero': instance.numero,
        }

# SERIALIZADORES DE LA API COMENTARIO
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'comentario': instance.comentario,
            'fecha': instance.fechaCreado,
        }
