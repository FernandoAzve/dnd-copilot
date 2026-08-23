import streamlit as st

def apply_custom_styles():
    """Aplica estilo visual temático de RPG / Grimório de Fantasia à aplicação Streamlit."""
    custom_css = """
    <style>
    /* Estilo Geral e Paleta de Cores D&D */
    :root {
        --primary-gold: #c99a4e;
        --dark-gold: #8c6a2e;
        --bg-dark: #121418;
        --panel-dark: #1b1f27;
        --border-gold: #4a3e28;
        --text-light: #e8e3d9;
        --accent-red: #9e2a2b;
    }

    /* Fundo da página */
    .stApp {
        background-color: #0f1115;
        color: #e2ded4;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #161920;
        border-right: 1px solid #332b1d;
    }

    /* Título e Cabeçalhos */
    h1, h2, h3 {
        color: #dfb15b !important;
        font-family: 'Cinzel', 'Georgia', serif;
        letter-spacing: 0.5px;
    }

    /* Cartões e Caixas de Mensagem */
    .dnd-card {
        background: #1e222b;
        border: 1px solid #4a3f2b;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    .dnd-card-title {
        color: #e5b967;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 6px;
        border-bottom: 1px solid #3d3524;
        padding-bottom: 4px;
    }

    /* Botões estilizados */
    .stButton > button {
        background: linear-gradient(180deg, #2b313d 0%, #1c2027 100%);
        color: #f1ebd9;
        border: 1px solid #5a4b33;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(180deg, #3d4556 0%, #29303b 100%);
        border-color: #d4a755;
        color: #ffffff;
        box-shadow: 0 0 8px rgba(212, 167, 85, 0.4);
    }

    /* Botões de Rolagem de Dados Rápidos */
    .dice-btn-container {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
        margin-bottom: 15px;
    }

    /* Tags de Status e Destaques */
    .dnd-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-right: 6px;
    }
    .badge-2024 {
        background-color: #6b2d5c;
        color: #ffc4f5;
        border: 1px solid #aa4592;
    }
    .badge-5e {
        background-color: #264653;
        color: #e76f51;
        border: 1px solid #2a9d8f;
    }

    /* Histórico de Chat */
    .stChatMessage {
        border-radius: 10px;
        margin-bottom: 10px;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #11141a;
    }
    ::-webkit-scrollbar-thumb {
        background: #3c3426;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #c99a4e;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
