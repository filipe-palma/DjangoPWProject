# perguntas.py

from datetime import timedelta
from django.db.models import Count, Avg
from bandas.models import Banda, Album, Musica

def pergunta_1():
    # 1. Listar o nome das bandas, ordenadas alfabeticamente.
    bandas = Banda.objects.order_by('nome').values_list('nome', flat=True)
    print("1. Bandas ordenadas alfabeticamente:")
    print(list(bandas), "\n")

def pergunta_2():
    # 2. Listar o nome dos álbuns de uma banda, ordenados cronologicamente.
    # Exemplo: álbuns da banda "Rockers United".
    albuns = Album.objects.filter(banda__nome="Rockers United").order_by('ano_lancamento').values_list('titulo', flat=True)
    print("2. Álbuns da banda 'Rockers United' ordenados cronologicamente:")
    print(list(albuns), "\n")

def pergunta_3():
    # 3. Apresentar todos os álbuns que foram lançados entre dois anos.
    # Exemplo: entre 1990 e 2000.
    albuns = Album.objects.filter(ano_lancamento__gte=1990, ano_lancamento__lte=2000)
    print("3. Álbuns lançados entre 1990 e 2000:")
    for album in albuns:
        print(f"  {album.titulo} - {album.ano_lancamento}")
    print("")

def pergunta_4():
    # 4. Criar uma playlist de um álbum, ou seja, a lista dos links das músicas.
    # Exemplo: álbum "Primeiro Impacto".
    try:
        album = Album.objects.get(titulo="Primeiro Impacto")
    except Album.DoesNotExist:
        print("4. Álbum 'Primeiro Impacto' não encontrado.\n")
        return

    # Considerando que a playlist seja composta, por exemplo, dos links do Spotify (link_spotify)
    links = album.musicas.exclude(link_spotify="").values_list('link_spotify', flat=True)
    print("4. Playlist do álbum 'Primeiro Impacto' (links Spotify):")
    print(list(links), "\n")

def pergunta_5():
    # 5. Listar os álbuns com músicas que durem mais de 5 minutos.
    # Converte 5 minutos para timedelta
    cinco_min = timedelta(minutes=5)
    albuns = Album.objects.filter(musicas__duracao__gt=cinco_min).distinct()
    print("5. Álbuns com pelo menos uma música com duração superior a 5 minutos:")
    for album in albuns:
        print(f"  {album.titulo}")
    print("")

def pergunta_6():
    # 6. Listar todas as músicas que tenham uma determinada palavra no título ou na letra.
    # Exemplo: a palavra "Rebelde"
    palavras = "Rebelde"
    musicas = Musica.objects.filter(titulo__icontains=palavras) | Musica.objects.filter(letra__icontains=palavras)
    print("6. Músicas que contenham a palavra 'Rebelde' no título ou na letra:")
    for musica in musicas.distinct():
        print(f"  {musica.titulo} (álbum: {musica.album.titulo})")
    print("")

def pergunta_7():
    # 7. Listar o número de álbuns por banda.
    bandas = Banda.objects.all().annotate(num_albuns=Count('albuns'))
    print("7. Número de álbuns por banda:")
    for banda in bandas:
        print(f"  {banda.nome}: {banda.num_albuns} álbuns")
    print("")

def pergunta_8():
    # 8. Listar as bandas que foram formadas antes de um dado ano.
    # Exemplo: bandas formadas antes de 1990.
    bandas = Banda.objects.filter(ano_formacao__lt=1990)
    print("8. Bandas formadas antes de 1990:")
    for banda in bandas:
        print(f"  {banda.nome} - {banda.ano_formacao}")
    print("")

def pergunta_9():
    # 9. Listar a duração média das músicas por álbum.
    albuns = Album.objects.annotate(avg_duracao=Avg('musicas__duracao'))
    print("9. Duração média das músicas por álbum:")
    for album in albuns:
        print(f"  {album.titulo}: {album.avg_duracao}")
    print("")

def pergunta_10():
    # 10. Listar as top 3 bandas com o maior número de músicas.
    bandas = Banda.objects.annotate(num_musicas=Count('albuns__musicas')).order_by('-num_musicas')[:3]
    print("10. Top 3 bandas com mais músicas:")
    for banda in bandas:
        print(f"  {banda.nome}: {banda.num_musicas} músicas")
    print("")

print("### Respostas às Queries com ORM ###\n")
pergunta_1()
pergunta_2()
pergunta_3()
pergunta_4()
pergunta_5()
pergunta_6()
pergunta_7()
pergunta_8()
pergunta_9()
pergunta_10()
