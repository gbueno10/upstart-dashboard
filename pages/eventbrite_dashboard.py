import streamlit as st
import pandas as pd
from utils.eventbrite_api import  obter_id_organizacao, obter_resumo_eventos, obter_ids_eventos, obter_todos_participantes
from dotenv import load_dotenv
import os

load_dotenv()
# Authentication and setup
token=os.getenv('TOKEN') 
print(token)
org_id = obter_id_organizacao(token)



# Main Page Layout
st.title(f'Eventbrite Event Dashboard')

# Display event summary
eventos_df = obter_resumo_eventos(token, org_id)
if not isinstance(eventos_df, pd.DataFrame):
    st.error('Failed to load event data.')
else:
    st.subheader('Event Summary')
    st.dataframe(eventos_df[['Nome', 'Data de Início', 'Data de Término', 'Capacidade', 'Status']])

# Interactive selection of events to view participants
eventos_dict = obter_ids_eventos(token, org_id)

if not eventos_dict:
    st.error("Não foi possível recuperar eventos. Verifique as configurações e permissões.")
else:
    evento_selecionado = st.selectbox('Select an Event:', list(eventos_dict.keys()))
    # Continuar com a lógica dependente do evento selecionado
# Display participants for the selected event
if evento_selecionado:
    participantes_df = obter_todos_participantes(token, {evento_selecionado: eventos_dict[evento_selecionado]})
    if participantes_df.empty:
        st.error('No participants found or error in fetching data.')
    else:
        st.subheader(f"Participants for {evento_selecionado}")
        st.dataframe(participantes_df)

# Run the Streamlit application by executing the script normally.
