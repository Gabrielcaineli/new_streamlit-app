import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Análise Exploratória de Dados ")


if os.path.exists(csv_path):
    st.info("Carregando dados do arquivo local `vehicles_us.csv`...")
    df = pd.read_csv(csv_path)
else:
    # Caso o arquivo não exista, pede upload
    file = st.file_uploader("Carregue um arquivo CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)

# Se temos dados carregados, mostra análises
if df is not None:
    st.subheader("Visualização dos Dados")
    st.dataframe(df.head())

    st.subheader("Estatísticas Descritivas")
    st.write(df.describe())

    # Selecionar colunas para gráfico
    colunas = df.select_dtypes(include=["int64", "float64"]).columns
    if len(colunas) >= 2:
        x_col = st.selectbox("Selecione a variável X", colunas)
        y_col = st.selectbox("Selecione a variável Y", colunas)

        fig = px.scatter(df, x=x_col, y=y_col,
                         title=f"Dispersão: {x_col} vs {y_col}")
        st.plotly_chart(fig)
    else:
        st.warning("O dataset precisa ter ao menos duas colunas numéricas.")
else:
    st.warning(
        "Nenhum dado disponível. Adicione `vehicles_us.csv` na pasta do projeto ou faça upload de um CSV.")


st.header("Dashboard de Anúncios de Veículos 🚗")

# carregar os dados
car_data = pd.read_csv("vehicles.csv")

# botão para histograma
hist_button = st.button("Criar histograma")

if hist_button:
    st.write("Criando um histograma para a coluna *odometer*")
    fig = px.histogram(car_data, x="odometer")
    st.plotly_chart(fig, use_container_width=True)

# botão para gráfico de dispersão
scatter_button = st.button("Criar gráfico de dispersão")

if scatter_button:
    st.write("Criando gráfico de dispersão entre preço e quilometragem")
    fig = px.scatter(car_data, x="odometer", y="price",
                     title="Preço vs Odômetro")
    st.plotly_chart(fig, use_container_width=True)
