import streamlit as st
import os
import sys

# Garantir que o diretório raiz esteja no PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agent.gemini_agent import DnDAgent
from src.ui.styles import apply_custom_styles
from src.ui.components import render_sidebar, render_chat_message
from src.ui.sheet_view import render_sheet_auditor_tab
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

# Inicialização do Estado da Sessão e Agente
if "agent" not in st.session_state:
    st.session_state.agent = DnDAgent()

if "main_view" not in st.session_state:
    st.session_state["main_view"] = "chat"

if "current_session_id" not in st.session_state:
    existing_sessions = list_sessions()
    if existing_sessions:
        latest_id = existing_sessions[0]["id"]
        st.session_state["current_session_id"] = latest_id
        session_data = load_session(latest_id)
        st.session_state.messages = session_data.get("messages", []) if session_data else []
    else:
        new_id = create_session(mode=st.session_state.agent.mode, model=st.session_state.agent.model_name)
        st.session_state["current_session_id"] = new_id
        st.session_state.messages = load_session(new_id)["messages"]

if "messages" not in st.session_state or not st.session_state.messages:
    session_data = load_session(st.session_state["current_session_id"])
    if session_data:
        st.session_state.messages = session_data.get("messages", [])
    else:
        st.session_state.messages = [
            {
                "role": "model",
                "content": (
                    "⚔️ **Saudações, aventureiro! Eu sou o Sábio do Grimório.**\n\n"
                    "Estou aqui para tirar qualquer dúvida sobre as regras de **D&D 5ª Edição e a nova revisão de 2024**, "
                    "explicar magias, habilidades de classes, ajudar na montagem de ficha e rolar dados para a sua mesa.\n\n"
                    "Como posso ajudar você hoje?"
                ),
                "tool_logs": []
            }
        ]

# Renderizar Barra Lateral
render_sidebar(st.session_state.agent)

# Cabeçalho Principal
col_title, col_badge = st.columns([3, 1])
with col_title:
    st.markdown("# 🐉 Grimório do Mestre & Mentor D&D")
    st.markdown("##### *Seu assistente inteligente de regras, combate, auditoria de fichas e aprendizado*")
with col_badge:
    mode_names = {
        "mentor": "🧙‍♂️ Modo Mentor (Iniciantes)",
        "arbitro": "⚔️ Modo Árbitro (Rápido)",
        "regras_2024": "📖 Modo Regras 2024"
    }
    current_mode_label = mode_names.get(st.session_state.agent.mode, "🧙‍♂️ Modo Mentor")
    st.info(f"**Ativo:** {current_mode_label}")

st.divider()

# Navegação Principal (Botões de Estado Confiáveis)
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

# 1. VISUALIZAÇÃO: CHAT DO GRIMÓRIO
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

    # Capturar Entrada do Usuário (Único chat_input quando na aba Chat)
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
        
        # 4. Salvar permanentemente no armazenamento em disco
        save_session(
            session_id=st.session_state["current_session_id"],
            messages=st.session_state.messages,
            mode=st.session_state.agent.mode,
            model=st.session_state.agent.model_name
        )
        
        render_chat_message("model", bot_text, tool_logs)
        st.rerun()

# 2. VISUALIZAÇÃO: AUDITOR DE FICHAS
else:
    render_sheet_auditor_tab(st.session_state.agent)
