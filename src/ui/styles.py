import streamlit as st

def apply_custom_styles():
    """
    Aplica estilo visual temático de RPG com suporte completo a Modo Escuro (Grimório)
    e Modo Claro (Pergaminho Arcano), garantindo contraste e legibilidade impecáveis.
    """
    custom_css = """
    <style>
    /* ==========================================================================
       1. DEFINIÇÃO DE VARIÁVEIS DE TEMA (DARK MODE PADRÃO / GRIMÓRIO)
       ========================================================================== */
    :root {
        --app-bg: #0f1115;
        --sidebar-bg: #14171d;
        --primary-gold: #c99a4e;
        --bright-gold: #e5b967;
        --text-main: #e8e3d9;
        --text-muted: #a09a8f;
        --border-color: #3d3424;
        
        --pill-bg: linear-gradient(135deg, #1b202a 0%, #12151b 100%);
        --pill-border: #3d3424;
        --pill-name: #f5f0e1;
        --pill-role: #e5b967;
        
        --chat-msg-bg: #171b22;
        --chat-msg-border: #2d3442;
        
        --btn-bg: linear-gradient(180deg, #282f3c 0%, #191e27 100%);
        --btn-border: #3d3424;
        --btn-text: #f1ebd9;
        --btn-hover-bg: linear-gradient(180deg, #374154 0%, #232a36 100%);
        
        --input-bg: #1a1e27;
        --input-border: #3d3424;
        --input-text: #f1ebd9;
        
        --scrollbar-thumb: #342d20;
    }

    /* ==========================================================================
       2. ADAPTAÇÃO PARA MODO CLARO (PERGAMINHO ARCANO)
       ========================================================================== */
    @media (prefers-color-scheme: light) {
        :root {
            --app-bg: #f8f5ee;
            --sidebar-bg: #eee8dc;
            --primary-gold: #8a5d14;
            --bright-gold: #74460a;
            --text-main: #231f18;
            --text-muted: #5e5648;
            --border-color: #cfc1a5;
            
            --pill-bg: linear-gradient(135deg, #ffffff 0%, #f4ede1 100%);
            --pill-border: #cfc1a5;
            --pill-name: #231f18;
            --pill-role: #8a5d14;
            
            --chat-msg-bg: #ffffff;
            --chat-msg-border: #ded3bc;
            
            --btn-bg: linear-gradient(180deg, #ffffff 0%, #eee6d6 100%);
            --btn-border: #c9b999;
            --btn-text: #2a241b;
            --btn-hover-bg: linear-gradient(180deg, #faf7f0 0%, #e4d8c2 100%);
            
            --input-bg: #ffffff;
            --input-border: #c9b999;
            --input-text: #231f18;
            
            --scrollbar-thumb: #c4b595;
        }
    }

    /* ==========================================================================
       3. APLICAÇÃO DOS ESTILOS GERAIS E ESTRUTURA
       ========================================================================== */
    .stApp {
        background-color: var(--app-bg) !important;
        color: var(--text-main) !important;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }

    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border-color) !important;
    }

    /* Tipografia e Títulos */
    h1, h2, h3, h4, h5, h6 {
        color: var(--bright-gold) !important;
        font-family: 'Cinzel', 'Georgia', serif;
        letter-spacing: 0.5px;
    }

    p, span, label, div {
        color: inherit;
    }

    /* ==========================================================================
       4. CABEÇALHO PRINCIPAL E BADGE DE USUÁRIO
       ========================================================================== */
    .app-header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border-color);
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

    .user-profile-pill {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: var(--pill-bg);
        border: 1px solid var(--pill-border);
        border-radius: 24px;
        padding: 6px 16px;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
        transition: all 0.2s ease;
    }

    .user-profile-pill:hover {
        border-color: var(--bright-gold);
        box-shadow: 0 0 10px rgba(201, 154, 78, 0.25);
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
        color: var(--pill-name);
        font-size: 0.88rem;
    }

    .user-profile-role {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--pill-role);
    }

    /* ==========================================================================
       5. BOTÕES E COMPONENTES INTERATIVOS
       ========================================================================== */
    .stButton > button {
        background: var(--btn-bg) !important;
        color: var(--btn-text) !important;
        border: 1px solid var(--btn-border) !important;
        border-radius: 6px;
        font-weight: 600;
        min-height: 38px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: var(--btn-hover-bg) !important;
        border-color: var(--bright-gold) !important;
        box-shadow: 0 0 8px rgba(201, 154, 78, 0.3);
    }

    /* Botão Primário (Dourado de Destaque) */
    .stButton > button[kind="primary"], .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(180deg, #c99a4e 0%, #a8792c 100%) !important;
        color: #1a1408 !important;
        border: 1px solid #7c581d !important;
        font-weight: 700;
    }

    .stButton > button[kind="primary"]:hover, .stButton > button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(180deg, #dfb15b 0%, #bd8c36 100%) !important;
        color: #000000 !important;
        box-shadow: 0 0 12px rgba(201, 154, 78, 0.5) !important;
    }

    /* Balões de Chat */
    .stChatMessage {
        background: var(--chat-msg-bg) !important;
        border: 1px solid var(--chat-msg-border) !important;
        border-radius: 8px;
        margin-bottom: 12px;
        color: var(--text-main) !important;
    }

    /* Expansores */
    .streamlit-expanderHeader {
        background-color: var(--chat-msg-bg) !important;
        border-radius: 6px !important;
        color: var(--text-main) !important;
    }

    /* ==========================================================================
       6. RESPONSIVIDADE (MEDIA QUERIES)
       ========================================================================== */
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
            min-height: 42px;
        }
        .stChatMessage {
            padding: 8px !important;
            font-size: 0.9rem;
        }
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
        background: var(--app-bg);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--scrollbar-thumb);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--bright-gold);
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
