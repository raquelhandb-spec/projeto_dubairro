import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configuração da página
st.set_page_config(
    page_title="Dashboard Mercado duBairro",
    page_icon="🛒",
    layout="wide"
)

# Carregar dados
@st.cache_data
def load_data():
    # Tenta carregar o arquivo processado. 
    # Certifique-se que o 'vendas_processadas.csv' está na mesma pasta!
    df = pd.read_csv('vendas_processadas.csv')
    try:
        df['Data'] = pd.to_datetime(df['Data'])
    except:
        pass # Se der erro na conversão, segue o jogo
    return df

# Tentar carregar os dados
try:
    df = load_data()
except FileNotFoundError:
    st.error("ERRO: O arquivo 'vendas_processadas.csv' não foi encontrado na pasta. Rode o script de processamento antes.")
    st.stop()

# Sidebar com logo e menu
with st.sidebar:
    # --- AJUSTE MINIMALISTA DA LOGO AQUI ---
    # Original era: use_container_width=True (ficava gigante)
    # Agora: width=150 (fica discreto e elegante)
    try:
        st.image("logo_dubairro.png", width=150)
    except:
        st.warning("Logo não encontrada")
    
    st.write("---")
    
    # Menu Original do Claude
    selected = option_menu(
        menu_title=None,
        options=["Visão Geral", "Vendas por Período", "Análise de Produtos", "Top Clientes"],
        icons=["house", "calendar", "box", "people"],
        menu_icon="cast",
        default_index=0,
    )

# Dashboard principal
st.title(f"Dashboard de Vendas - {selected}")

# Lógica para cada página do menu (Código Original mantido)
if selected == "Visão Geral":
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    receita_total = df['Valor_Total'].sum()
    ticket_medio = df['Valor_Total'].mean()
    total_vendas = len(df)
    total_produtos = df['Qtde_Produtos'].sum()
    
    col1.metric("Receita Total", f"R$ {receita_total:,.2f}")
    col2.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
    col3.metric("Total de Vendas", f"{total_vendas:,}")
    col4.metric("Total de Produtos", f"{total_produtos:,}")
    
    st.markdown("---")
    
    # Gráfico de vendas diárias
    st.subheader("Evolução das Vendas")
    vendas_diarias = df.groupby('Data')['Valor_Total'].sum().reset_index()
    fig_diarias = px.line(vendas_diarias, x='Data', y='Valor_Total')
    st.plotly_chart(fig_diarias, use_container_width=True)
    
    # Gráfico de vendas por forma de pagamento
    col_pag1, col_pag2 = st.columns(2)
    
    with col_pag1:
        st.subheader("Formas de Pagamento")
        vendas_pagamento = df.groupby('Forma_Pagamento')['Valor_Total'].sum().reset_index()
        fig_pagamento = px.pie(vendas_pagamento, values='Valor_Total', names='Forma_Pagamento')
        st.plotly_chart(fig_pagamento, use_container_width=True)
    
    with col_pag2:
        st.subheader("Ticket Médio por Pagamento")
        ticket_pagamento = df.groupby('Forma_Pagamento')['Valor_Total'].mean().reset_index().sort_values('Valor_Total', ascending=False)
        fig_ticket_pag = px.bar(ticket_pagamento, x='Valor_Total', y='Forma_Pagamento', orientation='h')
        st.plotly_chart(fig_ticket_pag, use_container_width=True)

elif selected == "Vendas por Período":
    st.subheader("Análise Temporal")
    
    # Filtro de data
    col_date1, col_date2 = st.columns(2)
    min_date = df['Data'].min().date() if hasattr(df['Data'], 'dt') else df['Data'].min()
    max_date = df['Data'].max().date() if hasattr(df['Data'], 'dt') else df['Data'].max()
    
    data_inicial = col_date1.date_input("Data Inicial", min_date)
    data_final = col_date2.date_input("Data Final", max_date)
    
    # Aplica filtro (garantindo conversão para data)
    mask = (df['Data'].dt.date >= data_inicial) & (df['Data'].dt.date <= data_final)
    df_filtrado = df[mask]
    
    # Vendas por dia da semana
    st.subheader("Vendas por Dia da Semana")
    # Ordem correta dos dias
    dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    vendas_dia_semana = df_filtrado.groupby('Dia_Semana')['Valor_Total'].mean().reindex(dias_ordem).reset_index()
    
    fig_dia_semana = px.bar(vendas_dia_semana, x='Dia_Semana', y='Valor_Total')
    st.plotly_chart(fig_dia_semana, use_container_width=True)
    
    # Vendas por mês
    st.subheader("Vendas Mensais")
    vendas_mensais = df_filtrado.groupby(df_filtrado['Data'].dt.to_period('M').astype(str))['Valor_Total'].sum().reset_index()
    fig_mensal = px.bar(vendas_mensais, x='Data', y='Valor_Total')
    st.plotly_chart(fig_mensal, use_container_width=True)

elif selected == "Análise de Produtos":
    st.subheader("Performance de Produtos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top 10 Receita")
        top_produtos_receita = df.groupby('Produto')['Valor_Total'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_top_receita = px.bar(top_produtos_receita, x='Valor_Total', y='Produto', orientation='h')
        fig_top_receita.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top_receita, use_container_width=True)
    
    with col2:
        st.markdown("#### Top 10 Volume")
        top_produtos_qtde = df.groupby('Produto')['Qtde_Produtos'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_top_qtde = px.bar(top_produtos_qtde, x='Qtde_Produtos', y='Produto', orientation='h')
        fig_top_qtde.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top_qtde, use_container_width=True)

elif selected == "Top Clientes":
    st.subheader("Melhores Clientes")
    
    # Remove cliente desconhecido e agrupa
    df_clientes = df[df['Cliente'] != 'CLIENTE DESCONHECIDO']
    top_clientes = df_clientes.groupby('Cliente')['Valor_Total'].sum().sort_values(ascending=False).head(10).reset_index()
    
    fig_clientes = px.bar(top_clientes, x='Valor_Total', y='Cliente', orientation='h')
    fig_clientes.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_clientes, use_container_width=True)
    
    st.dataframe(top_clientes, use_container_width=True)
