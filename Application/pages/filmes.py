import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

API_URL = "http://localhost:3000/filmes"

st.title("🎬 Filmes")

# Cadastro
st.header("📋 Cadastrar Novo Filme")
with st.form("form_filme"):
    titulo = st.text_input("Título")
    genero = st.text_input("Gênero")
    ano = st.number_input("Ano", min_value=1700, max_value=2100, step=1)
    disponivel = st.checkbox("Disponível", value=True)

    submit = st.form_submit_button("Cadastrar")
    if submit:
        if not titulo or not genero:
            st.error("Por favor, preencha título e gênero.")
        else:
            response = requests.post(API_URL, json={
                "titulo": titulo,
                "genero": genero,
                "ano": ano,
                "disponivel": disponivel
            })
            if response.status_code == 200:
                if response.status_code == 200:
                    st.success("✅ Filme cadastrado com sucesso!")

                    st.rerun()
            else:
                st.error(f"❌ Erro ao cadastrar filme: {response.text}")

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
        # Mostrar colunas relevantes e corrigir nomes para exibir
        df_display = df.rename(columns={
            "titulo": "Título",
            "genero": "Gênero",
            "ano": "Ano",
            "disponivel": "Disponível"
        })[["Título", "Gênero", "Ano", "Disponível"]]

        st.dataframe(df_display, use_container_width=True)

        # Exclusão
        st.subheader("❌ Excluir Filme")
        filmes_opcoes = {f"{f['titulo']} ({f['genero']})": f["id"] for f in filmes}
        opcao_exclusao = st.selectbox("Selecione um filme para excluir", list(filmes_opcoes.keys()))
        if st.button("Excluir Filme"):
            id_filme = filmes_opcoes[opcao_exclusao]
            del_resp = requests.delete(f"{API_URL}/{id_filme}")
            if del_resp.status_code == 200:
                st.success("🗑️ Filme excluído com sucesso!")
                st.rerun()
            else:
                st.error("❌ Erro ao excluir filme.")
    else:
        st.warning("Nenhum filme cadastrado ainda.")

    st.header("📊 Gráfico: Quantidade de Filmes por Gênero")
    if not df.empty:
        genero_count = df['genero'].value_counts()
        fig, ax = plt.subplots()
        genero_count.plot(kind='barh', ax=ax, color='skyblue')
        ax.set_xlabel("Quantidade de Filmes")
        ax.set_ylabel("Gênero")
        st.pyplot(fig)
    else:
     st.info("Não há dados suficientes para gerar o gráfico.")

except Exception as e:
    st.error(f"Erro ao buscar filmes: {e}")

# Gráfico


def reset_form():
    st.session_state['titulo'] = ""
    st.session_state['genero'] = ""
    st.session_state['ano'] = ""
    st.session_state['disponivel'] = True
