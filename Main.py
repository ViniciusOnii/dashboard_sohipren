# Importa bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Configura a largura da página
st.set_page_config(page_title="Home", page_icon="", layout="wide")

# Carrega o arquivo Excel
df = pd.read_excel("base_2.xlsx")

st.markdown("""  <h3 style="color:#002b50;"> Dashboard Análise Sohipren </h3>    """, unsafe_allow_html=True)
#Carregando CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.image("assets/sohi_logo.png")

# Converte a coluna "EMISSÃO" para o formato yyyy/mm/dd, ignorando erros
df["EMISSÃO"] = pd.to_datetime(df["EMISSÃO"], dayfirst=True, errors='coerce')

# Converte a coluna "VALOR TOTAL" para numérico, substituindo valores inválidos por NaN
df["VALOR TOTAL"] = pd.to_numeric(df["VALOR TOTAL"], errors="coerce")

# Verifica se há valores NaN na coluna "VALOR TOTAL" após a conversão
if df["VALOR TOTAL"].isna().any():
    st.warning("Alguns valores na coluna 'VALOR TOTAL' não são numéricos e foram convertidos para NaN.")

# Barra lateral para seleção de datas
with st.sidebar:
    st.title("Selecionar Período de Datas")
    start_date = st.date_input(label="Data de Início")
    end_date = st.date_input(label="Data de Fim")

# Filtra o DataFrame com base no intervalo de datas (ignora valores NaT)
df2 = df[(df["EMISSÃO"] >= pd.to_datetime(start_date)) & (df["EMISSÃO"] <= pd.to_datetime(end_date))]

# Exibe o DataFrame filtrado
with st.expander("Filtrar o Execel"):
    filtered_df = dataframe_explorer(df2, case=False)
    st.dataframe(filtered_df, use_container_width=True)

# Divide a página em duas colunas
a1, a2 = st.columns(2)

with a1:
    st.subheader("Inserindo Novos Dados", divider="rainbow")
    from add_data import *
    add_data()

#metricas
with a2:
    st.subheader("Estatísticas de Dados", divider="rainbow")
    from streamlit_extras.metric_cards import style_metric_cards
    col1,col2=st.columns(2)
    col1.metric(label="Total de Itens", value=df2['DESCRIÇÃO MATERIAL'].count(), delta="Conjunto de Dados")
    col2.metric(label="Soma do Preço dos Produtos (BRL)", value=f"{df2['VALOR TOTAL'].sum():,.0f}", delta=f"{df2['VALOR TOTAL'].median():,.0f}")

    col11,col22,col33=st.columns(3)
    col11.metric(label="Preço Máximo", value=f"{df2['VALOR TOTAL'].max():,.0f}", delta="Maior Preço")
    col22.metric(label="Preço Mínimo", value=f"{df2['VALOR TOTAL'].min():,.0f}", delta="Menor Preço")
    col33.metric(label="Faixa de Preço ou Intervalo de Preço", value=f"{df2['VALOR TOTAL'].max() - df2['VALOR TOTAL'].min():,.0f}", delta="Intervalo ")
    #style the metrics 
    style_metric_cards(background_color="#3c4d66",border_left_color="#e6200e",border_color="#0060a")


b1, b2 = st.columns(2)

# Renomear a coluna "CÓD.MAT." para "CÓDIGO"
df2 = df2.rename(columns={"CÓD.MAT.": "CÓDIGO"})

# Converter todos os valores na coluna "CÓDIGO" para strings, substituindo valores nulos por "Sem Código"
df2["CÓDIGO"] = df2["CÓDIGO"].apply(lambda x: str(x).replace(".0", "") if pd.notnull(x) else "Sem Código")

with b1:
    st.subheader("DESCRIÇÃO MATERIAL & VALOR TOTAL", divider="rainbow")
    source = df2
    chart = alt.Chart(source).mark_circle().encode(
        x="DESCRIÇÃO MATERIAL",
        y="VALOR TOTAL",
        color="CÓDIGO"  # Usando o novo nome da coluna
    ).interactive()
    st.altair_chart(chart, theme="streamlit", use_container_width=True)

