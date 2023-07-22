import random

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.audiovisual.api.serializer import *
from apps.utils import procedimiento_para_obtener_comentarios, procedimiento_para_dar_like


class Generic(viewsets.ModelViewSet):
    serializer_class = None
    list_serializer_class = None
    mensajeCreado = None
    mensajeModificado = None
    mensajeGetObject = None
    mensajeEliminado = None
    mensajeNotFound = None

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        query = list(self.get_queryset())
        aux = random.sample(query, 2)
        serializer = self.serializer_class(aux, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': self.mensajeCreado}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        concepto = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(concepto)
        return Response({'message': self.mensajeGetObject, 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': self.mensajeModificado, 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': self.mensajeNotFound}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        concepto = self.get_queryset(pk)
        if concepto:
            concepto.delete()
            return Response({'message': self.mensajeEliminado}, status=status.HTTP_200_OK)
        return Response({'message': self.mensajeNotFound}, status=status.HTTP_400_BAD_REQUEST)

#VIEW DE PELICULA
class PeliculaViewSet(Generic):
    serializer_class = PeliculaSerializer
    mensajeGetObject = 'Detalles de la pelicula.'
    mensajeNotFound = 'Pelicula no encontrada.'

    def buscador(self, titulo=None, genero=None, indicador=None):
        if genero == None:
            data = {
                '1': Pelicula.objects.filter(titulo__icontains=titulo),
                '2': Serie.objects.filter(titulo__icontains=titulo),
                '3': Novela.objects.filter(titulo__icontains=titulo),
            }
            query = data.get(indicador)
        elif titulo == None:
            data = {
                '1': Pelicula.objects.filter(genero=genero),
                '2': Serie.objects.filter(genero=genero),
                '3': Novela.objects.filter(pais__icontains=genero),
            }
            query = data.get(indicador)
        else:
            data = {
                '1': Pelicula.objects.filter(titulo__icontains=titulo, genero=genero),
                '2': Serie.objects.filter(titulo__icontains=titulo, genero=genero),
                '3': Novela.objects.filter(titulo__icontains=titulo, pais__icontains=genero),
            }
            query = data.get(indicador)
        if not query.exists():
            return False
        if indicador == '1':
            serializer = PeliculaSerializer(query, many=True)
        elif indicador == '2':
            serializer = SerieSerializer(query, many=True)
        else:
            serializer = NovelaSerializer(query, many=True)
        return serializer.data

    @action(detail=False, methods=['get'], url_path='getEstrenos')
    def get_estrenos(self, request, *args, **kwargs):
        query = list(Pelicula.objects.filter(es_estreno=True))
        aux = random.sample(query, 2)
        serializer = self.serializer_class(aux, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='darLike')
    def dar_like(self, request, *args, **kwargs):
        dataModelos = {
            '1': Pelicula,
            '2': Serie,
            '3': Novela,
        }
        parametros = self.kwargs['pk'].split('-')
        idAudiovisual = parametros[0]
        modelo = dataModelos.get(parametros[1])
        procedimiento_para_dar_like(modelo, idAudiovisual)
        return Response('', status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='getAudiovisual')
    def get_getAudiovisual(self, request, *args, **kwargs):
        parametros, aux = self.kwargs['pk'].split('-'), None
        titulo = parametros[0]
        genero = parametros[1]
        indicador = parametros[2]
        if titulo != '' and genero != '':
            aux = self.buscador(titulo,genero, indicador)
        elif titulo != '' and genero == '':
            aux = self.buscador(titulo, None, indicador)
        elif titulo == '' and genero != '':
            aux = self.buscador(titulo, genero, indicador)
        return Response(aux, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='getLista3D')
    def get_lista3D(self, request, *args, **kwargs):
        query = list(Pelicula.objects.all())
        aux = random.sample(query, 9)
        serializer = PeliculaSerializer(aux, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='topLiked')
    def get_topLiked(self, request, *args, **kwargs):
        aux = []
        peliculas = Pelicula.objects.order_by('-likes')[:3]
        serializer = PeliculaSerializer(peliculas, many=True)
        for i in serializer.data:
            aux.append(i)
        novela = Novela.objects.order_by('likes')[:2]
        serializer = NovelaSerializer(novela, many=True)
        for i in serializer.data:
            aux.append(i)
        serie = Serie.objects.order_by('likes')[:2]
        serializer = SerieSerializer(serie, many=True)
        for i in serializer.data:
            aux.append(i)
        aux = sorted(aux, key=lambda x: x['likes'], reverse=True)
        return Response(aux, status=status.HTTP_200_OK)

#VIEW DE SERIE
class SerieViewSet(PeliculaViewSet):
    serializer_class = SerieSerializer
    mensajeGetObject = 'Detalles de la pelicula.'
    mensajeNotFound = 'Pelicula no encontrada.'

#VIEW DE NOVELA
class NovelaViewSet(PeliculaViewSet):
    serializer_class = NovelaSerializer
    mensajeGetObject = 'Detalles de la pelicula.'
    mensajeNotFound = 'Pelicula no encontrada.'

#VIEW DE TEMPORADA
class TemporadaViewSet(Generic):
    serializer_class = TemporadaSerializer
    mensajeGetObject = 'Detalles de la pelicula.'
    mensajeNotFound = 'Pelicula no encontrada.'

    @action(detail=True, methods=['get'], url_path='getThrillerYcapitulos')
    def getThrillerYcapitulos(self, request, *args, **kwargs):
        idTemporada = self.kwargs['pk']
        query = get_object_or_404(Temporada, pk=idTemporada)
        seriealizer = self.serializer_class(query)
        return Response(seriealizer.data, status=status.HTTP_200_OK)

#VIEW DE CAPITULO
class CapituloViewSet(Generic):
    serializer_class = CapituloSerializer
    mensajeGetObject = 'Detalles de la pelicula.'
    mensajeNotFound = 'Pelicula no encontrada.'

#VIEW DE COMEMTARIO
class ComentarioViewSet(Generic):
    serializer_class = ComentarioSerializer
    mensajeGetObject = 'Detalles de la pelicula.'
    mensajeNotFound = 'Pelicula no encontrada.'

    @action(detail=False, methods=['post'], url_path='createComentarioPersonalizado')
    def create_comentario_personalizado(self, request, *args, **kwargs):
        data = {}
        if request.data['fk_pelicula'] != '':
            Comentario.objects.create(
                fk_pelicula_id=request.data['fk_pelicula'],
                nombre=request.data['nombre'],
                comentario=request.data['comentario']
            )
            data['message'] = 'Comentario realizado correctamente.'
        elif request.data['fk_serie'] != '':
            Comentario.objects.create(
                fk_serie_id=request.data['fk_serie'],
                nombre=request.data['nombre'],
                comentario=request.data['comentario']
            )
            data['message'] = 'Comentario realizado correctamente.'
        else:
            Comentario.objects.create(
                fk_novela_id=request.data['fk_novela'],
                nombre=request.data['nombre'],
                comentario=request.data['comentario']
            )
            data['message'] = 'Comentario realizado correctamente.'
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='getComentarios')
    def get_comentarios(self, request, *args, **kwargs):
        parametros = self.kwargs['pk'].split('-')
        idAudiovisual = parametros[0]
        indicadorAudiovisual = parametros[1]
        seriealizer = procedimiento_para_obtener_comentarios(self.serializer_class.Meta.model, self.serializer_class, idAudiovisual, indicadorAudiovisual)
        return Response(seriealizer.data, status=status.HTTP_200_OK)