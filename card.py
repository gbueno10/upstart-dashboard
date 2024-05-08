import streamlit as st

# Dados de exemplo, que você provavelmente obteria de uma API ou banco de dados
user_data = {
    "name": "upstart-bot",
    "id": "1149361057245188136",
    "discriminator": "1420",
    "avatar_url": None,
    "nickname": None,
    "joined_at": "2023-09-07 15:34:41.376000+00:00",
    "roles": ["@everyone", "upstart-bot", "ADM"],
    "status": "offline",
    "activity": None
}

def render_user_card(user):
    """Renderiza um card de usuário com informações do Discord."""
    roles = ', '.join(user['roles'])  # Converte lista de roles para string
    avatar_url = user['avatar_url'] or "URL_to_default_avatar"
    st.markdown(f"""
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

st.title("User Profile Card")
render_user_card(user_data)
