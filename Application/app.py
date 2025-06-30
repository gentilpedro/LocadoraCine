import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
banner_path = os.path.join(BASE_DIR, 'assets', 'banner.png')  # só 'assets' porque já está dentro de Application

st.image(banner_path, use_container_width=True)

st.title("🎥 Locadora Avenida")

st.markdown("""
Bem-vindo à **Locadora Avenida**, seu destino para os melhores filmes!  
Aqui você pode gerenciar filmes, clientes, reservas e enviar relatórios por email.

Use o menu lateral para navegar entre as páginas.
""")