with b2:
    st.subheader("Descrição dos Produtos & Quantidade", divider="rainbow")
    
    # Cria o DataFrame `source` com as colunas "QUANTIDADE" e "DESCRIÇÃO MATERIAL" de `df2`
    # e substitui valores nulos em "DESCRIÇÃO MATERIAL" (caso existam)
    energy_source = pd.DataFrame({
       "DESCRIÇÃO MATERIAL": df2["DESCRIÇÃO MATERIAL"], 
       "VALOR UNITÁRIO (R$)": df2["VALOR UNITÁRIO"], 
       "Date":df2["EMISSÃO"]
    })

    # Cria o gráfico de barras usando Altair
    bar_chart = alt.Chart(energy_source).mark_bar().encode(
        x="month(Date):O",
        y="sum(VALOR UNITÁRIO (R$)):Q",
        color="DESCRIÇÃO MATERIAL:N"
    )

    # Exibe o gráfico no Streamlit
    st.altair_chart(bar_chart, use_container_width=True)

c1,c2=st.columns(2)
# Ajustar o layout do Streamlit
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Ajustar o layout do Streamlit
with c1:
    # Subtítulo com separador em arco-íris
    st.subheader("Atributos por Frequência", divider="rainbow")

    # Seleção de variáveis qualitativas e quantitativas
    feature_x = st.selectbox("Select X, qualitative data", df2.select_dtypes("object").columns)
    feature_y = st.selectbox("Select Y, quantitative data", df2.select_dtypes("number").columns)

    # Filtrar as 5 categorias mais frequentes em "DESCRIÇÃO MATERIAL"
    top_5_materials = df2["DESCRIÇÃO MATERIAL"].value_counts().nlargest(5).index
    df2_filtered = df2[df2["DESCRIÇÃO MATERIAL"].isin(top_5_materials)]

    # Caso a variável selecionada para o eixo X seja "RAZÃO SOCIAL CLIENTE", aplicar uma filtragem adicional
    if feature_x == "RAZÃO SOCIAL CLIENTE":
        # Filtrar para os 10 clientes mais frequentes para reduzir o número de labels
        top_10_clients = df2_filtered["RAZÃO SOCIAL CLIENTE"].value_counts().nlargest(10).index
        df2_filtered = df2_filtered[df2_filtered["RAZÃO SOCIAL CLIENTE"].isin(top_10_clients)]

    # Criação do gráfico com o DataFrame filtrado, ajustando o tamanho da figura
    fig, ax = plt.subplots(figsize=(12, 8))  # Tamanho ajustado para o original (12, 8)

    sns.scatterplot(
        data=df2_filtered, 
        x=feature_x, 
        y=feature_y, 
        hue="DESCRIÇÃO MATERIAL", 
        ax=ax,
        alpha=0.5,           # Aumenta a transparência para reduzir a sobreposição
        s=80                 # Reduz o tamanho dos pontos para melhor visualização
    )

    # Ajuste das labels para reduzir sobreposição
    if feature_x == "RAZÃO SOCIAL CLIENTE":
        # Abrevia nomes longos e rotaciona as labels
        ax.set_xticklabels([label.get_text()[:15] + '...' if len(label.get_text()) > 15 else label.get_text() 
                            for label in ax.get_xticklabels()], rotation=45, ha='right', fontsize=9)
    else:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right', fontsize=9)

    ax.set_yticklabels(ax.get_yticklabels(), fontsize=8)

    # Títulos e legendas melhorados
    ax.set_title("Visualização das 5 Principais Categorias de Material", fontsize=16)
    ax.set_xlabel("Variável Qualitativa (X)", fontsize=14)
    ax.set_ylabel("Variável Quantitativa (Y)", fontsize=14)

    # Legenda fora do gráfico para uma visualização mais compacta
    ax.legend(title="Descrição Material", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Adiciona linhas de grade para facilitar a comparação dos valores
    ax.grid(True, linestyle='--', alpha=0.7)

    # Exibe o gráfico no Streamlit
    st.pyplot(fig)

with c2:    
    st.subheader("DESCRIÇÃO MATERIAL & QUANTIDADE", divider="rainbow")

    # Cria o DataFrame `source` com as colunas "QUANTIDADE" e "DESCRIÇÃO MATERIAL" de `df2`
    # e substitui valores nulos em "DESCRIÇÃO MATERIAL" (caso existam)
    source = pd.DataFrame({
        "QUANTIDADE ($)": df2["QUANTIDADE"],
        "DESCRIÇÃO MATERIAL ($)": df2["DESCRIÇÃO MATERIAL"].fillna("Sem descrição")
    })
    with st.expander("Exibir Descrição Material"):
    # Cria o gráfico de barras
        bar_chart = alt.Chart(source).mark_bar().encode(
            x=alt.X("sum(QUANTIDADE ($)):Q", title="Quantidade Total ($)"),
            y=alt.Y("DESCRIÇÃO MATERIAL ($):N", sort="-x", title="Descrição do Material")
        )

        # Exibe o gráfico no Streamlit
        st.altair_chart(bar_chart, use_container_width=True)
