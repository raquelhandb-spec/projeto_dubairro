# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="duBairro | Gestao",
    layout="wide",
    page_icon="🛒"
)

st.markdown("""
    <style>
    :root { color-scheme: light !important; }
    html, body { background-color: #FFFFFF !important; color: #212121 !important; }
    .stApp { background-color: #FFFFFF !important; }
    [data-testid="stAppViewContainer"] { background-color: #FFFFFF !important; }
    [data-testid="stMain"] { background-color: #FFFFFF !important; }
    [data-testid="stMainBlockContainer"] { background-color: #FFFFFF !important; }
    .main, .block-container { background-color: #FFFFFF !important; }
    section[data-testid="stSidebar"] { background-color: #F5F5F5 !important; }
    section[data-testid="stSidebar"] * { color: #212121 !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, div, li, a { color: #212121 !important; }
    [data-testid="metric-container"] {
        background-color: #FAFAFA !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 8px;
        padding: 12px !important;
    }
    [data-testid="stFileUploadDropzone"] {
        background-color: #FFFDE7 !important;
        border: 2px dashed #FBC02D !important;
    }
    .stAlert { background-color: #FFFDE7 !important; color: #212121 !important; }
    </style>
""", unsafe_allow_html=True)

CUSTO_FIXO_REAL = 16913.46
META_LUCRO = 0.15

col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists("logo_dubairro.png"):
        st.image("logo_dubairro.png", width=130)
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=130)
    else:
        st.markdown("# 🛒")
with col2:
    st.markdown("# Gestao | Mercado duBairro")
    st.markdown("**Painel dos Socios**")

with st.sidebar:
    st.header("Controle")
    uploaded_file = st.file_uploader("Suba a Base_PowerBI.xlsx", type=["xlsx"])
    st.markdown("---")
    st.markdown(f"**Custo Fixo:** R$ {CUSTO_FIXO_REAL:,.2f}")
    st.markdown(f"**Meta Liquida:** {META_LUCRO*100:.0f}%")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name='DadosVendas')
        for c in ['Receita_Bruta', 'CMV', 'Qtde_Vendida']:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        fat = df['Receita_Bruta'].sum()
        lucro_bruto = (fat * 0.985) - df['CMV'].sum()
        lucro_liq = lucro_bruto - CUSTO_FIXO_REAL
        margem = (lucro_liq / fat) if fat > 0 else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Faturamento", f"R$ {fat:,.2f}")
        c2.metric("Lucro Liquido", f"R$ {lucro_liq:,.2f}")
        c3.metric("Margem Real", f"{margem*100:.1f}%", "Meta: 15%")
        mg_contrib = lucro_bruto / fat if fat > 0 else 0
        peq = CUSTO_FIXO_REAL / mg_contrib if mg_contrib > 0 else 0
        c4.metric("Ponto Equilibrio", f"R$ {peq:,.0f}")

        st.markdown("---")
        st.subheader("Desempenho Visual")
        top_produtos = df.sort_values('Receita_Bruta', ascending=False).head(15)

        fig = px.bar(
            top_produtos, x='Produto', y='Receita_Bruta',
            title="Top 15 Produtos que mais Faturam",
            color_discrete_sequence=['#FBC02D']
        )
        fig.update_layout(
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            font_color='#212121'
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Area Tecnica - Produtos sem Custo"):
            sem_custo = df[df['CMV'] <= 0]
            st.write(f"Produtos sem custo cadastrado: **{len(sem_custo)}**")
            if len(sem_custo) > 0:
                st.dataframe(sem_custo[['Produto', 'Receita_Bruta']])

    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")
else:
    st.info("Ola! Carregue a planilha para ver os indicadores.")
