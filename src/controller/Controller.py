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