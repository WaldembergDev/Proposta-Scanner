from pathlib import Path
import unicodedata
import re
import pandas as pd
from src.controller.Controller import ControllerConsulta
from datetime import datetime, timedelta

from src.controller.Controller import ControllerConsulta
from src.services import conexao_db
from datetime import datetime, timedelta

lista_teste = [
  (3643, 2025, 'ACX CONTROLE DE PRAGAS LTDA', 0, 'Aprovado', 'Comercial 7'),
  (3644, 2025, 'ETICA ENGENHARIA E SOLUCOES AMBIENTAIS LTDA ', 0, 'Aprovado', 'Comercial 1'),
  (3645, 2025, 'VETO VETORES COMERCIO E SERVIÇOS LTDA', 0, 'Aprovado', 'Comercial 7'),
  (3646, 2025, 'RS RODRIGUES DESENTUPIDORA E DEDETIZADORA LTDA', 0, 'Aprovado', 'Comercial 7'),
  (3647, 2025, 'RS RODRIGUES DESENTUPIDORA E DEDETIZADORA LTDA', 0, 'Aprovado', 'Comercial 7'),
  (3648, 2025, 'RS RODRIGUES DESENTUPIDORA E DEDETIZADORA LTDA', 0, 'Aprovado', 'Comercial 7'),
  (3649, 2025, 'APS SOLUCOES COMERCIO E SERVICO LTDA', 0, 'Aprovado', 'Comercial 7'),
  (3650, 2025, 'THELIO MOREIRA LIMA', 0, 'Em aprovação', 'Comercial 1')
]

# Caminho dos arquivos
caminho = Path(r'Z:\QUALYLAB\Q-COMERCIAL')

# verificar se existe pasta
for os in lista_teste:
  # casos que deverão ser ignorados
  if os[5] == 'Comercial 7' or os[4] == 'Em aprovação' or os[4] == 'Em análise crítica':
    continue
  