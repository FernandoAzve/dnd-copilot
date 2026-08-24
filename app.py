import streamlit as st
import os
import sys

# Garantir que o diretório raiz esteja no PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agent.gemini_agent import DnDAgent
from src.ui.styles import apply_custom_styles
from src.ui.components import render_sidebar, render_chat_message
from src.ui.sheet_view import render_sheet_auditor_tab
from src.ui.character_view import render_character_management_tab
from src.auth.auth_ui import render_auth_page
from src.auth.security import validate_session_token
from src.auth.user_manager import get_user_profile
from src.storage.chat_storage import (
    create_session,
    save_session,
    load_session,
    list_sessions
)
from src.storage.character_storage import (
    get_active_character_id,
    get_character,
    format_character_context
)

# Configuração da Página
st.set_page_config(
    page_title="Grimório do Mestre | Agente D&D 5e & 2024",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gerenciamento de Tema (Modo Claro vs Modo Escuro)
theme_param = st.query_params.get("theme")
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = theme_param if theme_param in ["light", "dark"] else "dark"
theme_mode = st.session_state["theme_mode"]

# Aplicar estilos visuais customizados
apply_custom_styles(theme_mode)

# 1. VERIFICAÇÃO DE AUTENTICAÇÃO COM PERSISTÊNCIA (AUTH GATE + SESSION TOKEN)
if "authenticated_user" not in st.session_state or not st.session_state["authenticated_user"]:
    token = st.query_params.get("session_token")
    if token:
        valid_user = validate_session_token(token)
        if valid_user:
            profile = get_user_profile(valid_user)
            if profile:
                st.session_state["authenticated_user"] = profile

if "authenticated_user" not in st.session_state or not st.session_state["authenticated_user"]:
    render_auth_page()
    st.stop()

user_data = st.session_state["authenticated_user"]
username = user_data["username"]
user_api_key = user_data.get("gemini_api_key", "")

# 2. INICIALIZAÇÃO DO ESTADO DA SESSÃO E AGENTE DO USUÁRIO
if "agent" not in st.session_state:
    st.session_state.agent = DnDAgent(api_key=user_api_key)
elif user_api_key and st.session_state.agent.api_key != user_api_key:
    st.session_state.agent.update_config(api_key=user_api_key)

if "main_view" not in st.session_state:
    st.session_state["main_view"] = "chat"

if "current_session_id" not in st.session_state or not st.session_state["current_session_id"]:
    existing_sessions = list_sessions(username=username)
    if existing_sessions:
        latest_id = existing_sessions[0]["id"]
        st.session_state["current_session_id"] = latest_id
        session_data = load_session(latest_id, username=username)
        st.session_state.messages = session_data.get("messages", []) if session_data else []
    else:
        new_id = create_session(mode=st.session_state.agent.mode, model=st.session_state.agent.model_name, username=username)
        st.session_state["current_session_id"] = new_id
        st.session_state.messages = load_session(new_id, username=username)["messages"]

if "messages" not in st.session_state or not st.session_state.messages:
    session_data = load_session(st.session_state["current_session_id"], username=username)
    if session_data:
        st.session_state.messages = session_data.get("messages", [])
    else:
        st.session_state.messages = [
            {
                "role": "model",
                "content": (
                    f"⚔️ **Saudações, {user_data.get('name', username)}! Eu sou o Sábio do Grimório.**\n\n"
                    "Estou aqui para tirar qualquer dúvida sobre as regras de **D&D 5ª Edição e a nova revisão de 2024**, "
                    "explicar magias, habilidades de classes, ajudar na montagem de ficha e rolar dados para a sua mesa.\n\n"
                    "Como posso ajudar você hoje?"
                ),
                "tool_logs": []
            }
        ]

# 3. RENDERIZAR BARRA LATERAL COM DADOS DO USUÁRIO E PERMISSÕES RBAC
render_sidebar(st.session_state.agent, user_data=user_data)

# 4. CABEÇALHO PRINCIPAL TEMÁTICO E RESPONSIVO
is_admin = user_data.get("is_admin", False)
badge_label = "👑 Mestre Administrador" if is_admin else "⚔️ Jogador"
display_name = user_data.get("name") or username

st.markdown(
    f"""
    <div class="app-header-container">
        <div class="app-header-titles">
            <h1 class="app-header-title">🐉 Grimório do Mestre & Mentor D&D</h1>
            <p class="app-header-subtitle">Seu assistente inteligente de regras, combate, auditoria de fichas e aprendizado</p>
        </div>
        <div class="user-profile-pill">
            <div class="user-profile-avatar">👤</div>
            <div class="user-profile-info">
                <span class="user-profile-name">{display_name}</span>
                <span class="user-profile-role">{badge_label}</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Alerta caso o usuário ainda não tenha configurado sua chave Gemini
if not st.session_state.agent.api_key:
    st.warning(
        "⚠️ **Chave de API do Gemini não configurada para sua conta.**\n\n"
        "Para ativar as respostas completas da IA e a visão computacional de fichas, adicione sua chave gratuita na barra lateral esquerda (menu **'Minha Chave Gemini'**)."
    )

# 5. VISUALIZAÇÕES
if st.session_state["main_view"] == "chat":
    # Sugestões Rápidas de Perguntas (Grid 2x2 Responsivo)
    st.markdown("**Perguntas Frequentes & Exemplos Rápidos:**")
    col_chip1, col_chip2 = st.columns(2)
    with col_chip1:
        if st.button("💬 Como calculo o bônus de ataque do meu personagem?", key="chip_0", use_container_width=True):
            st.session_state["pending_prompt"] = "Como calculo o bônus de ataque do meu personagem?"
        if st.button("💬 O que mudou em Poção de Cura em 2024?", key="chip_2", use_container_width=True):
            st.session_state["pending_prompt"] = "O que mudou em Poção de Cura em 2024?"
    with col_chip2:
        if st.button("💬 Como funciona a magia Bola de Fogo?", key="chip_1", use_container_width=True):
            st.session_state["pending_prompt"] = "Como funciona a magia Bola de Fogo?"
        if st.button("💬 Como funciona a Concentração ao tomar dano?", key="chip_3", use_container_width=True):
            st.session_state["pending_prompt"] = "Como funciona a Concentração ao tomar dano?"

    # Renderizar Histórico de Mensagens da Sessão Ativa
    for msg in st.session_state.messages:
        render_chat_message(
            role=msg["role"],
            content=msg["content"],
            tool_logs=msg.get("tool_logs", [])
        )

    # Capturar Entrada do Usuário
    user_query = st.chat_input("Pergunte uma regra, magia, rolagem de dados ou conceito de D&D...", key="main_chat_input")
    if "pending_prompt" in st.session_state and st.session_state["pending_prompt"]:
        user_query = st.session_state["pending_prompt"]
        st.session_state["pending_prompt"] = None

    if user_query:
        # 1. Adicionar mensagem do usuário e renderizar na tela
        st.session_state.messages.append({"role": "user", "content": user_query})
        render_chat_message("user", user_query)

        # 2. Obter contexto do personagem ativo (se houver)
        act_id = get_active_character_id(username)
        act_char = get_character(act_id, username) if act_id else None
        char_context = format_character_context(act_char) if act_char else ""

        # 3. Obter resposta do agente com STREAMING em tempo real e contexto do personagem
        with st.chat_message("model", avatar="🧙‍♂️"):
            stream_gen = st.session_state.agent.stream_query(user_query, character_context=char_context)
            bot_text = st.write_stream(stream_gen)

        # 4. Adicionar mensagem completa do agente ao histórico em memória
        st.session_state.messages.append({
            "role": "model",
            "content": bot_text,
            "tool_logs": []
        })
        
        # 5. Salvar permanentemente no diretório privado do usuário
        save_session(
            session_id=st.session_state["current_session_id"],
            messages=st.session_state.messages,
            mode=st.session_state.agent.mode,
            model=st.session_state.agent.model_name,
            username=username
        )
        st.rerun()

elif st.session_state["main_view"] == "characters":
    # Módulo Central de Heróis do Jogador
    render_character_management_tab(st.session_state.agent, username=username)

else:
    # Auditor de Fichas com histórico isolado por usuário
    render_sheet_auditor_tab(st.session_state.agent, username=username)
