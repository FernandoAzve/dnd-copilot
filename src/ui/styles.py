import streamlit as st

def apply_custom_styles():
    """Aplica estilo visual temático de RPG / Grimório de Fantasia responsivo para Desktop, Tablet e Celular."""
    custom_css = """
    <style>
    /* 1. Estilo Geral e Paleta de Cores D&D */
    :root {
        --primary-gold: #c99a4e;
        --bright-gold: #e5b967;
        --dark-gold: #8c6a2e;
        --bg-dark: #0f1115;
        --panel-dark: #1b1f27;
        --border-gold: #3d3424;
        --text-light: #e8e3d9;
        --text-muted: #a09a8f;
        --accent-red: #9e2a2b;
    }

    /* Fundo da página */
    .stApp {
        background-color: var(--bg-dark);
        color: var(--text-light);
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }

    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #14171d;
        border-right: 1px solid var(--border-gold);
    }

    /* Títulos e Tipografia */
    h1, h2, h3 {
        color: var(--bright-gold) !important;
        font-family: 'Cinzel', 'Georgia', serif;
        letter-spacing: 0.5px;
    }

    /* 2. Cabeçalho Principal Responsivo com Container Flexbox */
    .app-header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border-gold);
    }

    .app-header-titles {
        flex: 1 1 300px;
    }

    .app-header-title {
        margin: 0 !important;
        font-size: 1.75rem !important;
        color: var(--bright-gold) !important;
        font-family: 'Cinzel', 'Georgia', serif;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .app-header-subtitle {
        margin: 4px 0 0 0 !important;
        font-size: 0.88rem !important;
        color: var(--text-muted) !important;
        font-style: italic;
    }

    /* 3. Badge / Pill de Usuário Temático */
    .user-profile-pill {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: linear-gradient(135deg, #1b202a 0%, #12151b 100%);
        border: 1px solid var(--border-gold);
        border-radius: 24px;
        padding: 6px 16px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
        transition: all 0.2s ease;
    }

    .user-profile-pill:hover {
        border-color: var(--bright-gold);
        box-shadow: 0 0 12px rgba(212, 167, 85, 0.25);
    }

    .user-profile-avatar {
        font-size: 1.3rem;
        line-height: 1;
    }

    .user-profile-info {
        display: flex;
        flex-direction: column;
        line-height: 1.25;
    }

    .user-profile-name {
        font-weight: 700;
        color: #f5f0e1;
        font-size: 0.88rem;
    }

    .user-profile-role {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--bright-gold);
    }

    /* 4. Botões Estilizados e Touch-Friendly */
    .stButton > button {
        background: linear-gradient(180deg, #282f3c 0%, #191e27 100%);
        color: #f1ebd9;
        border: 1px solid var(--border-gold);
        border-radius: 6px;
        font-weight: 600;
        min-height: 38px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(180deg, #374154 0%, #232a36 100%);
        border-color: var(--bright-gold);
        color: #ffffff;
        box-shadow: 0 0 8px rgba(212, 167, 85, 0.35);
    }

    /* 5. Cartões de Conteúdo e Chat */
    .stChatMessage {
        background: #171b22 !important;
        border: 1px solid #2d3442 !important;
        border-radius: 8px;
        margin-bottom: 12px;
    }

    /* 6. RESPONSIVIDADE (MEDIA QUERIES) */
    
    /* Tablets (Max-width: 992px) */
    @media (max-width: 992px) {
        .app-header-title {
            font-size: 1.45rem !important;
        }
        .user-profile-pill {
            padding: 5px 12px;
        }
        .user-profile-name {
            font-size: 0.82rem;
        }
    }

    /* Celulares / Telas Pequenas (Max-width: 640px) */
    @media (max-width: 640px) {
        .app-header-container {
            flex-direction: column;
            align-items: stretch;
            gap: 10px;
        }
        .app-header-title {
            font-size: 1.25rem !important;
        }
        .app-header-subtitle {
            font-size: 0.78rem !important;
        }
        .user-profile-pill {
            width: 100%;
            justify-content: flex-start;
            border-radius: 8px;
        }
        .stButton > button {
            min-height: 42px; /* Área de toque confortável no celular */
        }
        .stChatMessage {
            padding: 8px !important;
            font-size: 0.9rem;
        }
        /* Tabelas com scroll horizontal suave no celular */
        table {
            display: block;
            max-width: 100%;
            overflow-x: auto;
            white-space: nowrap;
        }
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 7px;
        height: 7px;
    }
    ::-webkit-scrollbar-track {
        background: #0f1115;
    }
    ::-webkit-scrollbar-thumb {
        background: #342d20;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--bright-gold);
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
