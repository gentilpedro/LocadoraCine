import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:3000/clientes"

st.title("👤 Clientes")

# Cadastro / Atualização
st.header("📋 Cadastrar ou Atualizar Cliente")
with st.form("form_cliente"):
    cliente_id = st.text_input("ID do cliente (deixe vazio para novo)")
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    telefone = st.text_input("Telefone")
    submitted = st.form_submit_button("Salvar")

    if submitted:
        cliente_data = {"nome": nome, "email": email, "telefone": telefone}
        if cliente_id:
            response = requests.put(f"{API_URL}/{cliente_id}", json=cliente_data)
            if response.status_code == 200:
                st.success("✅ Cliente atualizado com sucesso!")
            else:
                st.error("❌ Erro ao atualizar cliente.")
        else:
            response = requests.post(API_URL, json=cliente_data)
            if response.status_code == 200:
                st.success("✅ Cliente cadastrado com sucesso!")
            else:
                st.error("❌ Erro ao cadastrar cliente.")

# Listagem
st.header("📄 Lista de Clientes")
try:
    response = requests.get(API_URL)
    if response.status_code == 200 and response.text.strip():
        clientes = response.json()
    else:
        clientes = []

    df = pd.DataFrame(clientes)


    if not df.empty:
        # Filtros
        st.subheader("🔍 Filtro por nome ou email")
        col1, col2 = st.columns(2)
        with col1:
            filtro_nome = st.text_input("Filtrar por nome")
        with col2:
            filtro_email = st.text_input("Filtrar por email")

        if filtro_nome:
            df = df[df["nome"].str.contains(filtro_nome, case=False)]
        if filtro_email:
            df = df[df["email"].str.contains(filtro_email, case=False)]

        st.dataframe(df, use_container_width=True)

        # Seleção para exclusão
        st.subheader("🗑️ Excluir Cliente")
        nomes = {f"{row['nome']} ({row['email']})": row["id"] for _, row in df.iterrows()}
        cliente_selecionado = st.selectbox("Selecione um cliente para excluir", list(nomes.keys()))
        id_cliente = nomes[cliente_selecionado]
        if st.button("Excluir Cliente"):
            del_resp = requests.delete(f"{API_URL}/{id_cliente}")
            if del_resp.status_code == 200:
                st.success("Cliente excluído com sucesso!")
                st.experimental_rerun()
            else:
                st.error("Erro ao excluir cliente.")

    else:
        st.info("Nenhum cliente encontrado.")

except Exception as e:
    st.error(f"Erro ao conectar com a API: {e}")

# Enviar email
st.header("✉️ Enviar Relatório por Email")
if not df.empty:
    clientes_opcoes = {f"{c['nome']} ({c['email']})": c['id'] for c in clientes}
    cliente_email = st.selectbox("Selecione o cliente para enviar email", list(clientes_opcoes.keys()))

    if st.button("Enviar email"):
        try:
            resp = requests.post(f"http://localhost:3000/send-email/{clientes_opcoes[cliente_email]}")
            if resp.status_code == 200:
                st.success("✅ Email enviado com sucesso!")
            else:
                st.error(f"❌ Falha ao enviar email: {resp.json().get('error')}")
        except Exception as e:
            st.error(f"Erro ao enviar email: {e}")
