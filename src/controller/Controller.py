from src.services import conexao_db as cd
from pathlib import Path
import unicodedata
import re
import pandas as pd
from datetime import datetime

class ControllerConsulta:  
  @classmethod
  def obter_dados(cls, data_inicial: datetime, data_final: datetime):
    resultados = cd.obter_dados_QL(data_inicial, data_final)
    return resultados

  @classmethod
  def obter_numeros(cls, texto: str):
    compilado = re.compile(r'\d+')
    resultados = compilado.findall(texto)
    if not resultados:
      return resultados
    # transfornmando todos os valores encontrados em números inteiros
    resultados_convertidos = list(map(int, resultados))
    return resultados_convertidos

  @classmethod
  def normalizar_nome(cls, nome: str):
    # sistema de automação busca de OS
      return unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore').decode('ascii').lower()
  
  @classmethod
  def encontrar_pasta(cls, ano: int, os: int):
    caminho = Path(r'Z:\QUALYLAB\Q-COMERCIAL')
    caminho_ano = caminho / f'OS {ano}'
    for pasta in caminho_ano.iterdir():
      OSs_pasta = ControllerConsulta.obter_numeros(pasta.name)
      if os in OSs_pasta:
        return pasta
    return False
  
  @classmethod
  def configurar_arquivos(cls, lista_arquivos: list):
    lista_configurada = [(arquivo, False) for arquivo in lista_arquivos]
    return lista_configurada
  
  @classmethod
  def configurar_revisoes(cls, lista_revisoes: list):
    revisoes = []
    for (proposta, solicitacao) in lista_revisoes:
      revisoes.append(proposta)
      revisoes.append(solicitacao)
    return revisoes
  
  @classmethod
  def procurar_arquivos(cls, arquivos: list, caminho_procurado: Path):
    lista_arquivos = cls.configurar_arquivos(arquivos)
    for i, (arq, valor) in enumerate(lista_arquivos):
      for arquivo in caminho_procurado.iterdir():
        nome_ajustado = cls.normalizar_nome(arquivo.name)
        if arq in nome_ajustado:
          lista_arquivos[i] = (arq, True)
          continue
    return lista_arquivos
  
  @classmethod
  def gerar_lista_pendencia(cls, lista_arquivos: list):
    pendencias = []
    for (os, ano, cliente, resultado) in lista_arquivos:
      for pendencia in resultado:
        if pendencia[1] == False:
          pendencias.append((os, ano, cliente, pendencia[0]))
    return pendencias
  
  @classmethod
  def obter_lista_pendencias(cls, lista: list):
    lista_verificacao = []
    for resultado in lista:
      # caresultados que deverão ser ignorados
      if resultado[5] == 'Comercial 7' \
        or resultado[4] == 'Em aprovação' \
          or resultado[4] == 'Em análise crítica':
        continue
      # definir os arquivos/pastas que deverão ser procurados
      arquivos_procurados = ['solicitacao', 'proposta'] # caso geral - solic, prop
      if resultado[2] != 'C&M SERVICOS AMBIENTAIS':
        arquivos_procurados += ['condicoes comerciais'] # Caso qualy
      if resultado[4] == 'Aprovado':
         arquivos_procurados += ['aprovacao']
      # definir as revisões que serão procuradadas
      revisoes = [(f'proposta rev{i+1}', f'solicitacao rev{i+1}') for i in range(resultado[3])] # proposta, solicitação
      if revisoes:
        lista_revisoes = cls.configurar_revisoes(revisoes)
        arquivos_procurados += lista_revisoes
      # Salvando os dados em uma variável mais amigável
      ano = resultado[1]
      os = resultado[0]
      empresa = resultado[2]
      pasta = cls.encontrar_pasta(ano, os)
      if not pasta:
        arquivos_encontrados = cls.configurar_arquivos(arquivos_procurados) # definindo como todos False
      if pasta:
        arquivos_encontrados = cls.procurar_arquivos(arquivos_procurados, pasta)
        pasta = True
      arquivos_encontrados.insert(0, ('pasta', pasta))
      lista_verificacao.append((os, ano, empresa, arquivos_encontrados))
    lista_pendencias = cls.gerar_lista_pendencia(lista_verificacao)
    return lista_pendencias
  
  @classmethod
  def gerar_dataframe(cls, lista: list):
    dataframe = pd.DataFrame(lista, columns=['OS', 'Ano', 'Cliente', 'Pendência'])
    return dataframe