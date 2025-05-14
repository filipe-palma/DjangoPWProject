from django.db import models

class Banda(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='bandas/fotos/', blank=True, null=True)
    ano_formacao = models.IntegerField()
    descricao = models.TextField(blank=True)
    genero = models.CharField(max_length=50)
    pais_origem = models.CharField(max_length=50)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Banda'
        verbose_name_plural = 'Bandas'

class Album(models.Model):
    titulo = models.CharField(max_length=100)
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE, related_name='albuns')
    capa = models.ImageField(upload_to='bandas/capas/', blank=True, null=True)
    ano_lancamento = models.IntegerField()
    gravadora = models.CharField(max_length=100, blank=True)
    descricao = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.banda.nome}"

    class Meta:
        verbose_name = 'Álbum'
        verbose_name_plural = 'Álbuns'

class Musica(models.Model):
    titulo = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='musicas')
    duracao = models.DurationField(blank=True, null=True)
    ordem = models.IntegerField()
    letra = models.TextField(blank=True)
    link_spotify = models.URLField(blank=True)
    link_youtube = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.album.banda.nome}"

    class Meta:
        verbose_name = 'Música'
        verbose_name_plural = 'Músicas'
        ordering = ['album', 'ordem']