"""
MERCADO duBAIRRO — Dashboard de Gestão
Streamlit App com 5 páginas de análise estratégica

Fontes: Base_PowerBI.xlsx (gerado pelo processar_dados_mercado.py)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ============================================================
# CONFIGURAÇÃO GERAL
# ============================================================
st.set_page_config(
    page_title="Gestão | Mercado duBairro",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTO_FIXO = 16913.46
META_LIQUIDA = 0.15

# Paleta de cores do Mercado duBairro
COLORS = {
    'yellow': '#FFC107',
    'dark': '#2D2D2D',
    'gray': '#666666',
    'green': '#27AE60',
    'red': '#E74C3C',
    'blue': '#2E86C1',
    'light_gray': '#F5F5F5',
    'orange': '#F39C12',
    'green_dark': '#1E8449',
    'green_light': '#82E0AA',
    'yellow_light': '#F9E79F',
    'red_light': '#F5B7B1',
}

CATEGORY_COLORS = px.colors.qualitative.Set2


# ============================================================
# CSS CUSTOMIZADO
# ============================================================
st.markdown("""
<style>
    /* Fundo geral */
    .stApp { background-color: #FAFAFA; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #2D2D2D;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #FFFFFF !important;
        font-size: 14px;
    }

    /* Cards de KPI */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #FFC107;
        margin-bottom: 8px;
    }
    .kpi-title {
        font-size: 13px;
        color: #666;
        margin-bottom: 4px;
        font-weight: 500;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #2D2D2D;
        line-height: 1.2;
    }
    .kpi-subtitle {
        font-size: 11px;
        color: #999;
        margin-top: 4px;
    }
    .kpi-positive { color: #27AE60; }
    .kpi-negative { color: #E74C3C; }
    .kpi-neutral { color: #F39C12; }

    /* Story box */
    .story-box {
        background: #FFF9E6;
        border-left: 3px solid #FFC107;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin: 8px 0 16px 0;
        font-size: 13px;
        color: #555;
    }

    /* Alert boxes */
    .alert-red {
        background: #FDF2F2;
        border-left: 3px solid #E74C3C;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin: 4px 0;
        font-size: 12px;
    }
    .alert-green {
        background: #F0FFF0;
        border-left: 3px solid #27AE60;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin: 4px 0;
        font-size: 12px;
    }

    /* Section headers */
    .section-header {
        font-size: 18px;
        font-weight: 600;
        color: #2D2D2D;
        border-bottom: 2px solid #FFC107;
        padding-bottom: 6px;
        margin: 24px 0 12px 0;
    }

    /* Hide default streamlit footer and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Metric delta styling */
    [data-testid="stMetricDelta"] { font-size: 14px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# CARREGAMENTO DE DADOS
# ============================================================
@st.cache_data
def load_data():
    """Carrega todas as abas do Base_PowerBI.xlsx"""
    file_path = "Base_PowerBI.xlsx"
    data = {}

    data['vendas_mensais'] = pd.read_excel(file_path, sheet_name='fato_vendas_mensais')
    data['vendas_diarias'] = pd.read_excel(file_path, sheet_name='fato_vendas_diarias')
    data['produtos'] = pd.read_excel(file_path, sheet_name='dim_produtos')
    data['calendario'] = pd.read_excel(file_path, sheet_name='dim_calendario')
    data['yoy'] = pd.read_excel(file_path, sheet_name='comparativo_yoy')
    data['erosao'] = pd.read_excel(file_path, sheet_name='alertas_erosao_margem')

    return data


def render_kpi_card(title, value, subtitle="", color_class=""):
    """Renderiza um card de KPI estilizado"""
    sub_html = f'<div class="kpi-subtitle {color_class}">{subtitle}</div>' if subtitle else ''
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)


def render_story(text):
    """Renderiza caixa de história/insight"""
    st.markdown(f'<div class="story-box">💡 {text}</div>', unsafe_allow_html=True)


def render_section(text):
    """Renderiza cabeçalho de seção"""
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)

# ============================================================
# PÁGINA 1: RESUMO EXECUTIVO
# ============================================================
def page_resumo_executivo(data):
    st.markdown("## 📊 Resumo Executivo")
    st.markdown("*Como foi o mês? Estamos melhor ou pior que antes?*")
    st.markdown("---")

    vm = data['vendas_mensais']
    yoy = data['yoy']
    produtos = data['produtos']

    # KPIs macro
    faturamento = vm['Vlr_Venda'].sum()
    lucro_bruto = vm['Vlr_Lucro'].sum()
    lucro_liquido = lucro_bruto - CUSTO_FIXO
    margem_bruta = (lucro_bruto / faturamento * 100) if faturamento > 0 else 0
    margem_real = (lucro_liquido / faturamento * 100) if faturamento > 0 else 0
    ponto_equilibrio = CUSTO_FIXO / (margem_bruta / 100) if margem_bruta > 0 else 0
    folga_pe = ((faturamento / ponto_equilibrio) - 1) * 100 if ponto_equilibrio > 0 else 0
    total_cupons = vm['Qtde_Documentos'].sum()
    ticket_medio = faturamento / total_cupons if total_cupons > 0 else 0
    skus_ativos = len(produtos)

    # YoY do mês atual
    yoy_mes = yoy[yoy['Receita_2026'] > 0]
    if not yoy_mes.empty:
        var_receita = yoy_mes.iloc[-1]['Var_Receita_Pct']
        var_lucro = yoy_mes.iloc[-1]['Var_Lucro_Pct']
        cupons_25 = yoy_mes.iloc[-1]['Cupons_2025']
        receita_25 = yoy_mes.iloc[-1]['Receita_2025']
        ticket_25 = receita_25 / cupons_25 if cupons_25 > 0 else 0
        var_cupons = ((total_cupons - cupons_25) / cupons_25 * 100) if cupons_25 > 0 else 0
        var_ticket = ((ticket_medio - ticket_25) / ticket_25 * 100) if ticket_25 > 0 else 0
        mes_ref = yoy_mes.iloc[-1]['Mes']
    else:
        var_receita = var_lucro = var_cupons = var_ticket = 0
        mes_ref = ""

    # --- ROW 1: KPIs principais ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        delta_str = f"{'▲' if var_receita > 0 else '▼'} {var_receita:+.1f}% vs {mes_ref}/25"
        color = "kpi-positive" if var_receita > 0 else "kpi-negative"
        render_kpi_card("Faturamento do Mês", f"R$ {faturamento:,.2f}", delta_str, color)
    with c2:
        render_kpi_card("Lucro Líquido", f"R$ {lucro_liquido:,.2f}",
                        f"Bruto: R$ {lucro_bruto:,.2f} − Fixo: R$ {CUSTO_FIXO:,.2f}")
    with c3:
        status = "✅ Saudável" if margem_real > 20 else ("⚠️ Atenção" if margem_real > 15 else "🔴 Crítico")
        render_kpi_card("Margem Real", f"{margem_real:.1f}%", f"Meta: 15% | {status}")
    with c4:
        render_kpi_card("Ponto de Equilíbrio", f"R$ {ponto_equilibrio:,.0f}",
                        f"Folga de {folga_pe:.0f}%", "kpi-positive" if folga_pe > 50 else "kpi-negative")

    # --- ROW 2: KPIs complementares ---
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        delta_cup = f"{'▲' if var_cupons > 0 else '▼'} {var_cupons:+.1f}% vs ano anterior"
        render_kpi_card("Nº de Cupons (Clientes)", f"{total_cupons:,.0f}", delta_cup,
                        "kpi-positive" if var_cupons > 0 else "kpi-negative")
    with c6:
        delta_tk = f"{'▲' if var_ticket > 0 else '▼'} {var_ticket:+.1f}% vs ano anterior"
        render_kpi_card("Ticket Médio", f"R$ {ticket_medio:.2f}", delta_tk,
                        "kpi-positive" if var_ticket > 0 else "kpi-negative")
    with c7:
        render_kpi_card("SKUs Ativos", f"{skus_ativos:,}", f"Curva A: {len(produtos[produtos['Curva'] == 'A'])} produtos")
    with c8:
        delta_lucro_str = f"{'▲' if var_lucro > 0 else '▼'} {var_lucro:+.1f}% vs ano anterior"
        render_kpi_card("Variação YoY Lucro", f"{var_lucro:+.1f}%", delta_lucro_str,
                        "kpi-positive" if var_lucro > 0 else "kpi-negative")

    # --- HISTÓRIA ---
    if var_receita != 0:
        render_story(
            f"O faturamento caiu {abs(var_receita):.1f}% vs {mes_ref}/25, mas o lucro caiu apenas "
            f"{abs(var_lucro):.1f}%. Isso significa que estamos mais eficientes — vendemos menos, "
            f"mas lucramos mais por real vendido. O fluxo de clientes caiu {abs(var_cupons):.0f}%, "
            f"porém o ticket médio subiu {var_ticket:.0f}%. Os clientes fiéis estão comprando mais, "
            f"mas menos gente está entrando no mercado."
        )

    st.markdown("---")

    # --- GRÁFICOS ---
    col_left, col_right = st.columns([3, 2])

    with col_left:
        render_section("Evolução Mensal — 2025 a 2026")

        chart_data = []
        for _, row in yoy.iterrows():
            if row['Receita_2025'] > 0:
                chart_data.append({
                    'Mês': row['Mes'],
                    'Receita': row['Receita_2025'],
                    'Lucro': row['Lucro_2025'],
                    'Ano': '2025'
                })
            if row['Receita_2026'] > 0:
                chart_data.append({
                    'Mês': row['Mes'],
                    'Receita': row['Receita_2026'],
                    'Lucro': row['Lucro_2026'],
                    'Ano': '2026'
                })

        if chart_data:
            df_chart = pd.DataFrame(chart_data)
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            df_25 = df_chart[df_chart['Ano'] == '2025']
            fig.add_trace(go.Bar(
                x=df_25['Mês'], y=df_25['Receita'],
                name='Faturamento 2025', marker_color='#D5DBDB',
                text=[f"R${v/1000:.0f}k" for v in df_25['Receita']],
                textposition='outside', textfont_size=9
            ))

            df_26 = df_chart[df_chart['Ano'] == '2026']
            if not df_26.empty:
                fig.add_trace(go.Bar(
                    x=df_26['Mês'], y=df_26['Receita'],
                    name='Faturamento 2026', marker_color=COLORS['yellow'],
                    text=[f"R${v/1000:.0f}k" for v in df_26['Receita']],
                    textposition='outside', textfont_size=9
                ))

            fig.add_trace(go.Scatter(
                x=df_25['Mês'], y=df_25['Lucro'],
                name='Lucro 2025', line=dict(color=COLORS['green'], width=2, dash='dot'),
                mode='lines+markers'
            ), secondary_y=True)

            if not df_26.empty:
                fig.add_trace(go.Scatter(
                    x=df_26['Mês'], y=df_26['Lucro'],
                    name='Lucro 2026', line=dict(color=COLORS['green_dark'], width=3),
                    mode='lines+markers'
                ), secondary_y=True)

            fig.update_layout(
                barmode='group', height=380,
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", y=-0.15),
                plot_bgcolor='white',
                yaxis_title="Faturamento (R$)",
            )
            fig.update_yaxes(title_text="Lucro (R$)", secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        render_section("Participação por Categoria")
        vm_sorted = vm.sort_values('Vlr_Venda', ascending=False)

        def margin_color(md):
            if md > 55: return COLORS['green_dark']
            elif md > 40: return COLORS['green']
            elif md > 30: return COLORS['orange']
            else: return COLORS['red']

        vm_sorted['Color'] = vm_sorted['Markdown_Pct'].apply(margin_color)

        fig_tree = go.Figure(go.Treemap(
            labels=vm_sorted['Categoria'],
            parents=[''] * len(vm_sorted),
            values=vm_sorted['Vlr_Venda'],
            texttemplate="<b>%{label}</b><br>R$%{value:,.0f}<br>",
            marker=dict(colors=vm_sorted['Color']),
            hovertemplate="<b>%{label}</b><br>Faturamento: R$%{value:,.2f}<br><extra></extra>"
        ))
        fig_tree.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_tree, use_container_width=True)
        st.caption("🟢 Margem > 55%  |  🟡 Margem 40-55%  |  🟠 Margem 30-40%  |  🔴 Margem < 30%")

    # --- TOP 10 PRODUTOS POR LUCRO ---
    render_section("Top 10 Produtos por Lucro Absoluto")
    top10 = produtos.nlargest(10, 'Lucro_Total')
    top10['Custo'] = top10['Receita_Total'] - top10['Lucro_Total']

    fig_top = go.Figure()
    fig_top.add_trace(go.Bar(
        y=top10['Produto'], x=top10['Custo'],
        name='Custo', orientation='h', marker_color='#D5DBDB',
    ))
    fig_top.add_trace(go.Bar(
        y=top10['Produto'], x=top10['Lucro_Total'],
        name='Lucro', orientation='h', marker_color=COLORS['green'],
        text=[f"R$ {v:,.0f}" for v in top10['Lucro_Total']],
        textposition='outside', textfont_size=10
    ))
    fig_top.update_layout(
        barmode='stack', height=350,
        margin=dict(l=10, r=80, t=10, b=10),
        legend=dict(orientation="h", y=-0.1),
        plot_bgcolor='white',
        yaxis=dict(autorange="reversed"),
        xaxis_title="R$"
    )
    st.plotly_chart(fig_top, use_container_width=True)

    lucro_top10 = top10['Lucro_Total'].sum()
    lucro_total = produtos['Lucro_Total'].sum()
    pct_top10 = (lucro_top10 / lucro_total * 100) if lucro_total > 0 else 0
    render_story(
        f"Os 10 produtos com maior lucro absoluto juntos representam {pct_top10:.0f}% "
        f"de todo o lucro do mês. Banana Prata lidera com R$ {top10.iloc[0]['Lucro_Total']:,.0f}."
    )


# ============================================================
# PÁGINA 2: INTELIGÊNCIA DE PREÇOS
# ============================================================
def page_inteligencia_precos(data):
    st.markdown("## 💰 Inteligência de Preços")
    st.markdown("*Onde estou deixando dinheiro na mesa? Onde estou perdendo competitividade?*")
    st.markdown("---")

    vm = data['vendas_mensais']
    erosao = data['erosao']
    produtos = data['produtos']

    markdown_medio = (vm['Vlr_Venda'] * vm['Markdown_Pct'] / 100).sum() / vm['Vlr_Venda'].sum() * 100 if vm['Vlr_Venda'].sum() > 0 else 0

    custo_subiu = erosao[erosao['Alerta'].str.contains('SUBIU', na=False)]
    custo_caiu = erosao[erosao['Alerta'].str.contains('CAIU', na=False)]

    curva_a = produtos[produtos['Curva'] == 'A']
    margem_baixa = curva_a[curva_a['Margem_Media'] < 35]
    oportunidade = margem_baixa['Receita_Total'].sum() * 0.05

    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi_card("Markdown Médio Ponderado", f"{markdown_medio:.1f}%",
                        f"De cada R$ 1,00 vendido, R$ {markdown_medio/100:.2f} é margem bruta")
    with c2:
        render_kpi_card("Produtos com Custo Subindo", f"{len(custo_subiu)}",
                        f"Curva A com erosão de margem detectada", "kpi-negative")
    with c3:
        render_kpi_card("Oportunidade Estimada", f"R$ {oportunidade:,.0f}/mês",
                        f"{len(margem_baixa)} produtos Curva A com margem < 35%", "kpi-neutral")

    render_story(
        f"A margem média ponderada do mercado é {markdown_medio:.1f}%. "
        f"{len(custo_subiu)} produtos da Curva A tiveram aumento de custo na última entrada — "
        f"se os preços não forem reajustados, a margem vai erodir nos próximos meses."
    )

    st.markdown("---")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        render_section("Duelo de Produtos — Faturamento vs Margem")
        curva_a_plot = curva_a[curva_a['Receita_Total'] > 50].copy()

        fig_scatter = px.scatter(
            curva_a_plot, x='Receita_Total', y='Margem_Media',
            size='Lucro_Total', color='Classificacao', hover_name='Produto',
            hover_data={'Receita_Total': ':.2f', 'Lucro_Total': ':.2f', 'Margem_Media': ':.1f', 'Dias_Vendidos': True},
            color_discrete_map={
                '⭐ Estrela': COLORS['green'], '💰 Gerador de Caixa': COLORS['yellow'],
                '🔍 Oportunidade': COLORS['blue'], '⚠️ Peso Morto': COLORS['red'],
            },
            size_max=30,
        )

        avg_receita = curva_a_plot['Receita_Total'].mean()
        fig_scatter.add_hline(y=markdown_medio, line_dash="dash", line_color="#999",
                              annotation_text=f"Margem média: {markdown_medio:.0f}%")
        fig_scatter.add_vline(x=avg_receita, line_dash="dash", line_color="#999",
                              annotation_text=f"Receita média: R${avg_receita:.0f}")

        fig_scatter.update_layout(
            height=450, plot_bgcolor='white',
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title="Faturamento (R$)", yaxis_title="Margem (%)",
            legend=dict(orientation="h", y=-0.15),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_right:
        render_section("Ranking de Margem por Categoria")
        cat_rank = vm[['Categoria', 'Vlr_Venda', 'Vlr_Lucro', 'Markdown_Pct']].copy()
        cat_rank['Margem_Lucro'] = (cat_rank['Vlr_Lucro'] / cat_rank['Vlr_Venda'] * 100).round(1)
        cat_rank = cat_rank.sort_values('Markdown_Pct', ascending=False)

        def semaforo(md):
            if md > 55: return '🟢'
            elif md > 40: return '🟡'
            else: return '🔴'

        cat_rank['Status'] = cat_rank['Markdown_Pct'].apply(semaforo)
        cat_rank['Faturamento'] = cat_rank['Vlr_Venda'].apply(lambda x: f"R$ {x:,.0f}")
        cat_rank['Markdown'] = cat_rank['Markdown_Pct'].apply(lambda x: f"{x:.1f}%")

        st.dataframe(
            cat_rank[['Status', 'Categoria', 'Faturamento', 'Markdown']].reset_index(drop=True),
            use_container_width=True, height=420, hide_index=True,
        )

    # --- TABELA DE EROSÃO ---
    render_section("🚨 Alerta de Erosão de Margem — Curva A")
    st.markdown("*Produtos onde o custo de reposição mudou significativamente.*")

    tab1, tab2 = st.tabs(["🔴 Custo Subiu (Atenção!)", "🟢 Custo Caiu (Oportunidade)"])

    with tab1:
        if not custo_subiu.empty:
            df_show = custo_subiu[['Produto', 'Vlr_Venda', 'Margem_Pct', 'Markdown_Pct',
                                   'Markdown_Ult_Entrada', 'Erosao_Margem']].copy()
            df_show.columns = ['Produto', 'Faturamento', 'Margem %', 'Markdown Atual',
                               'Markdown Ult. Entrada', 'Erosão (pts)']
            df_show = df_show.sort_values('Erosão (pts)', ascending=False)
            st.dataframe(df_show.reset_index(drop=True), use_container_width=True, hide_index=True)
            render_story(
                f"Esses {len(custo_subiu)} produtos tiveram o custo de reposição aumentado. "
                f"Se não reajustar o preço, a margem futura vai cair."
            )
        else:
            st.success("Nenhum produto com custo subindo detectado!")

    with tab2:
        if not custo_caiu.empty:
            df_show = custo_caiu[['Produto', 'Vlr_Venda', 'Margem_Pct', 'Markdown_Pct',
                                   'Markdown_Ult_Entrada', 'Erosao_Margem']].copy()
            df_show.columns = ['Produto', 'Faturamento', 'Margem %', 'Markdown Atual',
                               'Markdown Ult. Entrada', 'Erosão (pts)']
            df_show = df_show.sort_values('Erosão (pts)')
            st.dataframe(df_show.reset_index(drop=True), use_container_width=True, hide_index=True)
            render_story(
                f"Boa notícia! Esses {len(custo_caiu)} produtos tiveram queda no custo. "
                f"Mantenha o preço e aumente a margem, ou reduza e ganhe competitividade."
            )
        else:
            st.info("Nenhum produto com custo caindo detectado.")


# ============================================================
# PÁGINA 3: MAPA DE PRODUTOS
# ============================================================
def page_mapa_produtos(data):
    st.markdown("## 🗺️ Mapa de Produtos — Matriz de Rentabilidade")
    st.markdown("*Se eu tivesse que cortar 50 produtos ou reforçar 50, quais seriam?*")
    st.markdown("---")

    produtos = data['produtos']

    estrelas = produtos[produtos['Classificacao'].str.contains('Estrela')]
    geradores = produtos[produtos['Classificacao'].str.contains('Gerador')]
    oportunidades = produtos[produtos['Classificacao'].str.contains('Oportunidade')]
    peso_morto = produtos[produtos['Classificacao'].str.contains('Peso Morto')]

    lucro_total = produtos['Lucro_Total'].sum()

    prod_sorted = produtos.sort_values('Lucro_Total', ascending=False)
    prod_sorted['Lucro_Acum'] = prod_sorted['Lucro_Total'].cumsum()
    target_80 = lucro_total * 0.8
    n_80 = (prod_sorted['Lucro_Acum'] <= target_80).sum() + 1

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("⭐ Estrelas", f"{len(estrelas)}",
                        f"Alto giro + Alta margem | R$ {estrelas['Lucro_Total'].sum():,.0f} lucro")
    with c2:
        render_kpi_card("💰 Geradores de Caixa", f"{len(geradores)}",
                        f"Alto giro + Baixa margem | R$ {geradores['Lucro_Total'].sum():,.0f} lucro")
    with c3:
        render_kpi_card("🔍 Oportunidades", f"{len(oportunidades)}",
                        f"Baixo giro + Alta margem | R$ {oportunidades['Lucro_Total'].sum():,.0f} lucro")
    with c4:
        render_kpi_card("⚠️ Peso Morto", f"{len(peso_morto)}",
                        f"Baixo giro + Baixa margem | R$ {peso_morto['Lucro_Total'].sum():,.0f} lucro")

    render_story(
        f"Apenas {n_80} produtos (de {len(produtos):,}) geram 80% do lucro total. "
        f"As {len(estrelas)} Estrelas são intocáveis — nunca podem faltar."
    )

    st.markdown("---")

    render_section("Matriz de Rentabilidade — Giro vs Margem")
    prod_plot = produtos[produtos['Receita_Total'] > 20].copy()

    fig_matrix = px.scatter(
        prod_plot, x='Giro', y='Margem_Media', size='Receita_Total',
        color='Classificacao', hover_name='Produto',
        hover_data={'Receita_Total': ':.2f', 'Lucro_Total': ':.2f', 'Dias_Vendidos': True, 'Curva': True},
        color_discrete_map={
            '⭐ Estrela': COLORS['green'], '💰 Gerador de Caixa': COLORS['yellow'],
            '🔍 Oportunidade': COLORS['blue'], '⚠️ Peso Morto': '#CCCCCC',
        },
        size_max=35,
    )

    fig_matrix.add_hline(y=50, line_dash="dash", line_color="#999", annotation_text="Margem 50%")
    fig_matrix.add_vline(x=0.6, line_dash="dash", line_color="#999", annotation_text="Giro 60%")

    fig_matrix.add_annotation(x=0.85, y=85, text="⭐ ESTRELAS", showarrow=False, font=dict(size=12, color=COLORS['green']))
    fig_matrix.add_annotation(x=0.85, y=15, text="💰 GERADORES", showarrow=False, font=dict(size=12, color=COLORS['orange']))
    fig_matrix.add_annotation(x=0.15, y=85, text="🔍 OPORTUNIDADES", showarrow=False, font=dict(size=12, color=COLORS['blue']))
    fig_matrix.add_annotation(x=0.15, y=15, text="⚠️ PESO MORTO", showarrow=False, font=dict(size=12, color=COLORS['red']))

    fig_matrix.update_layout(
        height=500, plot_bgcolor='white',
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Giro (% dos dias com venda)", yaxis_title="Margem Média (%)",
        xaxis=dict(range=[-0.05, 1.05], tickformat='.0%'),
        legend=dict(orientation="h", y=-0.12),
    )
    st.plotly_chart(fig_matrix, use_container_width=True)

    col_left, col_right = st.columns(2)

    with col_left:
        render_section("⭐ Estrelas — Proteger a Todo Custo")
        if not estrelas.empty:
            df_e = estrelas[['Produto', 'Dias_Vendidos', 'Margem_Media', 'Receita_Total', 'Lucro_Total']].copy()
            df_e.columns = ['Produto', 'Dias Vendidos', 'Margem %', 'Receita', 'Lucro']
            st.dataframe(df_e.sort_values('Lucro', ascending=False).reset_index(drop=True), use_container_width=True, hide_index=True)

        render_section("🔍 Oportunidades — Dar Visibilidade (Top 15)")
        oport_top = oportunidades.nlargest(15, 'Lucro_Total')
        if not oport_top.empty:
            df_o = oport_top[['Produto', 'Dias_Vendidos', 'Margem_Media', 'Receita_Total', 'Lucro_Total']].copy()
            df_o.columns = ['Produto', 'Dias Vendidos', 'Margem %', 'Receita', 'Lucro']
            st.dataframe(df_o.reset_index(drop=True), use_container_width=True, hide_index=True)

    with col_right:
        render_section("💰 Geradores de Caixa — Renegociar ou Aceitar")
        if not geradores.empty:
            df_g = geradores[['Produto', 'Dias_Vendidos', 'Margem_Media', 'Receita_Total', 'Lucro_Total']].copy()
            df_g.columns = ['Produto', 'Dias Vendidos', 'Margem %', 'Receita', 'Lucro']
            st.dataframe(df_g.sort_values('Receita', ascending=False).reset_index(drop=True), use_container_width=True, hide_index=True)

        render_section("⚠️ Peso Morto — Avaliar Remoção (Top 15)")
        pm_top = peso_morto.nlargest(15, 'Receita_Total')
        if not pm_top.empty:
            df_pm = pm_top[['Produto', 'Dias_Vendidos', 'Margem_Media', 'Receita_Total', 'Lucro_Total']].copy()
            df_pm.columns = ['Produto', 'Dias Vendidos', 'Margem %', 'Receita', 'Lucro']
            st.dataframe(df_pm.reset_index(drop=True), use_container_width=True, hide_index=True)

# ============================================================
# PÁGINA 4: DIAGNÓSTICO DE FATURAMENTO
# ============================================================
def page_diagnostico(data):
    st.markdown("## 🔍 Diagnóstico de Faturamento")
    st.markdown("*Foi porque vieram menos clientes, porque gastaram menos, ou porque o mix mudou?*")
    st.markdown("---")

    vm = data['vendas_mensais']
    vd = data['vendas_diarias']
    yoy = data['yoy']

    faturamento = vm['Vlr_Venda'].sum()
    cupons = vm['Qtde_Documentos'].sum()
    ticket = faturamento / cupons if cupons > 0 else 0

    yoy_mes = yoy[yoy['Receita_2026'] > 0]
    if not yoy_mes.empty:
        row = yoy_mes.iloc[-1]
        cupons_25 = row['Cupons_2025']
        receita_25 = row['Receita_2025']
        ticket_25 = receita_25 / cupons_25 if cupons_25 > 0 else 0
        var_cupons = ((cupons - cupons_25) / cupons_25 * 100) if cupons_25 > 0 else 0
        var_ticket = ((ticket - ticket_25) / ticket_25 * 100) if ticket_25 > 0 else 0
    else:
        cupons_25 = ticket_25 = var_cupons = var_ticket = receita_25 = 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("FATURAMENTO = ", f"R$ {faturamento:,.0f}", "Cupons × Ticket Médio")
    with c2:
        render_kpi_card("Nº Cupons (Clientes)", f"{cupons:,.0f}",
                        f"{'▼' if var_cupons < 0 else '▲'} {var_cupons:+.0f}% vs ano anterior",
                        "kpi-negative" if var_cupons < 0 else "kpi-positive")
    with c3:
        render_kpi_card("× Ticket Médio", f"R$ {ticket:.2f}",
                        f"{'▲' if var_ticket > 0 else '▼'} {var_ticket:+.0f}% vs ano anterior",
                        "kpi-positive" if var_ticket > 0 else "kpi-negative")
    with c4:
        if receita_25 > 0 and cupons_25 > 0:
            impacto_cupons = (cupons - cupons_25) * ticket_25
            impacto_ticket = (ticket - ticket_25) * cupons
            render_kpi_card("Diagnóstico",
                            "Fluxo ↓" if abs(impacto_cupons) > abs(impacto_ticket) else "Ticket ↓",
                            f"Cupons: R$ {impacto_cupons:+,.0f} | Ticket: R$ {impacto_ticket:+,.0f}")
        else:
            render_kpi_card("Diagnóstico", "—", "Sem dados YoY")

    render_story(
        f"O faturamento é {cupons:,.0f} cupons × R$ {ticket:.2f} de ticket médio. "
        f"O fluxo de clientes caiu {abs(var_cupons):.0f}% vs ano passado, mas cada cliente "
        f"gastou {var_ticket:.0f}% a mais. O problema principal é atração de novos clientes."
    )

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        render_section("Contribuição por Categoria")
        vm_waterfall = vm[['Categoria', 'Vlr_Venda', 'Vlr_Lucro']].copy()
        vm_waterfall = vm_waterfall.sort_values('Vlr_Venda', ascending=False).head(12)

        fig_cat = go.Figure(go.Bar(
            x=vm_waterfall['Categoria'], y=vm_waterfall['Vlr_Venda'],
            marker_color=[COLORS['green'] if l > 0 else COLORS['red'] for l in vm_waterfall['Vlr_Lucro']],
            text=[f"R${v:,.0f}" for v in vm_waterfall['Vlr_Venda']],
            textposition='outside', textfont_size=9,
        ))
        fig_cat.update_layout(
            height=380, plot_bgcolor='white',
            margin=dict(l=10, r=10, t=10, b=80),
            xaxis_tickangle=-45, yaxis_title="Faturamento (R$)"
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_right:
        render_section("Faturamento por Dia da Semana")
        vd_copy = vd.copy()
        vd_copy['Data'] = pd.to_datetime(vd_copy['Data'])
        vd_copy['Dia_Semana'] = vd_copy['Data'].dt.day_name()

        dia_map = {'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
                   'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
        vd_copy['Dia_Semana_PT'] = vd_copy['Dia_Semana'].map(dia_map)

        dia_order = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        daily_sum = vd_copy.groupby([vd_copy['Data'].dt.isocalendar().week.rename('Semana'), 'Dia_Semana_PT'])['Vlr_Venda'].sum().reset_index()

        heatmap_pivot = daily_sum.pivot(index='Semana', columns='Dia_Semana_PT', values='Vlr_Venda').fillna(0)
        heatmap_pivot = heatmap_pivot.reindex(columns=[d for d in dia_order if d in heatmap_pivot.columns])

        fig_heat = px.imshow(
            heatmap_pivot.values,
            x=heatmap_pivot.columns,
            y=[f"Sem {int(s)}" for s in heatmap_pivot.index],
            color_continuous_scale='YlOrRd',
            labels=dict(x="Dia da Semana", y="Semana", color="Faturamento"),
            text_auto='.0f'
        )
        fig_heat.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_heat, use_container_width=True)

    render_section("Faturamento Médio por Dia da Semana")
    dia_avg = vd_copy.groupby('Dia_Semana_PT').agg(
        Fat_Total=('Vlr_Venda', 'sum'), Dias=('Data', 'nunique')
    ).reset_index()
    dia_avg['Fat_Medio'] = dia_avg['Fat_Total'] / dia_avg['Dias']
    dia_avg['Dia_Semana_PT'] = pd.Categorical(dia_avg['Dia_Semana_PT'], categories=dia_order, ordered=True)
    dia_avg = dia_avg.sort_values('Dia_Semana_PT')

    fig_dia = go.Figure(go.Bar(
        x=dia_avg['Dia_Semana_PT'], y=dia_avg['Fat_Medio'],
        marker_color=[COLORS['yellow'] if d != 'Domingo' else COLORS['red'] for d in dia_avg['Dia_Semana_PT']],
        text=[f"R$ {v:,.0f}" for v in dia_avg['Fat_Medio']], textposition='outside',
    ))
    fig_dia.update_layout(height=280, plot_bgcolor='white', margin=dict(l=10, r=10, t=10, b=10), yaxis_title="Faturamento Médio (R$)")
    st.plotly_chart(fig_dia, use_container_width=True)

    best_day = dia_avg.loc[dia_avg['Fat_Medio'].idxmax(), 'Dia_Semana_PT']
    worst_day = dia_avg.loc[dia_avg['Fat_Medio'].idxmin(), 'Dia_Semana_PT']
    render_story(f"{best_day} é o dia mais forte, {worst_day} é o mais fraco. Considere promoções para {worst_day} e reforço de estoque para {best_day}.")


# ============================================================
# PÁGINA 5: SAZONALIDADE E TENDÊNCIAS
# ============================================================
def page_sazonalidade(data):
    st.markdown("## 📈 Sazonalidade e Tendências")
    st.markdown("*O que vai acontecer? Como me preparar?*")
    st.markdown("---")

    yoy = data['yoy']
    produtos = data['produtos']

    fat_anual_25 = yoy['Receita_2025'].sum()
    fat_medio_mensal_25 = fat_anual_25 / 12
    lucro_anual_25 = yoy['Lucro_2025'].sum()

    meses_26 = yoy[yoy['Receita_2026'] > 0]
    fat_acum_26 = meses_26['Receita_2026'].sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Faturamento 2025", f"R$ {fat_anual_25:,.0f}", f"Média mensal: R$ {fat_medio_mensal_25:,.0f}")
    with c2:
        render_kpi_card("Lucro 2025 (limpo)", f"R$ {lucro_anual_25:,.0f}",
                        f"Margem média: {(lucro_anual_25/fat_anual_25*100):.1f}%")
    with c3:
        render_kpi_card("Acumulado 2026", f"R$ {fat_acum_26:,.0f}", f"{len(meses_26)} mês(es) processado(s)")
    with c4:
        jan_25 = yoy[yoy['Mes_Num'] == 1]['Receita_2025'].values[0] if len(yoy[yoy['Mes_Num'] == 1]) > 0 else 0
        fev_25 = yoy[yoy['Mes_Num'] == 2]['Receita_2025'].values[0] if len(yoy[yoy['Mes_Num'] == 2]) > 0 else 0
        jan_26 = yoy[yoy['Mes_Num'] == 1]['Receita_2026'].values[0] if len(yoy[yoy['Mes_Num'] == 1]) > 0 else 0

        if jan_25 > 0 and fev_25 > 0 and jan_26 > 0:
            sazonalidade_fev = fev_25 / jan_25
            projecao_fev = jan_26 * sazonalidade_fev
            render_kpi_card("Projeção Fev/26", f"R$ {projecao_fev:,.0f}",
                            f"Baseado na sazonalidade (Fev/25 foi {(sazonalidade_fev-1)*100:+.1f}% vs Jan/25)")
        else:
            render_kpi_card("Projeção Fev/26", "—", "Dados insuficientes")

    st.markdown("---")

    col_left, col_right = st.columns([3, 2])
    meses_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    with col_left:
        render_section("Sazonalidade do Faturamento — 2025 vs 2026")

        fig_saz = go.Figure()
        fig_saz.add_trace(go.Scatter(
            x=meses_labels, y=yoy['Receita_2025'],
            name='2025', mode='lines+markers+text',
            line=dict(color='#AAAAAA', width=2), marker=dict(size=8),
            text=[f"R${v/1000:.0f}k" for v in yoy['Receita_2025']],
            textposition='top center', textfont_size=9,
        ))

        receitas_26 = yoy['Receita_2026'].tolist()
        meses_26_labels = [meses_labels[i] for i, v in enumerate(receitas_26) if v > 0]
        receitas_26_vals = [v for v in receitas_26 if v > 0]

        if receitas_26_vals:
            fig_saz.add_trace(go.Scatter(
                x=meses_26_labels, y=receitas_26_vals,
                name='2026', mode='lines+markers+text',
                line=dict(color=COLORS['yellow'], width=3), marker=dict(size=12, symbol='diamond'),
                text=[f"R${v/1000:.0f}k" for v in receitas_26_vals],
                textposition='bottom center', textfont_size=10,
            ))

        fig_saz.add_hline(y=fat_medio_mensal_25, line_dash="dot", line_color="#CCC",
                           annotation_text=f"Média 2025: R${fat_medio_mensal_25/1000:.0f}k")
        fig_saz.update_layout(height=400, plot_bgcolor='white', margin=dict(l=20, r=20, t=30, b=20),
                               yaxis_title="Faturamento (R$)", legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_saz, use_container_width=True)

    with col_right:
        render_section("Índice de Sazonalidade 2025")
        yoy_saz = yoy.copy()
        yoy_saz['Indice'] = yoy_saz['Receita_2025'] / fat_medio_mensal_25

        fig_idx = go.Figure(go.Bar(
            x=meses_labels, y=yoy_saz['Indice'],
            marker_color=[COLORS['green'] if v > 1 else COLORS['red'] for v in yoy_saz['Indice']],
            text=[f"{v:.2f}" for v in yoy_saz['Indice']], textposition='outside', textfont_size=10,
        ))
        fig_idx.add_hline(y=1, line_dash="solid", line_color="#999", line_width=2)
        fig_idx.update_layout(height=400, plot_bgcolor='white', margin=dict(l=20, r=20, t=30, b=20),
                               yaxis_title="Índice (1.0 = média)")
        st.plotly_chart(fig_idx, use_container_width=True)
        st.caption("Acima de 1.0 = mês acima da média | Abaixo de 1.0 = mês abaixo da média")

    render_section("Evolução do Mix de Produtos — 2025")
    skus_por_mes = yoy[['Mes', 'SKUs_2025']].copy()
    skus_por_mes = skus_por_mes[skus_por_mes['SKUs_2025'] > 0]

    if not skus_por_mes.empty:
        fig_skus = go.Figure(go.Scatter(
            x=skus_por_mes['Mes'], y=skus_por_mes['SKUs_2025'],
            mode='lines+markers+text', line=dict(color=COLORS['blue'], width=2),
            marker=dict(size=10), text=skus_por_mes['SKUs_2025'].astype(int).astype(str), textposition='top center',
        ))
        fig_skus.update_layout(height=280, plot_bgcolor='white', margin=dict(l=20, r=20, t=30, b=20), yaxis_title="Nº de SKUs vendidos")
        st.plotly_chart(fig_skus, use_container_width=True)

        primeiro = skus_por_mes.iloc[0]['SKUs_2025']
        ultimo = skus_por_mes.iloc[-1]['SKUs_2025']
        render_story(
            f"O mix encolheu de {int(primeiro)} para {int(ultimo)} SKUs ao longo de 2025 "
            f"({int(ultimo - primeiro)} produtos). Menos variedade pode significar menos motivos para o cliente entrar."
        )

    render_section("Tendência — Faturamento 12 Meses Móveis")
    receitas_all = yoy['Receita_2025'].tolist()
    for _, row in yoy.iterrows():
        if row['Receita_2026'] > 0:
            receitas_all.append(row['Receita_2026'])

    if len(receitas_all) >= 12:
        rolling = []
        labels = []
        for i in range(11, len(receitas_all)):
            rolling.append(sum(receitas_all[max(0, i-11):i+1]))
            if i < 12:
                labels.append(meses_labels[i] + '/25')
            else:
                labels.append(meses_labels[i-12] + '/26')

        fig_rolling = go.Figure(go.Scatter(
            x=labels, y=rolling, mode='lines+markers',
            line=dict(color=COLORS['blue'], width=3),
            fill='tozeroy', fillcolor='rgba(46,134,193,0.1)',
        ))
        fig_rolling.update_layout(height=280, plot_bgcolor='white', margin=dict(l=20, r=20, t=30, b=20),
                                   yaxis_title="Faturamento Acum. 12 meses (R$)")
        st.plotly_chart(fig_rolling, use_container_width=True)

        if len(rolling) > 1:
            trend_pct = ((rolling[-1] - rolling[0]) / rolling[0] * 100)
            direction = "subindo" if trend_pct > 0 else "caindo"
            render_story(
                f"O faturamento acumulado de 12 meses está em R$ {rolling[-1]:,.0f}. "
                f"Tendência {direction} ({trend_pct:+.1f}%). "
                f"{'O negócio está crescendo.' if trend_pct > 0 else 'O negócio está encolhendo — hora de agir.'}"
            )


# ============================================================
# SIDEBAR E NAVEGAÇÃO
# ============================================================
def main():
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🏪 Mercado duBairro")
        st.markdown("**Painel dos Sócios**")
        st.markdown("---")

        pagina = st.radio(
            "Navegação",
            [
                "📊 Resumo Executivo",
                "💰 Inteligência de Preços",
                "🗺️ Mapa de Produtos",
                "🔍 Diagnóstico de Faturamento",
                "📈 Sazonalidade e Tendências",
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("##### ⚙️ Informações")
        st.markdown(f"**Custo Fixo:** R$ {CUSTO_FIXO:,.2f}")
        st.markdown(f"**Meta Líquida:** {META_LIQUIDA*100:.0f}%")
        st.markdown("---")
        st.caption("Mercado duBairro © 2026")
        st.caption("Dashboard de Gestão v1.0")

    try:
        data = load_data()
    except FileNotFoundError:
        st.error("⚠️ Arquivo **Base_PowerBI.xlsx** não encontrado! "
                 "Certifique-se de que ele está no mesmo diretório do app.py.")
        st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.stop()

    if "Resumo" in pagina:
        page_resumo_executivo(data)
    elif "Preços" in pagina:
        page_inteligencia_precos(data)
    elif "Mapa" in pagina:
        page_mapa_produtos(data)
    elif "Diagnóstico" in pagina:
        page_diagnostico(data)
    elif "Sazonalidade" in pagina:
        page_sazonalidade(data)


if __name__ == "__main__":
    main()
