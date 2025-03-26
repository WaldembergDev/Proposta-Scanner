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
  (3354, 2025, 'THELIO MOREIRA LIMA', 0, 'Aprovado', 'Comercial 1'),
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

# for resultado in lista_teste:
#   # caresultados que deverão ser ignorados
#   if resultado[5] == 'Comercial 7' \
#     or resultado[4] == 'Em aprovação' \
#       or resultado[4] == 'Em análise crítica':
#     continue
#   # definir os arquivos/pastas que deverão ser procurados
#   arquivos_padroes = [False, False] # geral - solic, prop
#   revisoes = [[False, False] for i in range(resultado[3])] # proposta, solicitação
#   if resultado[0] != 'C&M SERVIÇOS AMBIENTAIS':
#     arquivos_qualy = [False, False] # Caso qualylab - aprovação, condições comerciais
#   # Salvando os dados em uma variável mais amigável
#   ano = resultado[1]
#   os = resultado[0]
#   pasta_existe = encontrar_pasta(ano, os)
#   print(f'OS: {os} - {pasta_existe}')
    
  
  