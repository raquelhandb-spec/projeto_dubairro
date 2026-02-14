import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# 1. Configuração da Página (Sempre a primeira coisa)
st.set_page_config(
    page_title="Dashboard Mercado duBairro",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS para Visual Limpo e Minimalista
st.markdown("""
<style>
    .block-container { padding-top: 1rem; padding-bottom: 2rem; }
    .stApp { background-color: #f9f9f9; }
    /* Ajuste para cards de métricas ficarem mais elegantes */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# 3. Carregamento de Dados (Cache para ficar rápido)
@st.cache_data
def load_data():
    try:
        # Tenta carregar da pasta 'data' (padrão)
        df_mensal = pd.read_csv("data/fato_vendas_mensais.csv")
        df_alertas = pd.read_csv("data/alertas_erosao_margem.csv")
        return df_mensal, df_alertas
    except FileNotFoundError:
        try:
            # Se não achar, tenta na raiz (caso os arquivos estejam soltos)
            df_mensal = pd.read_csv("fato_vendas_mensais.csv")
            df_alertas = pd.read_csv("alertas_erosao_margem.csv")
            return df_mensal, df_alertas
        except:
            return None, None

df_mensal, df_alertas = load_data()

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    # [CORREÇÃO SOLICITADA] Logo Minimalista (Tamanho controlado) [cite: 7]
    try:
        st.image("assets/logo_dubairro.png", width=140) # Ajuste width se quiser maior/menor
    except:
        st.warning("⚠️ Logo não encontrada em 'assets/'")
        
    st.write("---")
    
    # Menu Visual (Agora funciona pois você instalou o pacote!)
    selected = option_menu(
        menu_title=None,
        options=["Resumo Executivo", "Análise de Produtos", "Matriz Estratégica", "Alertas"],
        icons=["graph-up-arrow", "box-seam", "grid", "exclamation-triangle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#ff4b4b", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#ffebeb", "color": "#ff4b4b"},
        }
    )
    
    st.write("---")
    st.caption("Mercado duBairro © 2026")

# --- LÓGICA DAS PÁGINAS ---

if selected == "Resumo Executivo":
    st.title("📊 Resumo Executivo")
    st.markdown("### Visão Geral do Negócio")

    if df_mensal is not None:
        # Pega o último mês disponível
        ultimo_mes = df_mensal.iloc[-1]
        
        # Cards de KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Faturamento (Mês)", f"R$ {ultimo_mes['Receita']:,.2f}")
        col2.metric("Lucro Bruto", f"R$ {ultimo_mes['Lucro']:,.2f}")
        
        custo_fixo = 16913.46 # Valor fixo (podemos deixar dinâmico depois)
        lucro_liq = ultimo_mes['Lucro'] - custo_fixo
        col3.metric("Lucro Líquido (Est.)", f"R$ {lucro_liq:,.2f}", 
                   delta_color="normal" if lucro_liq > 0 else "inverse")

        st.divider()

        # Gráfico com Visual Limpo
        st.subheader("Evolução do Faturamento")
        
        # [MELHORIA PDF] Tooltip explicativo [cite: 16]
        with st.expander("ℹ️ Como ler este gráfico?"):
            st.markdown("""
            * **O que mostra:** A receita total do mercado mês a mês.
            * **Por que importa:** Ajuda a identificar tendências de crescimento ou queda sazonal.
            """)
            
        fig = px.line(df_mensal, x='Mes', y='Receita', markers=True)
        fig.update_layout(xaxis_title=None, yaxis_title="Reais (R$)", template="plotly_white")
        
        # config={'displayModeBar': False} -> Remove a barra de ferramentas (Minimalismo)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    else:
        st.warning("⚠️ Dados não carregados. Verifique se os arquivos CSV estão na pasta.")

elif selected == "Análise de Produtos":
    st.title("📦 Análise de Produtos")
    st.info("Em construção: Em breve aqui a Curva ABC.")

elif selected == "Matriz Estratégica":
    st.title("🎯 Matriz BCG")
    st.info("Em construção: Gráfico de Rentabilidade x Vendas.")

elif selected == "Alertas":
    st.title("⚠️ Alertas de Negócio")
    if df_alertas is not None and not df_alertas.empty:
        st.error(f"{len(df_alertas)} produtos com queda de margem.")
        st.dataframe(df_alertas, use_container_width=True, hide_index=True)
    else:
        st.success("Nenhuma erosão de margem detectada hoje!")
