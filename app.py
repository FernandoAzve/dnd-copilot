import streamlit as st
import os
import sys

# Garantir que o diretório raiz esteja no PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agent.gemini_agent import DnDAgent
from src.ui.styles import apply_custom_styles
from src.ui.components import render_sidebar, render_chat_message
from src.ui.sheet_view import render_sheet_auditor_tab
from src.auth.auth_ui import render_auth_page
from src.storage.chat_storage import (
    create_session,
    save_session,
    load_session,
    list_sessions
)

# Configuração da Página
st.set_page_config(
    page_title="Grimório do Mestre | Agente D&D 5e & 2024",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilos visuais customizados
apply_custom_styles()

# 1. VERIFICAÇÃO DE AUTENTICAÇÃO (AUTH GATE)
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

# 4. CABEÇALHO PRINCIPAL
col_title, col_badge = st.columns([3, 1])
with col_title:
    st.markdown("# 🐉 Grimório do Mestre & Mentor D&D")
    st.markdown("##### *Seu assistente inteligente de regras, combate, auditoria de fichas e aprendizado*")
with col_badge:
    is_admin = user_data.get("is_admin", False)
    badge_label = "👑 Mestre Administrador" if is_admin else "⚔️ Jogador"
    st.info(f"**Conectado:** {user_data.get('name', username)}\n\n*{badge_label}*")

# Alerta caso o usuário ainda não tenha configurado sua chave Gemini
if not st.session_state.agent.api_key:
    st.warning(
        "⚠️ **Chave de API do Gemini não configurada para sua conta.**\n\n"
        "Para ativar as respostas completas da IA e a visão computacional de fichas, adicione sua chave gratuita na barra lateral esquerda (menu **'Minha Chave Gemini'**)."
    )

st.divider()

# 5. NAVEGAÇÃO PRINCIPAL (ESTADO SEGURO)
col_nav_main1, col_nav_main2, _ = st.columns([2, 2.5, 3.5])
with col_nav_main1:
    is_chat_view = (st.session_state["main_view"] == "chat")
    if st.button("💬 **Grimório & Chat de Regras**", key="btn_main_chat", use_container_width=True, type="primary" if is_chat_view else "secondary"):
        st.session_state["main_view"] = "chat"
        st.rerun()

with col_nav_main2:
    is_sheet_view = (st.session_state["main_view"] == "sheets")
    if st.button("📋 **Auditor de Fichas (Fotos & PDFs)**", key="btn_main_sheets", use_container_width=True, type="primary" if is_sheet_view else "secondary"):
        st.session_state["main_view"] = "sheets"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# 6. VISUALIZAÇÕES
if st.session_state["main_view"] == "chat":
    # Sugestões Rápidas de Perguntas (Chips)
    st.markdown("**Perguntas Frequentes & Exemplos Rápidos:**")
    chip_cols = st.columns(4)
    suggested_prompts = [
        "Como calculo o bônus de ataque do meu personagem?",
        "Como funciona a magia Bola de Fogo?",
        "O que mudou em Poção de Cura em 2024?",
        "Como funciona a Concentração ao tomar dano?"
    ]

    for idx, prompt_text in enumerate(suggested_prompts):
        with chip_cols[idx]:
            if st.button(f"💬 {prompt_text}", key=f"chip_{idx}", use_container_width=True):
                st.session_state["pending_prompt"] = prompt_text

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
        # 1. Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": user_query})
        render_chat_message("user", user_query)

        # 2. Obter resposta do agente com indicador de carregamento
        with st.spinner("Consultando os tomos e pergaminhos de regras..."):
            response_data = st.session_state.agent.answer_query(user_query)
            bot_text = response_data.get("text", "Não obtive resposta.")
            tool_logs = response_data.get("tool_logs", [])

        # 3. Adicionar mensagem do agente ao histórico em memória
        st.session_state.messages.append({
            "role": "model",
            "content": bot_text,
            "tool_logs": tool_logs
        })
        
        # 4. Salvar permanentemente no diretório privado do usuário
        save_session(
            session_id=st.session_state["current_session_id"],
            messages=st.session_state.messages,
            mode=st.session_state.agent.mode,
            model=st.session_state.agent.model_name,
            username=username
        )
        
        render_chat_message("model", bot_text, tool_logs)
        st.rerun()

else:
    # Auditor de Fichas com histórico isolado por usuário
    render_sheet_auditor_tab(st.session_state.agent, username=username)
