import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="duBairro | Gestão", 
    layout="wide",
    page_icon="🛒",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILO VISUAL (Fundo Branco) ---
st.markdown("""
    <style>
        .stApp { background-color: #FFFFFF; }
        .stApp, .stMarkdown, p, h1, h2, h3 { color: #000000 !important; }
        [data-testid="stMetricValue"] { font-size: 24px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DADOS FIXOS ---
CUSTO_FIXO_REAL = 16913.46

# --- 4. CABEÇALHO ---
col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=130)
    else:
        st.markdown("# 🛒")

with col2:
    st.markdown("# Gestão | Mercado duBairro")
    st.markdown("**Painel Estratégico**")

# --- 5. SIDEBAR E UPLOAD ---
with st.sidebar:
    st.header("⚙️ Controle")
    uploaded_file = st.file_uploader("Suba a Base_PowerBI.xlsx", type=["xlsx"])
    st.info("💡 Use o arquivo gerado pelo script 'processar_dados_mercado.py'")

# --- 6. LÓGICA PRINCIPAL ---
if uploaded_file:
    try:
        # LENDO AS ABAS DA NOVA PLANILHA
        # dim_produtos: contém os dados detalhados por item
        df_prod = pd.read_excel(uploaded_file, sheet_name='dim_produtos')
        
        # CÁLCULOS (Recalculando totais para garantir precisão)
        fat_total = df_prod['Receita_Total'].sum()
        lucro_bruto = df_prod['Lucro_Total'].sum()
        
        # Lucro Líquido = Bruto - Custo Fixo
        lucro_liq = lucro_bruto - CUSTO_FIXO_REAL
        
        # Margens
        margem_real = (lucro_liq / fat_total) if fat_total > 0 else 0
        margem_bruta = (lucro_bruto / fat_total) if fat_total > 0 else 0
        
        # Ponto de Equilíbrio
        peq = CUSTO_FIXO_REAL / margem_bruta if margem_bruta > 0 else 0

        # --- EXIBIÇÃO DOS KPIS ---
        st.markdown("### 📈 Resumo do Mês")
        k1, k2, k3, k4 = st.columns(4)
        
        k1.metric("Faturamento", f"R$ {fat_total:,.2f}")
        k2.metric("Lucro Líquido", f"R$ {lucro_liq:,.2f}", delta_color="normal")
        k3.metric("Margem Real", f"{margem_real*100:.1f}%", "Meta: 15%")
        k4.metric("Ponto de Equilíbrio", f"R$ {peq:,.0f}")
        
        st.markdown("---")

        # --- GRÁFICO TOP PRODUTOS ---
        st.subheader("🏆 Top 15 Produtos (Faturamento)")
        
        # Pegando os campeões
        top_produtos = df_prod.sort_values('Receita_Total', ascending=False).head(15)
        
        fig = px.bar(
            top_produtos, 
            x='Produto', 
            y='Receita_Total',
            text='Receita_Total',
            title="Produtos que mais trouxeram dinheiro",
            color_discrete_sequence=['#FBC02D'] # Amarelo Ouro
        )
        
        # Ajuste visual fino
        fig.update_traces(texttemplate='R$ %{text:.2s}', textposition='outside')
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font_color="black",
            xaxis_title=None,
            yaxis_title="Receita (R$)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # --- TABELA DE CURVA A ---
        with st.expander("🔍 Ver Detalhes da Curva A"):
            # Filtrar apenas Curva A
            df_curva_a = df_prod[df_prod['Curva'] == 'A'][['Produto', 'Receita_Total', 'Lucro_Total', 'Margem_Media']]
            st.dataframe(df_curva_a.style.format({
                'Receita_Total': 'R$ {:,.2f}',
                'Lucro_Total': 'R$ {:,.2f}',
                'Margem_Media': '{:.1f}%'
            }))

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
        st.warning("Certifique-se de que está subindo o arquivo 'Base_PowerBI.xlsx' correto.")
else:
    st.info("👋 Olá! Faça o upload da planilha 'Base_PowerBI.xlsx' para ver os dados.")
