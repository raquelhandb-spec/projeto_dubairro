import pandas as pd
import glob
import os

print("============================================================")
print("   MERCADO duBAIRRO — Processador de Dados (CORRIGIDO)      ")
print("============================================================")

# 1. Encontrar os arquivos de entrada
print("🔍 Procurando arquivos de dados...")

# Tenta achar arquivos que tenham "vendas" ou "produtos" no nome
try:
    # Procura qualquer CSV de vendas
    lista_vendas = glob.glob("*vendas*.csv")
    if not lista_vendas:
        # Se não achar CSV, tenta achar dentro do XLSX base se ele existir como fonte
        raise FileNotFoundError("Nenhum CSV de vendas encontrado.")
    
    arquivo_vendas = lista_vendas[0]
    print(f"   -> Vendas: {arquivo_vendas}")

    # Procura arquivo de produtos
    lista_produtos = glob.glob("*produto*.csv")
    if not lista_produtos:
        raise FileNotFoundError("Nenhum CSV de produtos encontrado.")
        
    arquivo_produtos = lista_produtos[0]
    print(f"   -> Produtos: {arquivo_produtos}")

except Exception as e:
    print(f"❌ ERRO: {e}")
    print("Certifique-se de que os arquivos 'fato_vendas...' e 'dim_produtos...' estão nesta pasta.")
    exit()

# 2. Carregar e Processar
print("🍳 Cozinhando os dados...")
df_vendas = pd.read_csv(arquivo_vendas)
df_produtos = pd.read_csv(arquivo_produtos)

# Limpeza básica
df_vendas.columns = [c.strip() for c in df_vendas.columns]
df_produtos.columns = [c.strip() for c in df_produtos.columns]

# Cruzamento (Vendas + Produtos)
# Pega a primeira coluna como chave (geralmente Cod_Produto)
col_chave_vendas = df_vendas.columns[0]
col_chave_prod = df_produtos.columns[0]

df_final = pd.merge(df_vendas, df_produtos, left_on=col_chave_vendas, right_on=col_chave_prod, how='left')

# Ajustes finais para o Dashboard Original
if 'Valor' in df_final.columns: df_final.rename(columns={'Valor': 'Valor_Total'}, inplace=True)
if 'Qtd' in df_final.columns: df_final.rename(columns={'Qtd': 'Qtde_Produtos'}, inplace=True)
if 'Nome_Produto' in df_final.columns: df_final.rename(columns={'Nome_Produto': 'Produto'}, inplace=True)

# Garante datas
col_data = [c for c in df_final.columns if 'Data' in c or 'data' in c][0]
df_final['Data'] = pd.to_datetime(df_final[col_data])

# 3. SALVAR (AQUI ESTÁ A CORREÇÃO!)
# Antes salvava em /mnt/user-data/... (Erro no Windows)
# Agora salva na pasta atual
nome_arquivo_final = "Base_PowerBI.xlsx"

print(f"💾 Salvando arquivo final: {nome_arquivo_final}...")
# Salva como Excel para compatibilidade com o app original
df_final.to_excel(nome_arquivo_final, index=False)

# Também salva como CSV por segurança (é mais leve)
df_final.to_csv("vendas_processadas.csv", index=False)

print(f"\n✅ SUCESSO! Arquivos criados na sua pasta:")
print(f"   1. {nome_arquivo_final}")
print(f"   2. vendas_processadas.csv")
print("👉 Agora você pode fazer o upload para o GitHub!")
