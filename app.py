import streamlit as st
from pathlib import Path

# Tela principal
pagina_principal = st.Page(Path(r'src\views\principal.py'), title='Principal')

pagina = st.navigation([pagina_principal])

pagina.run()