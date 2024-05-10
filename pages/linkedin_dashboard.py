import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from utils.rows_api import fetch_table_data
import streamlit.components.v1 as components  # Importando components corretamente

# Carregando variáveis de ambiente e dados
load_dotenv()
api_key = os.getenv('ROWS_API_KEY')
spreadsheet_id = '7FIZkV8hcSztF47bvxPzUw'
table_id = '1dc0bfbf-d735-4443-a00a-bfd419a06f5d'
cell_range = 'A1:Z999'
data = fetch_table_data(api_key, spreadsheet_id, table_id, cell_range)

# Convertendo coluna 'Date' para o tipo datetime
data['Date'] = pd.to_datetime(data['Date'])

# Convertendo 'Engagement rate' para float e corrigindo percentuais
data['Engagement rate'] = data['Engagement rate'].str.rstrip('%').astype(float) / 100

# Visão Geral
st.title('Dashboard de Insights do LinkedIn da Upstart')

col1, col2, col3 = st.columns(3)
with col1:
    total_impressions = data['Impressions'].sum()
    st.metric(label="Total de Impressões", value=f"{total_impressions:,}")
with col2:
    total_engagements = data[['Likes', 'Comments', 'Shares']].sum().sum()
    st.metric(label="Total de Engajamentos", value=f"{total_engagements:,}")
with col3:
    engagement_rate = total_engagements / total_impressions
    st.metric(label="Taxa de Engajamento", value=f"{engagement_rate:.2%}")

# Gráfico de Linhas para Impressões e Engajamentos Totais
st.subheader('Tendências de Impressões e Engajamentos Totais')
engagement_cols = ['Impressions', 'Likes', 'Comments', 'Shares']
data['Total Engagements'] = data[engagement_cols[1:]].sum(axis=1)  # Sum de Likes, Comments, Shares

# Plotando Impressões e Total Engagements
line_chart_data = data.set_index('Date')[['Impressions', 'Total Engagements']]
st.line_chart(line_chart_data)

# Gráfico de Linhas para Engajamento Detalhado
st.subheader('Detalhes de Engajamento ao Longo do Tempo')
detailed_engagement_data = data.set_index('Date')[engagement_cols[1:]]  # Likes, Comments, Shares
st.line_chart(detailed_engagement_data)

# Elementos interativos e filtros
st.sidebar.header("Filtros de Data")
start_date, end_date = st.sidebar.date_input(
    "Selecionar Intervalo de Data",
    value=(data['Date'].min(), data['Date'].max()),
    min_value=data['Date'].min(),
    max_value=data['Date'].max()
)

filtered_data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]

if not filtered_data.empty:
    st.subheader("Dados Filtrados por Data")
    st.write(filtered_data)


# Mostrar dados brutos
if st.checkbox('Mostrar Dados Brutos'):
    st.write(data)

