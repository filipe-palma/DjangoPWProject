from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse

class Autor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    foto = models.ImageField(upload_to='artigos/autores/', blank=True, null=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Tag(models.Model):
    nome = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class Artigo(models.Model):
    STATUS_CHOICES = (
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
    )

    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='artigos')
    conteudo = models.TextField()
    imagem_capa = models.ImageField(upload_to='artigos/capas/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    data_publicacao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='rascunho')
    categorias = models.ManyToManyField(Categoria, related_name='artigos')
    tags = models.ManyToManyField(Tag, related_name='artigos', blank=True)
    tempo_leitura = models.PositiveIntegerField(help_text='Tempo estimado de leitura em minutos', default=5)
    destaque = models.BooleanField(default=False, help_text='Artigo em destaque na página inicial')
    fonte_original = models.URLField(blank=True, help_text='URL da fonte original do artigo, se aplicável')

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # usa o namespace 'artigos' + nome da rota 'artigo-detail'
        return reverse('artigos:artigo-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'
        ordering = ['-data_publicacao', '-data_criacao']

class Comentario(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comentarios')
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    aprovado = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='respostas')

    def __str__(self):
        return f'Comentário de {self.nome} em {self.artigo.titulo}'

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['data_criacao']

class Avaliacao(models.Model):
    PONTUACAO_CHOICES = (
        (1, '1 - Fraco'),
        (2, '2 - Regular'),
        (3, '3 - Bom'),
        (4, '4 - Muito Bom'),
        (5, '5 - Excelente'),
    )

    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='avaliacoes')
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    pontuacao = models.IntegerField(choices=PONTUACAO_CHOICES)
    comentario = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Avaliação de {self.nome} para {self.artigo.titulo}: {self.pontuacao}'

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        # Cada usuário só pode avaliar um artigo uma vez (por email)
        unique_together = ('artigo', 'email')