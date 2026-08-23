import streamlit as st

def apply_custom_styles(theme_mode: str = "dark"):
    """
    Aplica estilo visual temático de RPG com suporte completo a Modo Escuro (Grimório)
    e Modo Claro (Pergaminho Arcano), garantindo placeholders 100% nítidos, brilhantes e legíveis.
    """
    is_light = (theme_mode == "light")

    if is_light:
        custom_css = """
        <style>
        /* ==========================================
           MODO CLARO (PERGAMINHO ARCANO)
           ========================================== */
        :root {
            --app-bg: #f7f4ec;
            --sidebar-bg: #ece5d6;
            --primary-gold: #8a5d14;
            --bright-gold: #6b3f02;
            --text-main: #1c1813;
            --text-muted: #4e4436;
            --border-color: #cfc1a5;
            
            --pill-bg: linear-gradient(135deg, #ffffff 0%, #f4ede1 100%);
            --pill-border: #cfc1a5;
            --pill-name: #1c1813;
            --pill-role: #8a5d14;
            
            --chat-msg-bg: #ffffff;
            --chat-msg-border: #ded3bc;
            
            --btn-bg: linear-gradient(180deg, #ffffff 0%, #eee6d6 100%);
            --btn-border: #c9b999;
            --btn-text: #1c1813;
            --btn-hover-bg: linear-gradient(180deg, #faf7f0 0%, #e4d8c2 100%);
            
            --input-bg: #ffffff;
            --input-border: #c4b595;
            --input-text: #1c1813;
            
            --scrollbar-thumb: #c4b595;
        }

        .stApp {
            background-color: var(--app-bg) !important;
            color: #1c1813 !important;
        }

        /* Top Header e Bottom Toolbar do Streamlit */
        header[data-testid="stHeader"], .stAppHeader {
            background-color: var(--app-bg) !important;
            color: #1c1813 !important;
        }

        header[data-testid="stHeader"] * {
            color: #1c1813 !important;
        }

        [data-testid="stDecoration"] {
            background-image: linear-gradient(90deg, #cfc1a5, #8a5d14, #cfc1a5) !important;
        }

        [data-testid="stBottom"], [data-testid="stBottomBlockContainer"], footer {
            background-color: var(--app-bg) !important;
            color: #4e4436 !important;
        }

        /* Barra lateral */
        section[data-testid="stSidebar"] {
            background-color: var(--sidebar-bg) !important;
            border-right: 1px solid var(--border-color) !important;
        }

        /* Tipografia de Alta Legibilidade */
        h1, h2, h3, h4, h5, h6 {
            color: #6b3f02 !important;
            font-family: 'Cinzel', 'Georgia', serif;
            font-weight: 700;
        }

        p, span, li, label, [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] span, [data-testid="stMarkdownContainer"] li {
            color: #1c1813 !important;
        }

        strong, b {
            color: #0d0a07 !important;
            font-weight: 700;
        }

        .stCaption, [data-testid="stCaptionContainer"], small {
            color: #4e4436 !important;
        }

        /* Balões de Chat */
        .stChatMessage {
            background-color: #ffffff !important;
            border: 1px solid #ded3bc !important;
            border-radius: 8px;
            margin-bottom: 12px;
            color: #1c1813 !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.04);
        }

        /* Chat Input e Todos os seus Wrappers BaseWeb */
        div[data-testid="stChatInput"],
        div[data-testid="stChatInput"] > div,
        div[data-testid="stChatInput"] [data-baseweb="base-input"],
        div[data-testid="stChatInput"] [data-baseweb="textarea"],
        div[data-testid="stChatFloatingInputContainer"],
        .stChatFloatingInputContainer {
            background-color: #ffffff !important;
            background: #ffffff !important;
            border-color: #c4b595 !important;
        }

        div[data-testid="stChatInput"] textarea {
            background-color: #ffffff !important;
            color: #1c1813 !important;
            border: 1px solid #c4b595 !important;
            border-radius: 8px !important;
            font-size: 0.95rem !important;
        }

        div[data-testid="stChatInput"] button {
            color: #8a5d14 !important;
        }

        /* Placeholders Nítidos no Modo Claro */
        ::placeholder,
        ::-webkit-input-placeholder,
        :-moz-placeholder,
        ::-moz-placeholder,
        :-ms-input-placeholder,
        textarea::placeholder,
        input::placeholder,
        div[data-testid="stChatInput"] textarea::placeholder,
        div[data-testid="stChatInput"] textarea::-webkit-input-placeholder,
        div[data-baseweb="textarea"] textarea::placeholder,
        div[data-baseweb="base-input"] input::placeholder {
            color: #2b241a !important;
            -webkit-text-fill-color: #2b241a !important;
            opacity: 0.85 !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
        }

        /* Tabelas */
        table {
            border-collapse: collapse !important;
            width: 100% !important;
            margin: 10px 0 !important;
            color: #1c1813 !important;
        }

        table th {
            background-color: #ebd8b8 !important;
            color: #1c1813 !important;
            border: 1px solid #cfc1a5 !important;
            padding: 8px !important;
            font-weight: bold !important;
        }

        table td {
            background-color: #ffffff !important;
            color: #1c1813 !important;
            border: 1px solid #ded3bc !important;
            padding: 8px !important;
        }

        /* Blocos de Código */
        pre, code {
            background-color: #ede5d5 !important;
            color: #7c2223 !important;
            border: 1px solid #cfc1a5 !important;
            border-radius: 4px;
        }

        /* Caixas de Texto, Inputs e Dropdowns */
        input, textarea, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
            background-color: #ffffff !important;
            color: #1c1813 !important;
            border: 1px solid #c4b595 !important;
        }

        [data-baseweb="select"] * {
            color: #1c1813 !important;
        }

        /* Expansores / Conversas de Regras */
        div[data-testid="stExpander"] details,
        .streamlit-expanderContent {
            background-color: #f2ece0 !important;
            border: 1px solid #cfc1a5 !important;
            border-radius: 6px !important;
        }

        div[data-testid="stExpander"] summary {
            background-color: #eee6d6 !important;
            color: #6b3f02 !important;
            font-weight: 700 !important;
            border-radius: 6px !important;
            padding: 6px 10px !important;
        }

        /* Botões Normais */
        .stButton > button {
            background: linear-gradient(180deg, #ffffff 0%, #eee6d6 100%) !important;
            color: #1c1813 !important;
            border: 1px solid #c9b999 !important;
            border-radius: 6px;
            font-weight: 600;
        }

        .stButton > button:hover {
            background: linear-gradient(180deg, #faf7f0 0%, #e4d8c2 100%) !important;
            border-color: #8a5d14 !important;
            box-shadow: 0 0 8px rgba(138, 93, 20, 0.3) !important;
        }

        /* Botões Primários e Botões Ativos no Histórico */
        .stButton > button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"],
        div[data-testid="stFormSubmitButton"] button,
        .stFormSubmitButton > button {
            background: linear-gradient(180deg, #a36f1c 0%, #7c500c 100%) !important;
            color: #ffffff !important;
            border: 1px solid #5a3804 !important;
            font-weight: 700 !important;
            box-shadow: 0 2px 6px rgba(138, 93, 20, 0.25) !important;
        }

        .stButton > button[kind="primary"]:hover,
        .stButton > button[data-testid="baseButton-primary"]:hover,
        div[data-testid="stFormSubmitButton"] button:hover,
        .stFormSubmitButton > button:hover {
            background: linear-gradient(180deg, #b87e22 0%, #8f5c10 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 0 10px rgba(138, 93, 20, 0.4) !important;
        }

        /* Cabeçalho e Badge */
        .app-header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid #cfc1a5;
        }

        .app-header-title {
            margin: 0 !important;
            font-size: 1.75rem !important;
            color: #6b3f02 !important;
            font-family: 'Cinzel', 'Georgia', serif;
            font-weight: 700;
        }

        .app-header-subtitle {
            margin: 4px 0 0 0 !important;
            font-size: 0.88rem !important;
            color: #4e4436 !important;
            font-style: italic;
        }

        .user-profile-pill {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: linear-gradient(135deg, #ffffff 0%, #f4ede1 100%);
            border: 1px solid #cfc1a5;
            border-radius: 24px;
            padding: 6px 16px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
        }

        .user-profile-name {
            font-weight: 700;
            color: #1c1813;
            font-size: 0.88rem;
        }

        .user-profile-role {
            font-size: 0.75rem;
            font-weight: 600;
            color: #8a5d14;
        }
        </style>
        """
    else:
        custom_css = """
        <style>
        /* ==========================================
           MODO ESCURO (GRIMÓRIO SOMBRIO)
           ========================================== */
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

        .stApp {
            background-color: var(--app-bg) !important;
            color: #e8e3d9 !important;
        }

        /* Top Header e Bottom Toolbar do Streamlit */
        header[data-testid="stHeader"], .stAppHeader {
            background-color: var(--app-bg) !important;
            color: #e8e3d9 !important;
        }

        header[data-testid="stHeader"] * {
            color: #e8e3d9 !important;
        }

        [data-testid="stDecoration"] {
            background-image: linear-gradient(90deg, #3d3424, #c99a4e, #3d3424) !important;
        }

        [data-testid="stBottom"], [data-testid="stBottomBlockContainer"], footer {
            background-color: var(--app-bg) !important;
            color: #a09a8f !important;
        }

        /* Barra lateral */
        section[data-testid="stSidebar"] {
            background-color: var(--sidebar-bg) !important;
            border-right: 1px solid var(--border-color) !important;
        }

        /* Tipografia */
        h1, h2, h3, h4, h5, h6 {
            color: var(--bright-gold) !important;
            font-family: 'Cinzel', 'Georgia', serif;
            font-weight: 700;
        }

        p, span, li, label, [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] span, [data-testid="stMarkdownContainer"] li {
            color: #e8e3d9 !important;
        }

        strong, b {
            color: #ffffff !important;
            font-weight: 700;
        }

        .stCaption, [data-testid="stCaptionContainer"], small {
            color: #a09a8f !important;
        }

        /* Balões de Chat */
        .stChatMessage {
            background-color: #171b22 !important;
            border: 1px solid #2d3442 !important;
            border-radius: 8px;
            margin-bottom: 12px;
            color: #e8e3d9 !important;
        }

        /* Chat Input e Todos os seus Wrappers BaseWeb */
        div[data-testid="stChatInput"],
        div[data-testid="stChatInput"] > div,
        div[data-testid="stChatInput"] [data-baseweb="base-input"],
        div[data-testid="stChatInput"] [data-baseweb="textarea"],
        div[data-testid="stChatFloatingInputContainer"],
        .stChatFloatingInputContainer {
            background-color: #1a1e27 !important;
            background: #1a1e27 !important;
            border-color: #3d3424 !important;
        }

        div[data-testid="stChatInput"] textarea {
            background-color: #1a1e27 !important;
            color: #ffffff !important;
            border: 1px solid #3d3424 !important;
            border-radius: 8px !important;
            font-size: 0.95rem !important;
        }

        div[data-testid="stChatInput"] button {
            color: #e5b967 !important;
        }

        /* Placeholders Nítidos e de Alto Contraste no Modo Escuro */
        ::placeholder,
        ::-webkit-input-placeholder,
        :-moz-placeholder,
        ::-moz-placeholder,
        :-ms-input-placeholder,
        textarea::placeholder,
        input::placeholder,
        div[data-testid="stChatInput"] textarea::placeholder,
        div[data-testid="stChatInput"] textarea::-webkit-input-placeholder,
        div[data-baseweb="textarea"] textarea::placeholder,
        div[data-baseweb="base-input"] input::placeholder {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            opacity: 0.9 !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
        }

        /* Tabelas */
        table {
            border-collapse: collapse !important;
            width: 100% !important;
            margin: 10px 0 !important;
            color: #e8e3d9 !important;
        }

        table th {
            background-color: #222834 !important;
            color: #e5b967 !important;
            border: 1px solid #3d3424 !important;
            padding: 8px !important;
            font-weight: bold !important;
        }

        table td {
            background-color: #171b22 !important;
            color: #e8e3d9 !important;
            border: 1px solid #2d3442 !important;
            padding: 8px !important;
        }

        /* Blocos de Código */
        pre, code {
            background-color: #12151b !important;
            color: #f38d8e !important;
            border: 1px solid #3d3424 !important;
            border-radius: 4px;
        }

        /* Caixas de Texto, Inputs e Dropdowns */
        input, textarea, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
            background-color: #1a1e27 !important;
            color: #f1ebd9 !important;
            border: 1px solid #3d3424 !important;
        }

        /* Expansores / Conversas de Regras */
        div[data-testid="stExpander"] details,
        .streamlit-expanderContent {
            background-color: #161a22 !important;
            border: 1px solid #3d3424 !important;
            border-radius: 6px !important;
        }

        div[data-testid="stExpander"] summary {
            background-color: #1c212b !important;
            color: #e5b967 !important;
            font-weight: 700 !important;
            border-radius: 6px !important;
            padding: 6px 10px !important;
        }

        /* Botões Normais */
        .stButton > button {
            background: linear-gradient(180deg, #282f3c 0%, #191e27 100%) !important;
            color: #f1ebd9 !important;
            border: 1px solid #3d3424 !important;
            border-radius: 6px;
            font-weight: 600;
        }

        .stButton > button:hover {
            background: linear-gradient(180deg, #374154 0%, #232a36 100%) !important;
            border-color: #e5b967 !important;
            box-shadow: 0 0 8px rgba(229, 185, 103, 0.3) !important;
        }

        /* Botões Primários e Botões Ativos no Histórico */
        .stButton > button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"],
        div[data-testid="stFormSubmitButton"] button,
        .stFormSubmitButton > button {
            background: linear-gradient(180deg, #c99a4e 0%, #a8792c 100%) !important;
            color: #1a1408 !important;
            border: 1px solid #7c581d !important;
            font-weight: 700 !important;
            box-shadow: 0 2px 8px rgba(201, 154, 78, 0.3) !important;
        }

        .stButton > button[kind="primary"]:hover,
        .stButton > button[data-testid="baseButton-primary"]:hover,
        div[data-testid="stFormSubmitButton"] button:hover,
        .stFormSubmitButton > button:hover {
            background: linear-gradient(180deg, #dfb15b 0%, #bd8c36 100%) !important;
            color: #000000 !important;
            box-shadow: 0 0 12px rgba(229, 185, 103, 0.5) !important;
        }

        /* Cabeçalho e Badge */
        .app-header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid #3d3424;
        }

        .app-header-title {
            margin: 0 !important;
            font-size: 1.75rem !important;
            color: #e5b967 !important;
            font-family: 'Cinzel', 'Georgia', serif;
            font-weight: 700;
        }

        .app-header-subtitle {
            margin: 4px 0 0 0 !important;
            font-size: 0.88rem !important;
            color: #a09a8f !important;
            font-style: italic;
        }

        .user-profile-pill {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: linear-gradient(135deg, #1b202a 0%, #12151b 100%);
            border: 1px solid #3d3424;
            border-radius: 24px;
            padding: 6px 16px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
        }

        .user-profile-name {
            font-weight: 700;
            color: #f5f0e1;
            font-size: 0.88rem;
        }

        .user-profile-role {
            font-size: 0.75rem;
            font-weight: 600;
            color: #e5b967;
        }
        </style>
        """

    # Responsividade e Scrollbar
    common_css = """
    <style>
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

    st.markdown(custom_css + common_css, unsafe_allow_html=True)
