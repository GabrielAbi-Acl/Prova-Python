from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Transporte coletivo de BH", layout="wide")
st.title("Transporte coletivo de Belo Horizonte: usuários por linha")

arquivo = Path(__file__).parent / "dados_transporte_bh.csv"
df = pd.read_csv(
    arquivo,
    sep=";",
    dtype=str,
    usecols=lambda coluna: coluna.strip() in ["LINHA", "TOTAL USUARIOS"],
)
df.columns = df.columns.str.strip()
df["LINHA"] = df["LINHA"].str.strip()
df["TOTAL USUARIOS"] = pd.to_numeric(df["TOTAL USUARIOS"], errors="coerce").fillna(0)
totais = df.groupby("LINHA", as_index=False)["TOTAL USUARIOS"].sum()

opcao = st.sidebar.radio("Visualização", ["Tabela", "Gráficos"])

if opcao == "Tabela":
    st.header("Total de usuários por linha")
    st.dataframe(totais, hide_index=True, width="stretch")
else:
    st.header("Linhas que transportam mais e menos usuários")

    st.subheader("5 linhas que transportam mais usuários")
    maiores = totais.nlargest(5, "TOTAL USUARIOS")
    fig_maiores = px.bar(maiores, x="LINHA", y="TOTAL USUARIOS")
    fig_maiores.update_xaxes(type="category")
    st.plotly_chart(fig_maiores, width="stretch")

    st.subheader("5 linhas que transportam menos usuários")
    menores = totais.nsmallest(5, "TOTAL USUARIOS")
    fig_menores = px.bar(menores, x="LINHA", y="TOTAL USUARIOS")
    fig_menores.update_xaxes(type="category")
    st.plotly_chart(fig_menores, width="stretch")

st.caption("Fonte: dados abertos da Prefeitura de Belo Horizonte — https://dados.pbh.gov.br/")
