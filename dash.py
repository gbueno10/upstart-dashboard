import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Função para carregar o JSON a partir do caminho do arquivo
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Função para renderizar um card de membro da comunidade
def render_user_card(user, col):
    """Renderiza um card de usuário com informações."""
    roles = ', '.join(user['roles'])  # Converte lista de roles para string
    avatar_url = user['avatar_url'] or "URL_to_default_avatar"
    col.markdown(f"""
        <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px 0;">
            <h3>{user['name']}#{user['discriminator']}</h3>
            <img src="{avatar_url}" alt="Avatar" style="height: 50px; width: 50px; border-radius: 50%;">
            <p><strong>Nickname:</strong> {user['nickname'] or 'None'}</p>
            <p><strong>Joined:</strong> {user['joined_at']}</p>
            <p><strong>Roles:</strong> {roles}</p>
            <p><strong>Status:</strong> {user['status'].capitalize()}</p>
            <p><strong>Activity:</strong> {user['activity'] or 'None'}</p>
        </div>
    """, unsafe_allow_html=True)

# Layout Principal
st.title('Comunidade')

# Carregar o JSON pelo caminho do arquivo
file_path = "user_list.json"
community_data = load_json(file_path)

# Converter datas de entrada e criar DataFrame
df = pd.DataFrame(community_data)
df['joined_at'] = pd.to_datetime(df['joined_at']).dt.date
df.sort_values('joined_at', inplace=True)
df['cumulative_count'] = range(1, len(df) + 1)

# Plotar o crescimento da comunidade
st.subheader("Crescimento da Comunidade")
fig, ax = plt.subplots()
ax.plot(df['joined_at'], df['cumulative_count'], marker='o', linestyle='-')
ax.set_xlabel("Data")
ax.set_ylabel("Número Cumulativo de Membros")
ax.set_title("Crescimento da Comunidade ao Longo do Tempo")
st.pyplot(fig)

# Filtro por roles
st.subheader("Filtrar por Papéis (Roles)")
roles = list(set(role for user in community_data for role in user['roles']))
selected_roles = st.multiselect("Selecione os Papéis (Roles)", roles, roles)

# Aplicar filtro
filtered_data = [user for user in community_data if any(role in user['roles'] for role in selected_roles)]

# Indicadores de resumo
st.subheader("Resumo dos Participantes")
total_members = len(community_data)
total_marketing = sum(1 for user in community_data if 'Marketing' in user['roles'])
total_design = sum(1 for user in community_data if 'Design' in user['roles'])
total_business = sum(1 for user in community_data if 'Business' in user['roles'])
total_tech = sum(1 for user in community_data if 'Tech' in user['roles'])

cols = st.columns(6)  # Seis colunas para os seis indicadores
cols[0].metric("Total de Membros", total_members)
cols[1].metric("Marketing", total_marketing)
cols[2].metric("Design", total_design)
cols[3].metric("Business", total_business)
cols[4].metric("Tech", total_tech)

# Renderizar cards para cada membro da comunidade em colunas
st.subheader("Membros da Comunidade")
card_cols = st.columns(3)  # Define três colunas para os cards
for idx, member in enumerate(filtered_data):
    render_user_card(member, card_cols[idx % 3])  # Distribui os cards nas colunas de forma cíclica
