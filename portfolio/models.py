# portfolio/models.py
from django.db import models

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    ano = models.IntegerField()
    semestre = models.CharField(max_length=10)
    docente = models.CharField(max_length=100)
    moodle_url = models.URLField()
    pagina_uc = models.URLField()

    def __str__(self):
        return f"{self.nome} ({self.ano}/{self.semestre})"

class Tecnologia(models.Model):
    nome = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logos/')
    descricao = models.TextField()
    repositorio = models.URLField(blank=True)

    def __str__(self):
        return self.nome

class Projeto(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    github = models.URLField()
    video_demo = models.URLField(blank=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    tecnologias = models.ManyToManyField(Tecnologia)
    conceito = models.TextField()  # conceitos aplicados
    desafios = models.TextField()  # desafios técnicos

    def __str__(self):
        return self.titulo

class ImagemProjeto(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='projetos/')

class Extras(models.Model):
    projeto = models.OneToOneField(Projeto, on_delete=models.CASCADE)
    info_adicional = models.TextField()
