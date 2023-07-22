from django.shortcuts import get_object_or_404

from apps.audiovisual.models import Comentario


def get_cant_comentarios(id, indicadorAudiovisual):
    if indicadorAudiovisual == 1:
        query = Comentario.objects.filter(fk_pelicula_id=id).count()
    elif indicadorAudiovisual == 2:
        query = Comentario.objects.filter(fk_serie_id=id).count()
    else:
        query = Comentario.objects.filter(fk_novela_id=id).count()
    return query

def procedimiento_para_dar_like(model, id):
    query = get_object_or_404(model, pk=id)
    query.likes += 1
    query.save()

def procedimiento_para_obtener_comentarios(model, serializer, idAudiovisual, indicadorAudiovisual):
    if indicadorAudiovisual == '1':
        query = model.objects.filter(fk_pelicula_id=idAudiovisual)
        seriealizer = serializer(query, many=True)
    elif indicadorAudiovisual == '2':
        query = model.objects.filter(fk_serie_id=idAudiovisual)
        seriealizer = serializer(query, many=True)
    else:
        query = model.objects.filter(fk_novela_id=idAudiovisual)
        seriealizer = serializer(query, many=True)
    return seriealizer