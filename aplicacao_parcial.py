import unicodedata
import re
import pandas as pd
from src.controller.Controller import ControllerConsulta
from datetime import datetime, timedelta
from src.services import conexao_db
from pathlib import Path

lista_teste = [
  (3643, 2025, 'ACX CONTROLE DE PRAGAS LTDA', 0, 'Aprovado', 'Comercial 7'),
  (3644, 2025, 'ETICA ENGENHARIA E SOLUCOES AMBIENTAIS LTDA ', 0, 'Aprovado', 'Comercial 1'),
  (3645, 2025, 'VETO VETORES COMERCIO E SERVIÇOS LTDA', 0, 'Aprovado', 'Comercial 7'),
  (3646, 2025, 'RS RODRIGUES DESENTUPIDORA E DEDETIZADORA LTDA', 0, 'Aprovado', 'Comercial 7'),
  (3647, 2025, 'RS RODRIGUES DESENTUPIDORA E DEDETIZADORA LTDA', 0, 'Aprovado', 'Comercial 7'),
  (3648, 2025, 'RS RODRIGUES DESENTUPIDORA E DEDETIZADORA LTDA', 0, 'Aprovado', 'Comercial 7'),
  (3649, 2025, 'APS SOLUCOES COMERCIO E SERVICO LTDA', 0, 'Aprovado', 'Comercial 7'),
  (3650, 2025, 'THELIO MOREIRA LIMA', 0, 'Em aprovação', 'Comercial 1'),
  (3730, 2025, 'THELIO MOREIRA LIMA', 0, 'Aprovado', 'Comercial 1'),
  (593, 2025, 'THELIO MOREIRA LIMA', 0, 'Aprovado', 'Comercial 2'),
]

# Caminho dos arquivos
caminho = Path(r'Z:\QUALYLAB\Q-COMERCIAL')

# verificando se a pasta da proposta existe
def encontrar_pasta(ano: int, os: int):
  caminho = Path(r'Z:\QUALYLAB\Q-COMERCIAL')
  caminho_ano = caminho / f'OS {ano}'
  for pasta in caminho_ano.iterdir():
    OSs_pasta = ControllerConsulta.obter_numeros(pasta.name)
    if os in OSs_pasta:
      return pasta
  return False

def normalizar_nome(nome: str):
    # sistema de automação busca de OS
      return unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore').decode('ascii').lower()

def configurar_arquivos(lista_arquivos: list):
  lista_configurada = [(arquivo, False) for arquivo in lista_arquivos]
  return lista_configurada

def configurar_revisoes(lista_revisoes: list):
  revisoes = []
  for (proposta, solicitacao) in lista_revisoes:
    revisoes.append(proposta)
    revisoes.append(solicitacao)
  return revisoes

def procurar_arquivos(arquivos: list, caminho_procurado: Path):
  lista_arquivos = configurar_arquivos(arquivos)
  for i, (arq, valor) in enumerate(lista_arquivos):
    for arquivo in caminho_procurado.iterdir():
      nome_ajustado = normalizar_nome(arquivo.name)
      if arq in nome_ajustado:
        lista_arquivos[i] = (arq, True)
        continue
  return lista_arquivos

def gerar_lista_pendencia(lista_arquivos: list):
  pendencias = []
  for (os, ano, cliente, resultado) in lista_arquivos:
    for pendencia in resultado:
      if pendencia[1] == False:
        pendencias.append((os, ano, cliente, pendencia[0]))
  return pendencias

def obter_lista_pendencias(lista: list):
  lista_verificacao = []
  for resultado in lista:
    # caresultados que deverão ser ignorados
    if resultado[5] == 'Comercial 7' \
      or resultado[4] == 'Em aprovação' \
        or resultado[4] == 'Em análise crítica':
      continue
    # definir os arquivos/pastas que deverão ser procurados
    arquivos_procurados = ['solicitacao', 'proposta'] # caso geral - solic, prop
    if resultado[2] != 'C&M SERVIÇOS AMBIENTAIS':
      arquivos_procurados += ['aprovacao', 'condicoes comerciais'] # Caso qualy 
    # definir as revisões que serão procuradadas
    revisoes = [(f'proposta rev{i+1}', f'solicitacao rev{i+1}') for i in range(resultado[3])] # proposta, solicitação
    if revisoes:
      lista_revisoes = configurar_revisoes(revisoes)
      arquivos_procurados += lista_revisoes
    # Salvando os dados em uma variável mais amigável
    ano = resultado[1]
    os = resultado[0]
    empresa = resultado[2]
    pasta = encontrar_pasta(ano, os)
    if not pasta:
      arquivos_encontrados = configurar_arquivos(arquivos_procurados) # definindo como todos False
    if pasta:
      arquivos_encontrados = procurar_arquivos(arquivos_procurados, pasta)
      pasta = True
    arquivos_encontrados.insert(0, ('pasta', pasta))
    lista_verificacao.append((os, ano, empresa, arquivos_encontrados))
  lista_pendencias = gerar_lista_pendencia(lista_verificacao)
  return lista_pendencias

