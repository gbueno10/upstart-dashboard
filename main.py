import streamlit as st

# Import das páginas
from pages import eventbrite_dashboard, community_dashboard

# Configuração da barra lateral para seleção de página
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Eventbrite Dashboard', 'Community Dashboard'])

# Direcionamento para a página selecionada
if page == 'Eventbrite Dashboard':
    eventbrite_dashboard.show()
elif page == 'Community Dashboard':
    community_dashboard.show()
