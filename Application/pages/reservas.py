import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

API_BASE = "http://localhost:3000"

st.title("📆 Reservas")

# Buscar clientes e filmes disponíveis
def buscar_clientes():
    try:
        r = requests.get(f"{API_BASE}/clientes")
        return r.json()
    except:
        return []

def buscar_filmes_disponiveis():
    try:
        r = requests.get(f"{API_BASE}/filmes")
        filmes = r.json()
        return [f for f in filmes if f["disponivel"]]
    except:
        return []

# Cadastro
st.header("📋 Nova Reserva")
clientes = buscar_clientes()
filmes = buscar_filmes_disponiveis()

if clientes and filmes:
    cliente_opcoes = {f"{c['nome']} ({c['email']})": c["id"] for c in clientes}
    filme_opcoes = {f"{f['modelo']} ({f['marca']})": f["id"] for f in filmes}

    with st.form("nova_reserva"):
        cliente_selecionado = st.selectbox("Cliente", list(cliente_opcoes.keys()))
        filme_selecionado = st.selectbox("Filme disponível", list(filme_opcoes.keys()))
        data_inicio = st.date_input("Data de início", value=datetime.today())
        data_fim = st.date_input("Data de término", value=datetime.today() + timedelta(days=1))
        valor = st.number_input("Valor do pagamento", min_value=0.0)
        metodo = st.selectbox("Método de pagamento", ["Cartão", "Dinheiro", "PIX"])

        submitted = st.form_submit_button("Reservar")
        if submitted:
            payload = {
                "clienteId": cliente_opcoes[cliente_selecionado],
                "filmeId": filme_opcoes[filme_selecionado],
                "dataInicio": data_inicio.isoformat(),
                "dataFim": data_fim.isoformat(),
                "pagamento": {
                    "valor": valor,
                    "metodo": metodo
                }
            }
            res = requests.post(f"{API_BASE}/reservas", json=payload)
            if res.status_code == 200:
                st.success("✅ Reserva realizada com sucesso!")
                st.experimental_rerun()
            else:
                st.error(f"❌ Erro ao criar reserva: {res.json().get('error')}")
else:
    st.warning("Você precisa ter clientes e filmes disponíveis para criar uma reserva.")

# Listagem
st.header("📄 Reservas Atuais")
try:
    r = requests.get(f"{API_BASE}/reservas")
    if r.status_code == 200 and r.text.strip():
        reservas = r.json()
    else:
        reservas = []

    if reservas:
        df = pd.DataFrame(reservas)
        st.dataframe(df, use_container_width=True)

        st.subheader("🗑️ Cancelar Reserva")
        opcoes_reserva = {f"ID {r['id']} - Cliente {r['clienteId']} - Filme {r['filmeId']}": r["id"] for r in reservas}
        reserva_cancelar = st.selectbox("Escolha a reserva para cancelar", list(opcoes_reserva.keys()))
        if st.button("Cancelar Reserva"):
            id_reserva = opcoes_reserva[reserva_cancelar]
            resp_del = requests.delete(f"{API_BASE}/reservas/{id_reserva}")
            if resp_del.status_code == 200:
                st.success("Reserva cancelada com sucesso!")
                st.experimental_rerun()
            else:
                st.error("Erro ao cancelar reserva.")
    else:
        st.info("Nenhuma reserva encontrada.")

except Exception as e:
    st.error(f"Erro ao buscar reservas: {e}")


except Exception as e:
    st.error(f"Erro ao buscar reservas: {e}")
