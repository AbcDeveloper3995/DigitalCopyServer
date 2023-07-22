from django.db import models

from apps.audiovisual.choices import CHOICE_GENERO, CHOICE_ESTADO


class AudiovisualBase(models.Model):
    titulo = models.CharField(verbose_name='Titulo', max_length=250, null=True, blank=True)
    sinopsis = models.TextField(verbose_name='Sinopsis', null=True, blank=True)
    elenco_principal = models.CharField(verbose_name='Elenco Principal', max_length=250, blank=True, null=True)
    likes = models.PositiveIntegerField(verbose_name='Likes', default=0, null=True, blank=True)
    ano_lanzamiento = models.PositiveIntegerField(verbose_name='Año de Lanzamiento', null=True, blank=True)
    tiempo = models.CharField(verbose_name='Tiempo de duracion', max_length=50, null=True, blank=True)
    image = models.ImageField(verbose_name='Imagen', upload_to='backendImg/', null=True, blank=True)
    image_url = models.URLField(verbose_name='ImgUrl', unique=True, blank=True, null=True)

    class Meta:
        abstract = True

class Pelicula(AudiovisualBase):
    genero = models.CharField(verbose_name='Genero', max_length=50, choices=CHOICE_GENERO, blank=True, null=True)
    url_thriller = models.URLField(verbose_name='Triller', unique=True, blank=True, null=True)
    es_estreno = models.BooleanField(verbose_name='Es estreno', default=False)

    class Meta:
        db_table = 'Pelicula'
        verbose_name = 'Pelicula'
        verbose_name_plural = 'Peliculas'

    def __str__(self):
        return f'{self.titulo}.'

class Serie(AudiovisualBase):
    genero = models.CharField(verbose_name='Genero', max_length=50, choices=CHOICE_GENERO, blank=True, null=True)
    estado = models.CharField(verbose_name='Estado', max_length=5, choices=CHOICE_ESTADO, blank=True, null=True)

    class Meta:
        db_table = 'Serie'
        verbose_name = 'Serie'
        verbose_name_plural = 'Serie'

    def __str__(self):
        return f'{self.titulo}.'

class Novela(AudiovisualBase):
    url_thriller = models.URLField(verbose_name='Triller', max_length=250, unique=True, blank=True, null=True)
    estado = models.CharField(verbose_name='Estado', max_length=5, choices=CHOICE_ESTADO, blank=True, null=True)
    pais = models.CharField(verbose_name='Pais', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Novela'
        verbose_name = 'Novela'
        verbose_name_plural = 'Novelas'

    def __str__(self):
        return f'{self.titulo}.'

class Temporada(models.Model):
    fk_serie = models.ForeignKey(Serie, verbose_name='Serie', blank=True, null=True, on_delete=models.CASCADE)
    url_thriller = models.URLField(verbose_name='Triller', max_length=250, unique=True, blank=True, null=True)
    numero = models.PositiveIntegerField(verbose_name='Numero', blank=True, null=True)

    class Meta:
        db_table = 'Temporada'
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'

    def __str__(self):
        return f' Temporada {self.numero} de {self.fk_serie.titulo}.'

    def get_url(self):
        if self.url_thriller != None:
            return self.url_thriller
        return None

class Capitulo(models.Model):
    fk_temporada = models.ForeignKey(Temporada, verbose_name='Temporada', blank=True, null=True, on_delete=models.CASCADE)
    fk_novela = models.ForeignKey(Novela, verbose_name='Novela', blank=True, null=True, on_delete=models.CASCADE)
    numero = models.PositiveIntegerField(verbose_name='Numero', blank=True, null=True)
    class Meta:
        db_table = 'Capitulo'
        verbose_name = 'Capitulo'
        verbose_name_plural = 'Capitulos'

    def __str__(self):
        if self.fk_temporada == None:
            return f'Capitulo {self.numero} de la novela {self.fk_novela.titulo}.'
        return f'Capitulo {self.numero} de la temporada {self.fk_temporada.numero} de la serie {self.fk_temporada.fk_serie.titulo}.'

class Comentario(models.Model):
    fk_pelicula = models.ForeignKey(Pelicula, verbose_name='Pelicula ', blank=True, null=True,
                                       on_delete=models.CASCADE)
    fk_serie = models.ForeignKey(Serie, verbose_name='Serie ', blank=True, null=True,
                                   on_delete=models.CASCADE)
    fk_novela = models.ForeignKey(Novela, verbose_name='Novela ', blank=True, null=True,
                                     on_delete=models.CASCADE)
    fechaCreado = models.DateField(verbose_name='Fecha creado', auto_now=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=150, blank=True, null=True)
    comentario = models.TextField(verbose_name='Comentario', null=True, blank=True)

    class Meta:
        db_table = 'Comentario'
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'FC: {self.nombre} - {self.comentario}.'