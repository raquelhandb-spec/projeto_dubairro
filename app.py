import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============================================================
# CONFIGURACAO DA PAGINA (deve ser o primeiro comando Streamlit)
# ============================================================
st.set_page_config(
    page_title="duBairro | Financial Intelligence",
    layout="wide",
    page_icon="🏪",
    initial_sidebar_state="expanded"
)

# ============================================================
# CONSTANTES DE MARCA
# ============================================================
COLORS = {
    "amber": "#FFC107",
    "amber_dark": "#FF8F00",
    "amber_light": "#FFE082",
    "bg_main": "#0D1117",
    "bg_card": "#161B22",
    "bg_card_hover": "#1C2333",
    "border": "#30363D",
    "text": "#F0F6FC",
    "text_secondary": "#8B949E",
    "green": "#2EA043",
    "red": "#F85149",
    "blue": "#58A6FF",
    "purple": "#BC8CFF",
}

CHART_COLORS = ["#FFC107", "#2EA043", "#58A6FF", "#F85149", "#BC8CFF", "#FF7B72", "#FFE082", "#79C0FF"]

CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(22,27,34,0.8)",
    font=dict(family="Inter, DM Sans, sans-serif", color="#F0F6FC", size=12),
    title_font=dict(size=16, color="#FFC107"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    margin=dict(l=40, r=40, t=50, b=40),
    colorway=CHART_COLORS,
)

