import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Configuração da Página (Sempre a primeira linha)
st.set_page_config(
    page_title="Dashboard Mercado duBairro",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS para Estilo Minimalista ---
st.markdown("""
<style>
    /* Remove padding excessivo do topo */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Ajuste de fundo se necessário */
    .stApp {
        background-color: #f9f9f9;
    }
</style>
""", unsafe_allow_html=True)

# --- Carregamento de Dados (Cacheado para performance) ---
@st.cache_data
def load_data():
    try:
        # Carregando os arquivos CSV gerados pelo script de processamento
        df_vendas_mensais = pd.read_csv("data/fato_vendas_mensais.csv")
        df_alertas = pd.read_csv("data/alertas_erosao_margem.csv")
        
        # Opcional: Carregar outros se necessário, mas esses são os principais para o resumo
        # df_produtos = pd.read_csv("data/dim_produtos.csv")
        
        return df_vendas_mensais, df_alertas
    except FileNotFoundError:
        st.error("Arquivos de dados não encontrados. Rode o script 'processar_dados.py' primeiro.")
        return None, None

df_mensal, df_alertas = load_data()

# --- Sidebar (Menu Lateral) ---
with st.sidebar:
    # --- LOGO MINIMALISTA ---
    # Alterado: width=150 deixa a logo menor e elegante. 
    # Se quiser ainda menor, tente 120. Se quiser um pouco maior, 180.
    try:
        st.image("assets/logo_dubairro.png", width=150)
    except:
        st.warning("Logo não encontrada em assets/")
        
    st.write("---") # Linha separadora discreta
    
    selected = option_menu(
        menu_title=None,  # Título oculto para minimalismo
        options=["Resumo Executivo", "Análise de Produtos", "Matriz Estratégica", "Alertas"],
        icons=["bar-chart-fill", "box-seam", "grid", "exclamation-triangle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )
    
    st.write("---")
    st.caption("Mercado duBairro © 2026")

# --- Lógica das Páginas ---

if selected == "Resumo Executivo":
    st.title("📊 Resumo Executivo")
    st.markdown("### Visão Geral do Negócio")

    if df_mensal is not None:
        # Convertendo coluna de data se necessário
        # Assumindo que existe coluna 'Mes' ou similar. Ajuste conforme seu CSV.
        # Vou usar os nomes padrão do seu script de processamento.
        
        # Pegando o último mês disponível
        ultimo_mes = df_mensal.iloc[-1]
        
        # Métricas Principais (KPIs)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Faturamento (Mês Atual)", 
                value=f"R$ {ultimo_mes['Receita']:,.2f}",
                delta=f"{ultimo_mes['Margem_Percentual']:.1f}% Margem"
            )
        
        with col2:
            st.metric(
                label="Lucro Bruto", 
                value=f"R$ {ultimo_mes['Lucro']:,.2f}"
            )
            
        with col3:
            custo_fixo_estimado = 16913.46 # Valor fixo do seu código original
            lucro_liquido = ultimo_mes['Lucro'] - custo_fixo_estimado
            cor_lucro = "normal" if lucro_liquido > 0 else "inverse"
            st.metric(
                label="Lucro Líquido (Estimado)", 
                value=f"R$ {lucro_liquido:,.2f}",
                delta_color=cor_lucro
            )

        st.divider()

        # Gráfico de Tendência
        st.subheader("Evolução do Faturamento")
        fig_evolucao = px.line(
            df_mensal, 
            x='Mes', 
            y='Receita', 
            markers=True,
            title="Receita Mensal ao Longo do Tempo"
        )
        fig_evolucao.update_layout(xaxis_title="Mês", yaxis_title="Reais (R$)")
        # config={'displayModeBar': False} remove a barra de ferramentas do gráfico (mais minimalista)
        st.plotly_chart(fig_evolucao, use_container_width=True, config={'displayModeBar': False})

elif selected == "Análise de Produtos":
    st.title("📦 Análise de Produtos")
    st.info("Funcionalidade em desenvolvimento baseada na Curva ABC.")
    # Aqui entraria o código da aba de produtos

elif selected == "Matriz Estratégica":
    st.title("🎯 Matriz BCG (Rentabilidade)")
    st.markdown("Analise quais produtos são **Estrelas**, **Vacas Leiteiras**, **Interrogações** ou **Abacaxis**.")
    # Aqui entraria o gráfico de dispersão (Scatter Plot)

elif selected == "Alertas":
    st.title("⚠️ Alertas de Negócio")
    
    if df_alertas is not None and not df_alertas.empty:
        st.error(f"Atenção: {len(df_alertas)} produtos apresentaram erosão de margem recente.")
        st.dataframe(
            df_alertas[['Produto', 'Margem_Atual', 'Queda_Margem', 'Tendencia']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("Nenhum alerta crítico de margem detectado hoje.")
