import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Análise Exploratória de Dados 🚀")

# Upload de arquivo CSV
file = st.file_uploader("Carregue um arquivo CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
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
