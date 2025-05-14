import json
from datetime import timedelta
from bandas.models import Banda, Album, Musica

def importar_bandas(arquivo):
    """
    Importa bandas do ficheiro JSON para o modelo Banda.
    """
    with open(arquivo, 'r', encoding='utf-8') as f:
        bandas_data = json.load(f)

    for banda in bandas_data:
        obj, created = Banda.objects.update_or_create(
            nome=banda.get('nome'),
            defaults={
                'ano_formacao': banda.get('ano_formacao'),
                'genero': banda.get('genero'),
                'pais_origem': banda.get('pais_origem'),
                'descricao': banda.get('descricao', ''),
                'website': banda.get('website', '')
            }
        )
        if created:
            print(f'Banda criada: {obj.nome}')
        else:
            print(f'Banda atualizada: {obj.nome}')

def importar_disco_musicas(arquivo):
    """
    Importa discos (álbuns) e suas músicas do ficheiro JSON para os modelos Album e Musica.
    """
    with open(arquivo, 'r', encoding='utf-8') as f:
        discos_data = json.load(f)

    for disco in discos_data:
        # Recupera a banda associada pelo nome
        try:
            banda = Banda.objects.get(nome=disco.get('banda'))
        except Banda.DoesNotExist:
            print(f"Banda não encontrada para o álbum '{disco.get('titulo')}'. Pulando este registro.")
            continue

        album, created = Album.objects.update_or_create(
            titulo=disco.get('titulo'),
            banda=banda,
            defaults={
                'ano_lancamento': disco.get('ano_lancamento')
            }
        )
        if created:
            print(f'Álbum criado: {album.titulo}')
        else:
            print(f'Álbum atualizado: {album.titulo}')

        # Importa as músicas associadas ao álbum.
        for ordem, musica in enumerate(disco.get('musicas', []), start=1):
            # Conversão de string para timedelta (formato MM:SS ou HH:MM:SS)
            duracao_str = musica.get('duracao', '')
            duracao = None
            if duracao_str:
                try:
                    partes = duracao_str.split(':')
                    if len(partes) == 2:
                        minutos, segundos = map(int, partes)
                        duracao = timedelta(minutes=minutos, seconds=segundos)
                    elif len(partes) == 3:
                        horas, minutos, segundos = map(int, partes)
                        duracao = timedelta(hours=horas, minutes=minutos, seconds=segundos)
                except Exception as e:
                    print(f"Erro convertendo duração '{duracao_str}' para a música '{musica.get('titulo')}': {e}")

            musica_obj, created_musica = Musica.objects.update_or_create(
                titulo=musica.get('titulo'),
                album=album,
                defaults={
                    'duracao': duracao,
                    'ordem': ordem,
                    'letra': "",            # Atualize se houver letra
                    'link_spotify': "",     # Atualize se disponível
                    'link_youtube': ""      # Atualize se disponível
                }
            )
            if created_musica:
                print(f'  Música criada: {musica_obj.titulo}')
            else:
                print(f'  Música atualizada: {musica_obj.titulo}')

def importar_curso(bandas_file, discos_file):
    """
    Executa a importação de bandas e discos (com músicas).

    Parâmetros:
       bandas_file: caminho para o JSON de bandas.
       discos_file: caminho para o JSON de discos.
    """
    print("Importando Bandas...")
    importar_bandas(bandas_file)
    print("Importando Discos e Músicas...")
    importar_disco_musicas(discos_file)
    print("Importação concluída.")