# ============================================================
# CSS FINTECH DARK MODE
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

    /* === GLOBAL === */
    .stApp {
        background-color: #0D1117;
        color: #F0F6FC;
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #F0F6FC !important;
    }

    /* === SIDEBAR === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1117 0%, #161B22 100%);
        border-right: 2px solid #FFC107;
    }

    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] label {
        color: #8B949E;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFC107 !important;
    }

    /* === METRIC CARDS === */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #161B22 0%, #1C2333 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,193,7,0.15);
        border-color: #FFC107;
    }

    [data-testid="stMetricLabel"] {
        color: #8B949E !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #F0F6FC !important;
        font-size: 1.6rem !important;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161B22;
        border-radius: 10px;
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #8B949E;
        font-weight: 500;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFC107 !important;
        color: #0D1117 !important;
        font-weight: 700;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }

    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }

    /* === DIVIDER === */
    hr {
        border-color: #30363D !important;
    }

    /* === FILE UPLOADER === */
    [data-testid="stFileUploader"] {
        border: 2px dashed #30363D;
        border-radius: 10px;
        padding: 10px;
    }

    /* === DATAFRAME === */
    [data-testid="stDataFrame"] {
        border: 1px solid #30363D;
        border-radius: 10px;
    }

    /* === EXPANDER === */
    .streamlit-expanderHeader {
        background-color: #161B22;
        border-radius: 8px;
        color: #FFC107 !important;
    }

    /* === SCROLLBAR === */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0D1117; }
    ::-webkit-scrollbar-thumb { background: #30363D; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #FFC107; }

    /* === CUSTOM CLASSES === */
    .insight-strip {
        background: linear-gradient(135deg, #161B22 0%, #1C2333 100%);
        border: 1px solid #30363D;
        border-left: 4px solid #FFC107;
        border-radius: 10px;
        padding: 16px 24px;
        margin: 8px 0;
    }

    .story-card {
        background: linear-gradient(135deg, #161B22 0%, #1C2333 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 24px;
        margin: 12px 0;
    }

    .story-card-red { border-left: 4px solid #F85149; }
    .story-card-green { border-left: 4px solid #2EA043; }
    .story-card-amber { border-left: 4px solid #FFC107; }
    .story-card-blue { border-left: 4px solid #58A6FF; }

    .decision-card {
        background: linear-gradient(135deg, #161B22 0%, #1C2333 100%);
        border: 1px solid #30363D;
        border-left: 4px solid #FFC107;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 10px 0;
        transition: border-color 0.2s;
    }

    .decision-card:hover {
        border-color: #FFC107;
    }

    .badge-green {
        background-color: rgba(46,160,67,0.15);
        color: #2EA043;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .badge-red {
        background-color: rgba(248,81,73,0.15);
        color: #F85149;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .badge-amber {
        background-color: rgba(255,193,7,0.15);
        color: #FFC107;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .big-number {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        color: #FFC107;
        line-height: 1.1;
    }

    .subtitle-text {
        color: #8B949E;
        font-size: 0.9rem;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCOES AUXILIARES
# ============================================================

def format_brl(value):
    """Formata numero como Real brasileiro."""
    if abs(value) >= 1_000_000:
        return f"R$ {value/1_000_000:,.2f}M"
    if abs(value) >= 1_000:
        return f"R$ {value:,.2f}"
    return f"R$ {value:,.2f}"


def categorize_product(prod):
    """Classifica produto em categoria."""
    p = str(prod).upper()
    if any(x in p for x in ['ABACATE', 'MAMAO', 'UVA', 'TOFU', 'LIMAO', 'ALHO',
                              'TOMATE', 'BANANA', 'LARANJA', 'MACA', 'MANGA',
                              'MELANCIA', 'CEBOLA', 'BATATA', 'CENOURA', 'PEPINO']):
        return 'Hortifruti'
    if any(x in p for x in ['CERVEJA', 'REFRIGERANTE', 'AGUA', 'SUCO', 'MATE',
                              'VINHO', 'ENERGETICO', 'CHA', 'CAFE']):
        return 'Bebidas'
    if any(x in p for x in ['ARROZ', 'FEIJAO', 'BISCOITO', 'CHOCOLATE', 'PAO',
                              'MACARRAO', 'ACUCAR', 'SAL', 'OLEO', 'FARINHA',
                              'MOLHO', 'AZEITE', 'CONSERVA']):
        return 'Mercearia'
    if any(x in p for x in ['QUEIJO', 'REQUEIJAO', 'MANTEIGA', 'IOGURTE',
                              'LEITE', 'PRESUNTO', 'MORTADELA', 'CREAM']):
        return 'Frios & Laticinios'
    if any(x in p for x in ['FRANGO', 'CARNE', 'LINGUICA', 'SALSICHA',
                              'PEIXE', 'BACON', 'HAMBURGUER', 'OVO']):
        return 'Acougue & Proteinas'
    return 'Outros'

CATEGORY_ICONS = {
    'Hortifruti': '🍏',
    'Bebidas': '🥤',
    'Mercearia': '🛒',
    'Frios & Laticinios': '🧀',
    'Acougue & Proteinas': '🥩',
    'Outros': '📦',
}


@st.cache_data
def process_data(file):
    """Carrega e processa o arquivo de dados."""
    try:
        if file.name.endswith('.csv'):
            try:
                df = pd.read_csv(file, sep=';', decimal=',')
                if len(df.columns) <= 1:
                    file.seek(0)
                    df = pd.read_csv(file)
            except Exception:
                file.seek(0)
                df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Converter colunas numericas
        cols_num = ['Receita_Bruta', 'CMV', 'Qtde_Vendida', 'Margem_Bruta']
        for col in cols_num:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Calcular Lucro Bruto se nao existir
        if 'Lucro_Bruto' not in df.columns and 'Receita_Bruta' in df.columns and 'CMV' in df.columns:
            df['Lucro_Bruto'] = df['Receita_Bruta'] - df['CMV']

        # Categorizar produtos
        if 'Produto' in df.columns:
            df['Categoria'] = df['Produto'].apply(categorize_product)

        return df

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
        return pd.DataFrame()


def compute_kpis(df):
    """Calcula todos os KPIs do dashboard."""
    fat = df['Receita_Bruta'].sum() if 'Receita_Bruta' in df.columns else 0
    cmv = df['CMV'].sum() if 'CMV' in df.columns else 0
    lucro = df['Lucro_Bruto'].sum() if 'Lucro_Bruto' in df.columns else 0
    margem = (lucro / fat * 100) if fat > 0 else 0
    vol = df['Qtde_Vendida'].sum() if 'Qtde_Vendida' in df.columns else 0
    n_produtos = df['Produto'].nunique() if 'Produto' in df.columns else len(df)
    ticket_medio = fat / n_produtos if n_produtos > 0 else 0
    roi = (lucro / cmv * 100) if cmv > 0 else 0

    # Top e pior produto
    top_prod = ""
    worst_prod = ""
    if 'Produto' in df.columns and 'Lucro_Bruto' in df.columns and len(df) > 0:
        prod_lucro = df.groupby('Produto')['Lucro_Bruto'].sum()
        top_prod = prod_lucro.idxmax() if len(prod_lucro) > 0 else ""
        worst_prod = prod_lucro.idxmin() if len(prod_lucro) > 0 else ""

    # Concentracao top 5
    concentracao_top5 = 0
    if 'Produto' in df.columns and 'Receita_Bruta' in df.columns and fat > 0:
        top5_receita = df.groupby('Produto')['Receita_Bruta'].sum().nlargest(5).sum()
        concentracao_top5 = (top5_receita / fat) * 100

    return {
        'faturamento': fat,
        'cmv': cmv,
        'lucro': lucro,
        'margem': margem,
        'volume': vol,
        'n_produtos': n_produtos,
        'ticket_medio': ticket_medio,
        'roi': roi,
        'top_produto': top_prod,
        'worst_produto': worst_prod,
        'concentracao_top5': concentracao_top5,
    }


def compute_abc(df):
    """Calcula a curva ABC (Pareto)."""
    if 'Produto' not in df.columns or 'Receita_Bruta' not in df.columns:
        return pd.DataFrame()

    abc = df.groupby('Produto')['Receita_Bruta'].sum().reset_index()
    abc = abc.sort_values('Receita_Bruta', ascending=False).reset_index(drop=True)
    abc['Receita_Acumulada'] = abc['Receita_Bruta'].cumsum()
    total = abc['Receita_Bruta'].sum()
    abc['Pct_Acumulado'] = (abc['Receita_Acumulada'] / total) * 100 if total > 0 else 0

    def classify(pct):
        if pct <= 80:
            return 'A'
        elif pct <= 95:
            return 'B'
        return 'C'

    abc['Classe'] = abc['Pct_Acumulado'].apply(classify)
    return abc


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px 0;">
        <span style="font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 800; color: #FFC107;">
            du<span style="color: #F0F6FC;">Bairro</span>
        </span>
        <br>
        <span style="color: #8B949E; font-size: 0.8rem; letter-spacing: 0.15em; text-transform: uppercase;">
            Financial Intelligence
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Upload
    st.markdown("##### 📂 Dados de Vendas")
    uploaded_file = st.file_uploader(
        "Arraste seu arquivo aqui",
        type=["csv", "xlsx"],
        help="Aceita CSV ou Excel com colunas: Produto, Receita_Bruta, CMV, Qtde_Vendida, Margem_Bruta"
    )

    if uploaded_file is not None:
        st.markdown("---")

        # Navegacao
        st.markdown("##### 🧭 Navegacao")
        nav = st.radio(
            "Escolha a visao:",
            ["📊 Dashboard", "📑 Apresentacao"],
            label_visibility="collapsed"
        )
    else:
        nav = None

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; color:#8B949E; font-size:0.7rem; padding-top:10px;">
        Powered by <span style="color:#FFC107;">duBairro</span> Analytics<br>
        v2.0 · 2026
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# LOGICA PRINCIPAL
# ============================================================
if uploaded_file is not None:
    df = process_data(uploaded_file)

    if df.empty:
        st.error("Nao foi possivel carregar os dados. Verifique o formato do arquivo.")
        st.stop()

    # Filtro de categorias na sidebar
    if 'Categoria' in df.columns:
        cats = sorted(df['Categoria'].unique())
        with st.sidebar:
            st.markdown("##### 🏷️ Filtrar Categorias")
            sel_cats = st.multiselect(
                "Categorias:",
                cats,
                default=cats,
                label_visibility="collapsed"
            )
        df_filtered = df[df['Categoria'].isin(sel_cats)]
    else:
        df_filtered = df

    kpis = compute_kpis(df_filtered)

    # ===========================================================
    # DASHBOARD VIEW
    # ===========================================================
    if nav == "📊 Dashboard":

        # Header
        st.markdown("""
        <div style="padding: 10px 0 5px 0;">
            <h1 style="margin:0; font-size: 2rem;">
                <span style="color:#FFC107;">Financial</span> Intelligence Dashboard
            </h1>
            <p style="color:#8B949E; margin-top:4px; font-size:0.95rem;">
                Visao estrategica completa · Analise de performance por produto e categoria
            </p>
        </div>
        """, unsafe_allow_html=True)

        # --- KPIs LINHA 1 ---
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("Faturamento Bruto", format_brl(kpis['faturamento']))
        with k2:
            delta_lucro = "margem saudavel" if kpis['margem'] > 20 else "margem baixa"
            st.metric("Lucro Bruto", format_brl(kpis['lucro']), delta=delta_lucro,
                      delta_color="normal" if kpis['margem'] > 20 else "inverse")
        with k3:
            st.metric("Margem Bruta", f"{kpis['margem']:.1f}%",
                      delta="acima de 20%" if kpis['margem'] > 20 else "abaixo de 20%",
                      delta_color="normal" if kpis['margem'] > 20 else "inverse")
        with k4:
            st.metric("Itens Vendidos", f"{int(kpis['volume']):,}")

        # --- KPIs LINHA 2 ---
        k5, k6, k7, k8 = st.columns(4)
        with k5:
            st.metric("Ticket Medio / Produto", format_brl(kpis['ticket_medio']))
        with k6:
            st.metric("CMV Total", format_brl(kpis['cmv']))
        with k7:
            st.metric("ROI sobre Estoque", f"{kpis['roi']:.1f}%",
                      delta="positivo" if kpis['roi'] > 0 else "negativo",
                      delta_color="normal" if kpis['roi'] > 0 else "inverse")
        with k8:
            st.metric("Produtos Unicos", f"{kpis['n_produtos']}")

        # --- FAIXA DE INSIGHTS ---
        conc = kpis['concentracao_top5']
        conc_color = "#F85149" if conc > 60 else ("#FFC107" if conc > 40 else "#2EA043")
        conc_badge = "badge-red" if conc > 60 else ("badge-amber" if conc > 40 else "badge-green")
        conc_label = "ALTO RISCO" if conc > 60 else ("MODERADO" if conc > 40 else "SAUDAVEL")

        st.markdown(f"""
        <div class="insight-strip" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
            <div>
                <span style="color:#FFC107; font-size:1.1rem;">⭐</span>
                <span style="color:#8B949E; font-size:0.8rem;">PRODUTO ESTRELA</span><br>
                <span style="color:#F0F6FC; font-weight:600;">{kpis['top_produto']}</span>
            </div>
            <div>
                <span style="color:#F85149; font-size:1.1rem;">⚠️</span>
                <span style="color:#8B949E; font-size:0.8rem;">PRODUTO CRITICO</span><br>
                <span style="color:#F85149; font-weight:600;">{kpis['worst_produto']}</span>
            </div>
            <div>
                <span style="color:{conc_color}; font-size:1.1rem;">📊</span>
                <span style="color:#8B949E; font-size:0.8rem;">CONCENTRACAO TOP 5</span><br>
                <span style="color:{conc_color}; font-weight:700;">{conc:.0f}%</span>
                <span class="{conc_badge}">{conc_label}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- GRAFICOS LINHA 1 ---
        gc1, gc2 = st.columns(2)

        # VAMPIROS
        with gc1:
            st.markdown("#### 🧛 Vampiros de Lucro")
            st.caption("Produtos com alto giro mas margem critica")
            if 'Margem_Bruta' in df_filtered.columns and 'Qtde_Vendida' in df_filtered.columns:
                vampiros = df_filtered[df_filtered['Qtde_Vendida'] > 10].sort_values('Margem_Bruta').head(30)
                if len(vampiros) > 0:
                    fig_v = px.scatter(
                        vampiros, x="Qtde_Vendida", y="Margem_Bruta",
                        size="Receita_Bruta", color="Categoria",
                        hover_name="Produto",
                        hover_data={"Receita_Bruta": ":.2f", "Margem_Bruta": ":.2%"},
                        height=400,
                    )
                    # Linhas de quadrante
                    median_margem = df_filtered['Margem_Bruta'].median()
                    median_qtde = df_filtered['Qtde_Vendida'].median()
                    fig_v.add_hline(y=median_margem, line_dash="dash", line_color="#30363D", opacity=0.6)
                    fig_v.add_vline(x=median_qtde, line_dash="dash", line_color="#30363D", opacity=0.6)
                    fig_v.update_layout(**CHART_LAYOUT)
                    st.plotly_chart(fig_v, use_container_width=True)
                else:
                    st.info("Nenhum produto vampiro encontrado com os filtros atuais.")

        # JOIAS
        with gc2:
            st.markdown("#### 💎 Joias Escondidas")
            st.caption("Minas de ouro: alta margem e lucro")
            if 'Margem_Bruta' in df_filtered.columns and 'Lucro_Bruto' in df_filtered.columns:
                joias = df_filtered[df_filtered['Margem_Bruta'] > 0.30].sort_values('Lucro_Bruto', ascending=False).head(10)
                if len(joias) > 0:
                    joias_plot = joias.sort_values('Lucro_Bruto', ascending=True)
                    fig_j = px.bar(
                        joias_plot, x="Lucro_Bruto", y="Produto",
                        orientation='h', color="Lucro_Bruto",
                        color_continuous_scale=["#161B22", "#2EA043"],
                        hover_data={"Margem_Bruta": ":.2%"},
                        height=400,
                    )
                    fig_j.update_layout(**CHART_LAYOUT)
                    fig_j.update_layout(showlegend=False, coloraxis_showscale=False)
                    st.plotly_chart(fig_j, use_container_width=True)
                else:
                    st.info("Nenhuma joia encontrada com os filtros atuais.")

        # --- GRAFICOS LINHA 2 ---
        gc3, gc4, gc5 = st.columns(3)

        # TREEMAP
        with gc3:
            st.markdown("#### 🗺️ Mapa de Categorias")
            if 'Categoria' in df_filtered.columns:
                fig_tree = px.treemap(
                    df_filtered, path=['Categoria', 'Produto'],
                    values='Receita_Bruta',
                    color='Margem_Bruta',
                    color_continuous_scale=["#F85149", "#FFC107", "#2EA043"],
                    color_continuous_midpoint=df_filtered['Margem_Bruta'].median(),
                    height=380,
                )
                fig_tree.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif", color="#F0F6FC"),
                    margin=dict(l=5, r=5, t=5, b=5),
                    coloraxis_showscale=False,
                )
                st.plotly_chart(fig_tree, use_container_width=True)

        # HISTOGRAMA DE MARGEM
        with gc4:
            st.markdown("#### 📊 Distribuicao de Margem")
            if 'Margem_Bruta' in df_filtered.columns:
                fig_hist = px.histogram(
                    df_filtered, x="Margem_Bruta", nbins=25,
                    color_discrete_sequence=["#FFC107"],
                    height=380,
                )
                fig_hist.add_vline(
                    x=df_filtered['Margem_Bruta'].mean(),
                    line_dash="dash", line_color="#F85149",
                    annotation_text=f"Media: {df_filtered['Margem_Bruta'].mean():.2%}",
                    annotation_font_color="#F85149"
                )
                fig_hist.update_layout(**CHART_LAYOUT)
                st.plotly_chart(fig_hist, use_container_width=True)

        # DONUT DE RECEITA POR CATEGORIA
        with gc5:
            st.markdown("#### 🍩 Receita por Categoria")
            if 'Categoria' in df_filtered.columns:
                cat_receita = df_filtered.groupby('Categoria')['Receita_Bruta'].sum().reset_index()
                fig_donut = px.pie(
                    cat_receita, names='Categoria', values='Receita_Bruta',
                    hole=0.55, color_discrete_sequence=CHART_COLORS,
                    height=380,
                )
                fig_donut.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif", color="#F0F6FC"),
                    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
                    margin=dict(l=20, r=20, t=10, b=10),
                )
                fig_donut.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_donut, use_container_width=True)

        # --- CURVA ABC ---
        st.markdown("---")
        st.markdown("#### 📈 Curva ABC (Pareto)")
        st.caption("Classificacao de produtos por contribuicao na receita: A (80%), B (80-95%), C (95-100%)")

        abc = compute_abc(df_filtered)
        if not abc.empty:
            color_map = {'A': '#FFC107', 'B': '#58A6FF', 'C': '#8B949E'}
            abc['Cor'] = abc['Classe'].map(color_map)

            fig_abc = go.Figure()

            # Barras
            for classe in ['A', 'B', 'C']:
                mask = abc['Classe'] == classe
                fig_abc.add_trace(go.Bar(
                    x=abc[mask].index,
                    y=abc[mask]['Receita_Bruta'],
                    name=f'Classe {classe}',
                    marker_color=color_map[classe],
                    hovertext=abc[mask]['Produto'],
                    hovertemplate='<b>%{hovertext}</b><br>Receita: R$ %{y:,.2f}<extra></extra>',
                ))

            # Linha cumulativa
            fig_abc.add_trace(go.Scatter(
                x=abc.index,
                y=abc['Pct_Acumulado'],
                name='% Acumulado',
                yaxis='y2',
                line=dict(color='#F0F6FC', width=2),
                hovertemplate='%{y:.1f}%<extra></extra>',
            ))

            # Linhas de referencia
            fig_abc.add_hline(y=80, line_dash="dot", line_color="#FFC107", opacity=0.5,
                              annotation_text="80%", annotation_font_color="#FFC107", row="all", col="all")
            fig_abc.add_hline(y=95, line_dash="dot", line_color="#58A6FF", opacity=0.5,
                              annotation_text="95%", annotation_font_color="#58A6FF", row="all", col="all")

            fig_abc.update_layout(
                **CHART_LAYOUT,
                height=420,
                yaxis=dict(title="Receita (R$)", showgrid=False),
                yaxis2=dict(title="% Acumulado", overlaying='y', side='right',
                            range=[0, 105], showgrid=False),
                xaxis=dict(showticklabels=False, title="Produtos (ordenados por receita)"),
                barmode='stack',
            )
            st.plotly_chart(fig_abc, use_container_width=True)

            # Resumo ABC
            abc_summary = abc.groupby('Classe').agg(
                Produtos=('Produto', 'count'),
                Receita=('Receita_Bruta', 'sum')
            ).reset_index()
            total_receita = abc_summary['Receita'].sum()
            abc_summary['% Receita'] = (abc_summary['Receita'] / total_receita * 100).round(1)

            s1, s2, s3 = st.columns(3)
            for col, classe in zip([s1, s2, s3], ['A', 'B', 'C']):
                row = abc_summary[abc_summary['Classe'] == classe]
                if not row.empty:
                    with col:
                        cor = color_map[classe]
                        n = int(row['Produtos'].values[0])
                        pct = row['% Receita'].values[0]
                        st.markdown(f"""
                        <div class="story-card" style="text-align:center; border-top: 3px solid {cor};">
                            <span style="font-size:1.8rem; font-weight:800; color:{cor};">Classe {classe}</span><br>
                            <span class="big-number" style="color:{cor}; font-size:2rem;">{n}</span>
                            <span style="color:#8B949E;"> produtos</span><br>
                            <span style="color:#F0F6FC; font-size:1.2rem; font-weight:600;">{pct}%</span>
                            <span style="color:#8B949E;"> da receita</span>
                        </div>
                        """, unsafe_allow_html=True)

        # --- TABELA DE DADOS ---
        st.markdown("---")
        with st.expander("📋 Ver Tabela de Dados Completa"):
            st.dataframe(
                df_filtered.style.format({
                    'Receita_Bruta': 'R$ {:.2f}',
                    'CMV': 'R$ {:.2f}',
                    'Lucro_Bruto': 'R$ {:.2f}',
                    'Margem_Bruta': '{:.2%}',
                }),
                use_container_width=True,
                height=400,
            )
            csv = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download CSV", csv, "dubairro_dados.csv", "text/csv")

    # ===========================================================
    # APRESENTACAO (STORYTELLING)
    # ===========================================================
    elif nav == "📑 Apresentacao":

        st.markdown("""
        <div style="padding: 10px 0 5px 0;">
            <h1 style="margin:0; font-size: 2rem;">
                <span style="color:#FFC107;">Apresentacao</span> para Diretoria
            </h1>
            <p style="color:#8B949E; margin-top:4px;">
                Narrativa estrategica baseada em dados · Mercado duBairro
            </p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "1 · O Cenario",
            "2 · Os Numeros",
            "3 · Sangria",
            "4 · Ouro",
            "5 · Curva ABC",
            "6 · Decisoes"
        ])

        # ===================== SLIDE 1: O CENARIO =====================
        with tab1:
            st.markdown("""
            <div class="story-card story-card-amber">
                <h2 style="color:#FFC107 !important; margin-top:0;">🏪 O Cenario Atual</h2>
                <p style="color:#8B949E; font-size:1.05rem;">
                    Antes de qualquer decisao, precisamos entender o tamanho do tabuleiro.
                </p>
            </div>
            """, unsafe_allow_html=True)

            n_cats = df_filtered['Categoria'].nunique() if 'Categoria' in df_filtered.columns else 0

            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""
                <div class="story-card" style="text-align:center;">
                    <span class="big-number">{format_brl(kpis['faturamento'])}</span>
                    <p class="subtitle-text">Faturamento no Periodo</p>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="story-card" style="text-align:center;">
                    <span class="big-number">{kpis['n_produtos']}</span>
                    <p class="subtitle-text">Produtos no Mix</p>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="story-card" style="text-align:center;">
                    <span class="big-number">{n_cats}</span>
                    <p class="subtitle-text">Categorias Ativas</p>
                </div>
                """, unsafe_allow_html=True)

            # Receita por categoria
            if 'Categoria' in df_filtered.columns:
                cat_rev = df_filtered.groupby('Categoria')['Receita_Bruta'].sum().reset_index()
                cat_rev = cat_rev.sort_values('Receita_Bruta', ascending=True)
                fig_cat = px.bar(
                    cat_rev, x='Receita_Bruta', y='Categoria',
                    orientation='h', color='Categoria',
                    color_discrete_sequence=CHART_COLORS,
                    height=300,
                )
                fig_cat.update_layout(**CHART_LAYOUT)
                fig_cat.update_layout(showlegend=False, yaxis_title="", xaxis_title="Receita (R$)")
                st.plotly_chart(fig_cat, use_container_width=True)

            st.markdown("""
            <div class="story-card story-card-blue">
                <p style="color:#58A6FF; font-weight:600; margin:0;">
                    ➡️ Agora que sabemos o tamanho do tabuleiro, vamos olhar o que os numeros realmente dizem...
                </p>
            </div>
            """, unsafe_allow_html=True)

        # ===================== SLIDE 2: OS NUMEROS FALAM =====================
        with tab2:
            st.markdown("""
            <div class="story-card story-card-amber">
                <h2 style="color:#FFC107 !important; margin-top:0;">📊 Os Numeros Falam</h2>
                <p style="color:#8B949E; font-size:1.05rem;">
                    Cada numero conta uma parte da historia. Vamos decodificar.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # KPIs com interpretacao
            r1, r2 = st.columns(2)
            with r1:
                st.markdown(f"""
                <div class="story-card">
                    <span style="color:#8B949E; font-size:0.8rem; text-transform:uppercase;">Faturamento → CMV → Lucro</span>
                    <div style="display:flex; align-items:center; gap:12px; margin-top:12px;">
                        <div style="text-align:center;">
                            <span style="color:#FFC107; font-size:1.5rem; font-weight:700;">{format_brl(kpis['faturamento'])}</span>
                            <br><span style="color:#8B949E; font-size:0.75rem;">RECEITA</span>
                        </div>
                        <span style="color:#F85149; font-size:1.5rem;">→</span>
                        <div style="text-align:center;">
                            <span style="color:#F85149; font-size:1.5rem; font-weight:700;">- {format_brl(kpis['cmv'])}</span>
                            <br><span style="color:#8B949E; font-size:0.75rem;">CUSTO</span>
                        </div>
                        <span style="color:#2EA043; font-size:1.5rem;">→</span>
                        <div style="text-align:center;">
                            <span style="color:#2EA043; font-size:1.5rem; font-weight:700;">= {format_brl(kpis['lucro'])}</span>
                            <br><span style="color:#8B949E; font-size:0.75rem;">LUCRO</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with r2:
                margem_emoji = "✅" if kpis['margem'] > 20 else "⚠️"
                roi_emoji = "✅" if kpis['roi'] > 15 else "⚠️"
                st.markdown(f"""
                <div class="story-card">
                    <span style="color:#8B949E; font-size:0.8rem; text-transform:uppercase;">Indicadores de Eficiencia</span>
                    <div style="margin-top:12px;">
                        <p style="color:#F0F6FC; margin:8px 0;">
                            {margem_emoji} <strong>Margem de {kpis['margem']:.1f}%</strong>
                            — Para cada R$ 100 vendidos, <strong style="color:#FFC107;">R$ {kpis['margem']:.2f}</strong> ficam no caixa.
                        </p>
                        <p style="color:#F0F6FC; margin:8px 0;">
                            {roi_emoji} <strong>ROI de {kpis['roi']:.1f}%</strong>
                            — Para cada R$ 1 investido em estoque, retornam <strong style="color:#FFC107;">R$ {kpis['roi']/100:.2f}</strong>.
                        </p>
                        <p style="color:#F0F6FC; margin:8px 0;">
                            🎯 <strong>Ticket medio de {format_brl(kpis['ticket_medio'])}</strong> por linha de produto.
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Waterfall chart
            fig_wf = go.Figure(go.Waterfall(
                name="Fluxo", orientation="v",
                measure=["absolute", "relative", "total"],
                x=["Receita Bruta", "(-) CMV", "= Lucro Bruto"],
                y=[kpis['faturamento'], -kpis['cmv'], kpis['lucro']],
                connector={"line": {"color": "#30363D"}},
                increasing={"marker": {"color": "#2EA043"}},
                decreasing={"marker": {"color": "#F85149"}},
                totals={"marker": {"color": "#FFC107"}},
                textposition="outside",
                text=[format_brl(kpis['faturamento']), format_brl(kpis['cmv']), format_brl(kpis['lucro'])],
            ))
            fig_wf.update_layout(**CHART_LAYOUT, height=350, showlegend=False)
            fig_wf.update_layout(title="Cascata Financeira")
            st.plotly_chart(fig_wf, use_container_width=True)

            st.markdown("""
            <div class="story-card story-card-blue">
                <p style="color:#58A6FF; font-weight:600; margin:0;">
                    ➡️ Os numeros sao claros. Mas onde exatamente estamos perdendo dinheiro?
                </p>
            </div>
            """, unsafe_allow_html=True)

        # ===================== SLIDE 3: ONDE ESTAMOS SANGRANDO =====================
        with tab3:
            st.markdown("""
            <div class="story-card story-card-red">
                <h2 style="color:#F85149 !important; margin-top:0;">🩸 Onde Estamos Sangrando</h2>
                <p style="color:#8B949E; font-size:1.05rem;">
                    Produtos que giram nas prateleiras mas drenam nosso lucro silenciosamente.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Vampiros
            if 'Margem_Bruta' in df_filtered.columns:
                vampiros = df_filtered[df_filtered['Qtde_Vendida'] > 10].sort_values('Margem_Bruta').head(30)
                if len(vampiros) >= 2:
                    top_vamp = vampiros.head(5)
                    custo_oportunidade = top_vamp['Receita_Bruta'].sum() * (0.20 - top_vamp['Margem_Bruta'].mean())
                    custo_oportunidade = max(0, custo_oportunidade)

                    st.markdown(f"""
                    <div class="story-card" style="text-align:center;">
                        <span style="color:#F85149; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em;">
                            CUSTO DE OPORTUNIDADE ESTIMADO
                        </span><br>
                        <span class="big-number" style="color:#F85149; font-size:3rem;">{format_brl(custo_oportunidade)}</span>
                        <p class="subtitle-text">se esses produtos tivessem margem de 20%</p>
                    </div>
                    """, unsafe_allow_html=True)

                    vc1, vc2 = st.columns([3, 2])
                    with vc1:
                        fig_vamp = px.scatter(
                            vampiros, x="Qtde_Vendida", y="Margem_Bruta",
                            size="Receita_Bruta", color="Categoria",
                            hover_name="Produto", height=380,
                        )
                        fig_vamp.add_hline(y=0.10, line_dash="dash", line_color="#F85149",
                                           annotation_text="Margem critica 10%",
                                           annotation_font_color="#F85149")
                        fig_vamp.update_layout(**CHART_LAYOUT)
                        st.plotly_chart(fig_vamp, use_container_width=True)

                    with vc2:
                        st.markdown("##### 🔴 Top 5 Vampiros")
                        for i, row in top_vamp.iterrows():
                            icon = CATEGORY_ICONS.get(row.get('Categoria', ''), '📦')
                            st.markdown(f"""
                            <div class="decision-card" style="border-left-color:#F85149; padding:12px 16px;">
                                <span style="font-weight:600; color:#F0F6FC;">{icon} {row['Produto']}</span><br>
                                <span style="color:#F85149; font-weight:700;">{row['Margem_Bruta']*100:.1f}% margem</span>
                                <span style="color:#8B949E;"> · {int(row['Qtde_Vendida'])} unid.</span>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("Dados insuficientes para analise de vampiros.")

            st.markdown("""
            <div class="story-card story-card-blue">
                <p style="color:#58A6FF; font-weight:600; margin:0;">
                    ➡️ Ja sabemos o problema. Agora vamos ver onde esta o ouro escondido...
                </p>
            </div>
            """, unsafe_allow_html=True)

        # ===================== SLIDE 4: OURO ESCONDIDO =====================
        with tab4:
            st.markdown("""
            <div class="story-card story-card-green">
                <h2 style="color:#2EA043 !important; margin-top:0;">💎 Ouro Escondido</h2>
                <p style="color:#8B949E; font-size:1.05rem;">
                    Produtos que entregam lucro limpo. Precisamos colocar um holofote neles.
                </p>
            </div>
            """, unsafe_allow_html=True)

            if 'Margem_Bruta' in df_filtered.columns and 'Lucro_Bruto' in df_filtered.columns:
                joias = df_filtered[df_filtered['Margem_Bruta'] > 0.30].sort_values('Lucro_Bruto', ascending=False).head(15)

                if len(joias) > 0:
                    # Simulacao de crescimento
                    lucro_joias = joias['Lucro_Bruto'].sum()
                    lucro_extra_20 = lucro_joias * 0.20

                    g1, g2 = st.columns(2)
                    with g1:
                        st.markdown(f"""
                        <div class="story-card" style="text-align:center;">
                            <span style="color:#8B949E; font-size:0.8rem; text-transform:uppercase;">
                                LUCRO ATUAL DAS JOIAS
                            </span><br>
                            <span class="big-number" style="color:#2EA043;">{format_brl(lucro_joias)}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with g2:
                        st.markdown(f"""
                        <div class="story-card" style="text-align:center;">
                            <span style="color:#8B949E; font-size:0.8rem; text-transform:uppercase;">
                                SE VOLUME SUBIR 20%
                            </span><br>
                            <span class="big-number" style="color:#FFC107;">+ {format_brl(lucro_extra_20)}</span>
                            <p class="subtitle-text">lucro adicional estimado</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Top joias chart
                    joias_plot = joias.head(10).sort_values('Lucro_Bruto', ascending=True)
                    fig_joias = px.bar(
                        joias_plot, x='Lucro_Bruto', y='Produto',
                        orientation='h', color='Margem_Bruta',
                        color_continuous_scale=["#161B22", "#2EA043"],
                        height=400,
                    )
                    fig_joias.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
                    st.plotly_chart(fig_joias, use_container_width=True)

                    # Margem media por categoria
                    if 'Categoria' in df_filtered.columns:
                        cat_margem = df_filtered.groupby('Categoria')['Margem_Bruta'].mean().reset_index()
                        cat_margem = cat_margem.sort_values('Margem_Bruta', ascending=True)
                        fig_cm = px.bar(
                            cat_margem, x='Margem_Bruta', y='Categoria',
                            orientation='h', color='Margem_Bruta',
                            color_continuous_scale=["#F85149", "#FFC107", "#2EA043"],
                            height=280,
                        )
                        fig_cm.update_layout(**CHART_LAYOUT, coloraxis_showscale=False,
                                             title="Margem Media por Categoria")
                        st.plotly_chart(fig_cm, use_container_width=True)
                else:
                    st.info("Nenhum produto com margem acima de 30% encontrado.")

            st.markdown("""
            <div class="story-card story-card-blue">
                <p style="color:#58A6FF; font-weight:600; margin:0;">
                    ➡️ Sabemos onde sangra e onde brilha. Agora vamos classificar todo o portfolio...
                </p>
            </div>
            """, unsafe_allow_html=True)

        # ===================== SLIDE 5: CURVA ABC =====================
        with tab5:
            st.markdown("""
            <div class="story-card story-card-amber">
                <h2 style="color:#FFC107 !important; margin-top:0;">📈 A Curva ABC</h2>
                <p style="color:#8B949E; font-size:1.05rem;">
                    A regra de Pareto aplicada ao nosso mix: poucos produtos geram a maior parte da receita.
                </p>
            </div>
            """, unsafe_allow_html=True)

            abc = compute_abc(df_filtered)
            if not abc.empty:
                color_map = {'A': '#FFC107', 'B': '#58A6FF', 'C': '#8B949E'}

                # Summary cards
                abc_summ = abc.groupby('Classe').agg(
                    n=('Produto', 'count'),
                    receita=('Receita_Bruta', 'sum')
                ).reset_index()
                total_r = abc_summ['receita'].sum()
                total_p = abc_summ['n'].sum()

                ac1, ac2, ac3 = st.columns(3)
                for col, classe in zip([ac1, ac2, ac3], ['A', 'B', 'C']):
                    row = abc_summ[abc_summ['Classe'] == classe]
                    if not row.empty:
                        n = int(row['n'].values[0])
                        rec = row['receita'].values[0]
                        pct_r = (rec / total_r * 100) if total_r > 0 else 0
                        pct_p = (n / total_p * 100) if total_p > 0 else 0
                        cor = color_map[classe]
                        with col:
                            st.markdown(f"""
                            <div class="story-card" style="text-align:center; border-top:3px solid {cor};">
                                <span style="font-size:2rem; font-weight:800; color:{cor};">Classe {classe}</span><br>
                                <span class="big-number" style="color:{cor}; font-size:2.5rem;">{n}</span>
                                <span style="color:#8B949E;"> produtos ({pct_p:.0f}%)</span><br>
                                <span style="color:#F0F6FC; font-size:1.3rem; font-weight:700;">{pct_r:.1f}%</span>
                                <span style="color:#8B949E;"> da receita</span><br>
                                <span style="color:#8B949E; font-size:0.85rem;">{format_brl(rec)}</span>
                            </div>
                            """, unsafe_allow_html=True)

                # Pareto chart
                fig_pareto = go.Figure()
                for classe in ['A', 'B', 'C']:
                    mask = abc['Classe'] == classe
                    fig_pareto.add_trace(go.Bar(
                        x=abc[mask].index, y=abc[mask]['Receita_Bruta'],
                        name=f'Classe {classe}', marker_color=color_map[classe],
                        hovertext=abc[mask]['Produto'],
                        hovertemplate='<b>%{hovertext}</b><br>R$ %{y:,.2f}<extra></extra>',
                    ))

                fig_pareto.add_trace(go.Scatter(
                    x=abc.index, y=abc['Pct_Acumulado'],
                    name='% Acumulado', yaxis='y2',
                    line=dict(color='#F0F6FC', width=2, dash='dot'),
                ))

                fig_pareto.update_layout(
                    **CHART_LAYOUT, height=400,
                    yaxis=dict(title="Receita (R$)", showgrid=False),
                    yaxis2=dict(title="% Acumulado", overlaying='y', side='right', range=[0, 105], showgrid=False),
                    xaxis=dict(showticklabels=False, title="Produtos"),
                    barmode='stack',
                )
                st.plotly_chart(fig_pareto, use_container_width=True)

                # Insight de concentracao
                conc = kpis['concentracao_top5']
                if conc > 60:
                    alert_type = "story-card-red"
                    alert_icon = "🔴"
                    alert_msg = f"<strong>Alta concentracao!</strong> Apenas 5 produtos representam {conc:.0f}% da receita. Risco elevado — se um fornecedor falhar, o impacto e enorme."
                elif conc > 40:
                    alert_type = "story-card-amber"
                    alert_icon = "🟡"
                    alert_msg = f"<strong>Concentracao moderada.</strong> Top 5 produtos = {conc:.0f}% da receita. Monitore e busque diversificar gradualmente."
                else:
                    alert_type = "story-card-green"
                    alert_icon = "🟢"
                    alert_msg = f"<strong>Boa diversificacao!</strong> Top 5 = {conc:.0f}% da receita. O mix esta bem distribuido."

                st.markdown(f"""
                <div class="story-card {alert_type}">
                    <p style="color:#F0F6FC; font-size:1rem; margin:0;">
                        {alert_icon} {alert_msg}
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div class="story-card story-card-blue">
                <p style="color:#58A6FF; font-weight:600; margin:0;">
                    ➡️ Temos o diagnostico completo. Agora: quais decisoes precisamos tomar?
                </p>
            </div>
            """, unsafe_allow_html=True)

        # ===================== SLIDE 6: PERGUNTAS PARA DECISAO =====================
        with tab6:
            st.markdown("""
            <div class="story-card story-card-amber">
                <h2 style="color:#FFC107 !important; margin-top:0;">🎯 Perguntas para Tomada de Decisao</h2>
                <p style="color:#8B949E; font-size:1.05rem;">
                    Os dados ja falaram. Agora a diretoria precisa decidir. Cada pergunta abaixo e respaldada pelos numeros que acabamos de ver.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Perguntas estrategicas
            questions = [
                {
                    "icon": "🧛",
                    "titulo": "Vampiros: Descontinuar ou Renegociar?",
                    "contexto": f"Identificamos produtos com margem abaixo de 10% que movimentam alto volume. O custo de oportunidade e significativo.",
                    "cor": "#F85149",
                    "opcoes": ["Renegociar com fornecedores", "Aumentar preco gradualmente", "Descontinuar produtos", "Trocar por marca propria", "Manter e monitorar"],
                },
                {
                    "icon": "💎",
                    "titulo": "Joias: Como Amplificar?",
                    "contexto": f"Produtos de alta margem tem potencial inexplorado. Um aumento de 20% no volume geraria lucro adicional expressivo.",
                    "cor": "#2EA043",
                    "opcoes": ["Destaque em ponta de gondola", "Oferta combo com vampiros", "Marketing digital focado", "Degustacao na loja", "Manter estrategia atual"],
                },
                {
                    "icon": "🏷️",
                    "titulo": "Qual Categoria Merece Mais Espaco?",
                    "contexto": f"As categorias tem margens muito diferentes. Realocar espaco de prateleira pode impactar diretamente o lucro.",
                    "cor": "#FFC107",
                    "opcoes": ["Aumentar Hortifruti", "Aumentar Frios & Laticinios", "Aumentar Mercearia", "Redistribuir igualmente", "Analisar por metro quadrado"],
                },
                {
                    "icon": "📊",
                    "titulo": "Risco de Concentracao: Diversificar?",
                    "contexto": f"Top 5 produtos = {kpis['concentracao_top5']:.0f}% da receita. Se um fornecedor falhar ou o mercado mudar, qual o impacto?",
                    "cor": "#58A6FF",
                    "opcoes": ["Diversificar fornecedores", "Aumentar mix de produtos", "Criar marca propria", "Aceitar o risco", "Fazer estoque de seguranca"],
                },
                {
                    "icon": "💰",
                    "titulo": "Classe C: Suspender Recompra?",
                    "contexto": f"Produtos Classe C representam ~5% da receita mas ocupam espaco, capital e atencao. Vale manter?",
                    "cor": "#BC8CFF",
                    "opcoes": ["Suspender recompra 30 dias", "Reduzir variedade pela metade", "Manter com preco maior", "Eliminar definitivamente", "Avaliar caso a caso"],
                },
                {
                    "icon": "🏭",
                    "titulo": "Marca Propria: Hora de Investir?",
                    "contexto": f"Categorias com margem baixa (bebidas, mercearia basica) poderiam ter margem maior com marca propria duBairro.",
                    "cor": "#FF8F00",
                    "opcoes": ["Iniciar com 3 produtos piloto", "Estudar viabilidade primeiro", "Parceria com fabricante local", "Nao investir agora", "Priorizar outras acoes"],
                },
            ]

            for q in questions:
                st.markdown(f"""
                <div class="decision-card" style="border-left-color:{q['cor']};">
                    <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                        <span style="font-size:1.5rem;">{q['icon']}</span>
                        <span style="color:#F0F6FC; font-size:1.1rem; font-weight:700;">{q['titulo']}</span>
                    </div>
                    <p style="color:#8B949E; margin:4px 0 12px 0; font-size:0.9rem;">{q['contexto']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.selectbox(
                    f"Decisao: {q['titulo']}",
                    ["Selecione uma opcao..."] + q['opcoes'],
                    key=f"q_{q['icon']}",
                    label_visibility="collapsed",
                )
                st.markdown("<br>", unsafe_allow_html=True)

            # Area de notas
            st.markdown("---")
            st.markdown("#### 📝 Notas e Proximos Passos")
            st.text_area(
                "Registre aqui as decisoes e acoes definidas pela diretoria:",
                height=150,
                placeholder="Ex: Renegociar com fornecedor X, destacar produto Y na gondola principal, suspender recompra de Z por 30 dias...",
                key="notas_diretoria",
            )

            st.markdown("""
            <div class="story-card story-card-amber" style="text-align:center; margin-top:20px;">
                <span style="font-size:1.5rem;">🏪</span><br>
                <span style="color:#FFC107; font-family:'Space Grotesk', sans-serif; font-size:1.3rem; font-weight:700;">
                    Mercado duBairro
                </span><br>
                <span style="color:#8B949E; font-size:0.85rem;">
                    Decisoes inteligentes, baseadas em dados. Nao em achismos.
                </span>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# TELA DE ESPERA (SEM ARQUIVO)
# ============================================================
else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; padding:60px 20px;">
        <span style="font-family:'Space Grotesk', sans-serif; font-size:3.5rem; font-weight:800;">
            <span style="color:#FFC107;">du</span><span style="color:#F0F6FC;">Bairro</span>
        </span>
        <br>
        <span style="color:#8B949E; font-size:1.1rem; letter-spacing:0.15em; text-transform:uppercase;">
            Financial Intelligence Dashboard
        </span>
        <br><br><br>
        <div style="background:#161B22; border:2px dashed #30363D; border-radius:16px; padding:40px; max-width:500px; margin:0 auto;">
            <span style="font-size:3rem;">📂</span>
            <h3 style="color:#FFC107 !important; margin-top:16px;">Upload seus Dados</h3>
            <p style="color:#8B949E;">
                Arraste o arquivo <strong style="color:#F0F6FC;">DadosVendas.csv</strong> ou <strong style="color:#F0F6FC;">.xlsx</strong>
                na barra lateral esquerda para comecar.
            </p>
            <p style="color:#8B949E; font-size:0.8rem; margin-top:16px;">
                Colunas esperadas: Produto, Receita_Bruta, CMV, Qtde_Vendida, Margem_Bruta
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
