import streamlit as st
from src.controller.Controller import ControllerConsulta
from datetime import datetime, time

st.header('Busca de OS', divider=True)

# definindo duas colunas
col1, col2 = st.columns(2)

with col1:
  data_inicial = st.date_input('Selecione a data inicial', format='DD/MM/YYYY')
  data_inicial = datetime.combine(data_inicial, time(0,0,0,0))

with col2:
  data_final = st.date_input('Selcione a data final', format='DD/MM/YYYY')
  data_final = datetime.combine(data_final, time(23,0,0,0))

btn_pesquisar = st.button('Pesquisar')
if btn_pesquisar:
  resultados = ControllerConsulta.obter_dados(data_inicial, data_final)
  lista_pendencia = ControllerConsulta.obter_lista_pendencias(resultados)
  dataframe = ControllerConsulta.gerar_dataframe(lista_pendencia)
  st.dataframe(dataframe)



