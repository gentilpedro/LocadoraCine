import streamlit as st
import requests
import pandas as pd
from collections import Counter
from datetime import datetime
import altair as alt

API_BASE = "http://localhost:3000"  # ajuste sua URL da API

st.title("📊 Dados da Locadora Avenida")

# Buscar clientes
try:
    resp_clientes = requests.get(f"{API_BASE}/clientes")
    clientes = resp_clientes.json() if resp_clientes.status_code == 200 and resp_clientes.text.strip() else []
except Exception:
    clientes = []

if clientes:
    st.metric("Clientes cadastrados", len(clientes))
else:
    st.warning("Nenhum cliente cadastrado.")

# Buscar filmes
try:
    resp_filmes = requests.get(f"{API_BASE}/filmes")
    filmes = resp_filmes.json() if resp_filmes.status_code == 200 and resp_filmes.text.strip() else []
except Exception:
    filmes = []

if filmes:
    st.metric("Filmes cadastrados", len(filmes))
else:
    st.warning("Nenhum filme cadastrado.")

# Buscar reservas
try:
    resp_reservas = requests.get(f"{API_BASE}/reservas")
    reservas = resp_reservas.json() if resp_reservas.status_code == 200 and resp_reservas.text.strip() else []
except Exception:
    reservas = []

if reservas:
    meses = [datetime.fromisoformat(r['dataInicio']).strftime("%Y-%m") for r in reservas]
    contagem_meses = Counter(meses)
    df_reservas_mes = pd.DataFrame(contagem_meses.items(), columns=["Mês", "Reservas"])
    df_reservas_mes["Mês"] = pd.to_datetime(df_reservas_mes["Mês"]).dt.strftime("%B %Y")
    df_reservas_mes = df_reservas_mes.sort_values("Reservas", ascending=True)

    st.subheader("Reservas por mês")

    chart = alt.Chart(df_reservas_mes).mark_bar().encode(
        x=alt.X("Reservas:Q"),
        y=alt.Y("Mês:N", sort=None),
        tooltip=["Mês", "Reservas"]
    ).properties(height=300)

    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("Nenhuma reserva encontrada.")
