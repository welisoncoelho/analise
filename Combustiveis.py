import pandas as pd
import streamlit as st

# Substitua 'precos_combustiveis.xlsx' pelo nome do seu arquivo Excel
arquivo_excel = 'precos_combustiveis.xlsx'

# Carregue o arquivo Excel com pandas
df = pd.read_excel(arquivo_excel, dtype=str)

# Filtros selectbox no sidebar
filtro_estado = st.sidebar.selectbox('Selecione o Estado', ["Todos"] + list(df['ESTADO'].unique()))
filtro_produto = st.sidebar.selectbox('Selecione o Produto', ["Todos"] + list(df['PRODUTO'].unique()))

# Adicione o filtro de município se o estado não for "Todos"
if filtro_estado != "Todos":
    municipios_estado = df[df['ESTADO'] == filtro_estado]['MUNICÍPIO'].unique()
    filtro_municipio = st.sidebar.selectbox('Selecione o Município', ["Todos"] + list(municipios_estado))
else:
    filtro_municipio = "Todos"

# Filtros adicionais
filtro_bandeira = st.sidebar.selectbox('Selecione a Bandeira', ["Todos"] + list(df['BANDEIRA'].unique()))

# Se o município não for "Todos", filtre os bairros
if filtro_municipio != "Todos":
    filtro_bairro = st.sidebar.selectbox('Selecione o Bairro', ["Todos"] + list(df[df['MUNICÍPIO'] == filtro_municipio]['BAIRRO'].unique()))
else:
    filtro_bairro = "Todos"

# Acesse a coluna 'PREÇO DE REVENDA' e converta para tipo numérico
df['PREÇO DE REVENDA'] = pd.to_numeric(df['PREÇO DE REVENDA'], errors='coerce')

# Filtra o DataFrame com base nos filtros selecionados
filtro = (
    (df['ESTADO'] == filtro_estado) if filtro_estado != "Todos" else True) & (
    (df['PRODUTO'] == filtro_produto) if filtro_produto != "Todos" else True)

if filtro_municipio != "Todos":
    filtro &= (df['MUNICÍPIO'] == filtro_municipio)

filtro &= (
    (df['BANDEIRA'] == filtro_bandeira) if filtro_bandeira != "Todos" else True) & (
    (df['BAIRRO'] == filtro_bairro) if filtro_bairro != "Todos" else True)

# Garante que o DataFrame seja filtrado apenas se houver condições de filtro
if isinstance(filtro, pd.Series) and filtro.any():
    df_filtrado = df[filtro]
else:
    df_filtrado = df.copy()

# Encontre o maior e o menor preço com base no filtro de produto
maior_preco_produto = df_filtrado['PREÇO DE REVENDA'].max()
menor_preco_produto = df_filtrado['PREÇO DE REVENDA'].min()

# Exiba os resultados em um card
st.title("⛽🥗Análise de Preços Semanais ANP Combustiveis/GLP")

st.title("Resumo de Preços")
st.write(f'🥲Maior Preço ({filtro_produto}): R$ {maior_preco_produto:.2f}')
st.write(f'😁Menor Preço ({filtro_produto}): R$ {menor_preco_produto:.2f}')

# Filtra o DataFrame para mostrar as informações completas da entrada com o maior preço do produto selecionado
info_maior_preco_produto = df_filtrado[df_filtrado['PREÇO DE REVENDA'] == maior_preco_produto]
st.title(f"🥲Informações da Entrada com Maior Preço ({filtro_produto})")
st.write(info_maior_preco_produto)

# Filtra o DataFrame para mostrar as informações completas da entrada com o menor preço do produto selecionado
info_menor_preco_produto = df_filtrado[df_filtrado['PREÇO DE REVENDA'] == menor_preco_produto]
st.title(f"😁Informações da Entrada com Menor Preço ({filtro_produto})")
st.write(info_menor_preco_produto)

# Calcule a média para os dados filtrados
media_filtrada = df_filtrado['PREÇO DE REVENDA'].mean()

# Exiba a média
st.title("Média de Preço")
st.write(f'Média: R$ {media_filtrada:.2f}')

# Exiba os dados filtrados
st.title("Detalhes do Filtro")
st.write(df_filtrado)
