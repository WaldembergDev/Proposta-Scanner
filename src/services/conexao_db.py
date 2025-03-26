import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Caminho
caminho = Path().resolve() / '.venv' / '.env'

# Carregando variáveis de ambiente
load_dotenv(dotenv_path=caminho)

# Dados da conexão
connection_string = (
    "DRIVER={SQL Server};"
    f"SERVER={os.environ['SERVER']};"
    f"DATABASE={os.environ['DATABASE']};"
    f"UID={os.environ['USUARIO']};"
    f"PWD={os.environ['PASSWORD']};"
    f"Port={os.environ['PORT']};"
)

# Conectar ao banco de dados
def obter_dados_QL(data_inicial: datetime, data_final: datetime):
  try:
      connection = pyodbc.connect(connection_string)
      
      cursor = connection.cursor()
      
      query = """SELECT O.Numero, O.Ano, C.nome AS Solicitante, ISNULL(O.revisao, 0) AS Revisão,

CASE

  WHEN O.situacao = 1 THEN 'Em análise crítica'

  WHEN O.situacao = 2 THEN 'Em aprovação'

  WHEN O.situacao = 3 THEN 'Aprovado'

  WHEN O.situacao = 4 THEN 'Reprovado interno'

  WHEN O.situacao = 5 THEN 'Reprovado cliente'

END AS Situação, ISNULL(U.nome, '') AS Comercial

FROM Orcamentos O

LEFT OUTER JOIN Usuarios U ON (U.id_usuario = O.contato_comercial)

LEFT OUTER JOIN Clientes C ON (C.id_cliente = O.id_solicitante)

WHERE O.criacao BETWEEN ? AND ?;"""
      
      cursor.execute(query, (data_inicial, data_final))
      resultados = cursor.fetchall()
      
      # Fechando a conexão
      connection.close()

      return resultados

  except pyodbc.Error as e:
      print(f"Erro na conexão: {e}")
