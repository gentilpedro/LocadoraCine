import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

API_URL = "http://localhost:3000/filmes"

st.title("🎬 Filmes")

# Cadastro
st.header("📋 Cadastrar Novo Filme")
with st.form("form_filme"):
    modelo = st.text_input("Modelo")
    marca = st.text_input("Marca")
    ano = st.number_input("Ano", min_value=1900, max_value=2100, step=1)
    disponivel = st.checkbox("Disponível", value=True)

    submit = st.form_submit_button("Cadastrar")
    if submit and modelo and marca:
        response = requests.post(API_URL, json={
            "modelo": modelo,
            "marca": marca,
            "ano": ano,
            "disponivel": disponivel
        })
        if response.status_code == 200:
            st.success("✅ Filme cadastrado com sucesso!")
        else:
            st.error("❌ Erro ao cadastrar filme")

# Listagem
st.header("📄 Lista de Filmes")

try:
    response = requests.get(API_URL)
    if response.status_code == 200 and response.text.strip():
        filmes = response.json()
    else:
        filmes = []

    df = pd.DataFrame(filmes)

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        # Exclusão
        st.subheader("❌ Excluir Filme")
        filmes_opcoes = {f"{f['modelo']} ({f['marca']})": f["id"] for f in filmes}
        opcao_exclusao = st.selectbox("Selecione um filme para excluir", list(filmes_opcoes.keys()))
        if st.button("Excluir Filme"):
            id_filme = filmes_opcoes[opcao_exclusao]
            del_resp = requests.delete(f"{API_URL}/{id_filme}")
            if del_resp.status_code == 200:
                st.success("🗑️ Filme excluído com sucesso!")
                st.experimental_rerun()
            else:
                st.error("❌ Erro ao excluir filme.")
    else:
        st.warning("Nenhum filme cadastrado ainda.")

except Exception as e:
    st.error(f"Erro ao buscar filmes: {e}")

# Gráfico
st.header("📊 Gráfico: Quantidade de Filmes por Marca")
if 'df' in locals() and not df.empty:
    marca_count = df['marca'].value_counts()
    fig, ax = plt.subplots()
    marca_count.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_xlabel("Quantidade de Filmes")
    ax.set_ylabel("Marca")
    st.pyplot(fig)
else:
    st.info("Não há dados suficientes para gerar o gráfico.")
