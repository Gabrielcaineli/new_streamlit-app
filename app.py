import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Dashboard Veículos", layout="wide")
st.header("Dashboard de Anúncios de Veículos 🚗📊")

csv_path = "vehicles_us.csv"
df = None

# Tenta carregar arquivo local
if os.path.exists(csv_path):
    st.info(f"Carregando dados de `{csv_path}`...")
    df = pd.read_csv(csv_path)
else:
    st.warning(
        f"Arquivo `{csv_path}` não encontrado. Você pode fazer upload de um CSV para analisar.")
    uploaded = st.file_uploader("Carregue um arquivo CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)

# Se não há dados, mostra instrução e encerra
if df is None:
    st.stop()

# Mostra dados e estatísticas
st.subheader("Visão geral dos dados")
st.dataframe(df.head())

st.subheader("Estatísticas descritivas")
st.write(df.describe(include="all"))

# Opção: escolher colunas numéricas
num_cols = df.select_dtypes(include=["number"]).columns.tolist()

# Controle via botões
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Criar histograma (odometer)"):
        if "odometer" in df.columns:
            fig = px.histogram(df, x="odometer", nbins=50,
                               title="Distribuição da Quilometragem (odometer)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Coluna 'odometer' não encontrada no dataset.")
with col2:
    if st.button("Criar gráfico de dispersão (price vs odometer)"):
        if "odometer" in df.columns and "price" in df.columns:
            fig = px.scatter(df, x="odometer", y="price",
                             title="Preço vs Quilometragem")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Colunas 'price' e/ou 'odometer' não encontradas no dataset.")

# Alternativa com checkbox (opcional)
st.markdown("---")
st.subheader("Gerar gráficos com caixas de seleção")
build_hist = st.checkbox("Gerar histograma (escolher coluna numérica)")
build_scatter = st.checkbox("Gerar scatter (escolher X e Y)")

if build_hist and num_cols:
    col = st.selectbox("Coluna para histograma", num_cols, key="hist_col")
    fig = px.histogram(df, x=col, nbins=50, title=f"Histograma — {col}")
    st.plotly_chart(fig, use_container_width=True)

if build_scatter and len(num_cols) >= 2:
    x_col = st.selectbox("X (numérica)", num_cols, index=0, key="scatter_x")
    y_col = st.selectbox("Y (numérica)", num_cols, index=1, key="scatter_y")
    fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    st.plotly_chart(fig, use_container_width=True)
elif build_scatter:
    st.warning("Necessário ao menos 2 colunas numéricas para scatter.")
