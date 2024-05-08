import streamlit as st
import pandas as pd
from eventbrite_api import verificar_usuario, obter_id_organizacao, obter_resumo_eventos, obter_ids_eventos, obter_todos_participantes

# Authentication and setup
token = 'KA5CJABXFH733E2TDWYI'
org_id = obter_id_organizacao(token)

# Sidebar for User Information
st.sidebar.header('Eventbrite Dashboard')
usuario_info = verificar_usuario(token)
if isinstance(usuario_info, tuple):
    st.sidebar.error('Error: Could not fetch user data.')
else:
    st.sidebar.subheader(f"User: {usuario_info['name']}")

# Main Page Layout
st.title('Eventbrite Event Dashboard')

# Display event summary
eventos_df = obter_resumo_eventos(token, org_id)
if not isinstance(eventos_df, pd.DataFrame):
    st.error('Failed to load event data.')
else:
    st.subheader('Event Summary')
    st.dataframe(eventos_df[['Nome', 'Data de Início', 'Data de Término', 'Capacidade', 'Status']])

# Interactive selection of events to view participants
eventos_dict = obter_ids_eventos(token, org_id)
evento_selecionado = st.selectbox('Select an Event:', list(eventos_dict.keys()))

# Display participants for the selected event
if evento_selecionado:
    participantes_df = obter_todos_participantes(token, {evento_selecionado: eventos_dict[evento_selecionado]})
    if participantes_df.empty:
        st.error('No participants found or error in fetching data.')
    else:
        st.subheader(f"Participants for {evento_selecionado}")
        st.dataframe(participantes_df)

# Run the Streamlit application by executing the script normally.
