import streamlit as st
from typing import Dict, Any, Optional
from .user_manager import (
    register_user,
    authenticate_user,
    update_user_api_key,
    count_users
)
from .security import create_session_token

def render_auth_page():
    """Renderiza a página temática de login e cadastro com persistência de sessão."""
    col_center1, col_center2, col_center3 = st.columns([1, 2, 1])
    
    with col_center2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align: center;'>"
            "<h1>🐉 Grimório do Mestre & D&D Copilot</h1>"
            "<p style='color: #c99a4e; font-size: 1.1em;'>Seu assistente de regras 5e/2024, mentor e validador de fichas</p>"
            "</div>",
            unsafe_allow_html=True
        )
        st.divider()

        total_users = count_users()
        if total_users == 0:
            st.info("🧙‍♂️ **Bem-vindo, Mestre!** Seja o primeiro a se registrar para assumir o perfil de **Mestre Administrador** do sistema.")

        tab_login, tab_register = st.tabs(["🔑 **Entrar (Login)**", "✨ **Criar Conta (Cadastro)**"])

        # 1. ABA DE LOGIN
        with tab_login:
            with st.form("login_form", clear_on_submit=False):
                st.markdown("#### Acesse sua conta")
                login_user = st.text_input("Usuário:", placeholder="seu_usuario", key="login_input_user").strip().lower()
                login_pass = st.text_input("Senha:", type="password", placeholder="••••••••", key="login_input_pass")
                
                submit_login = st.form_submit_button("🧙‍♂️ Entrar no Grimório", use_container_width=True, type="primary")

                if submit_login:
                    if not login_user or not login_pass:
                        st.warning("Por favor, preencha o usuário e a senha.")
                    else:
                        success, user_data, msg = authenticate_user(login_user, login_pass)
                        if success and user_data:
                            token = create_session_token(login_user)
                            st.query_params["session_token"] = token
                            st.session_state["authenticated_user"] = user_data
                            st.session_state["current_session_id"] = None
                            st.session_state["selected_audit_id"] = None
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

        # 2. ABA DE CADASTRO
        with tab_register:
            with st.form("register_form", clear_on_submit=False):
                st.markdown("#### Crie sua conta individual")
                reg_name = st.text_input("Seu Nome / Apelido:", placeholder="Ex: Fernando, João, Mestre").strip()
                reg_user = st.text_input("Nome de Usuário (login):", placeholder="letras, numeros e _", key="reg_input_user").strip().lower()
                
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    reg_pass = st.text_input("Senha:", type="password", placeholder="Mínimo 6 caracteres")
                with col_p2:
                    reg_pass_conf = st.text_input("Confirmar Senha:", type="password", placeholder="Repita a senha")

                st.markdown("---")
                st.markdown("##### 🔑 Sua Chave do Google Gemini (Gratuita)")
                reg_api_key = st.text_input(
                    "Chave de API do Gemini:",
                    type="password",
                    placeholder="Cole sua GEMINI_API_KEY aqui",
                    help="Sua chave é criptografada e salva no seu perfil privado."
                ).strip()

                with st.expander("❓ Como obter uma chave gratuita do Gemini em 1 minuto"):
                    st.markdown(
                        "1. Acesse o **[Google AI Studio](https://aistudio.google.com/app/apikey)** com sua conta Google.\n"
                        "2. Clique no botão azul **'Create API key'**.\n"
                        "3. Copie a chave gerada e cole no campo acima!\n"
                        "*(Você também pode adicionar ou alterar sua chave depois nas configurações).*"
                    )

                submit_register = st.form_submit_button("⚔️ Criar Minha Conta", use_container_width=True, type="primary")

                if submit_register:
                    if not reg_user or not reg_pass:
                        st.warning("Preencha o nome de usuário e a senha.")
                    elif len(reg_pass) < 6:
                        st.warning("A senha deve ter no mínimo 6 caracteres.")
                    elif reg_pass != reg_pass_conf:
                        st.error("As senhas informadas não coincidem.")
                    else:
                        success, msg = register_user(
                            username=reg_user,
                            password=reg_pass,
                            name=reg_name,
                            gemini_api_key=reg_api_key
                        )
                        if success:
                            st.success(msg)
                            st.info("Agora vá para a aba **Entrar (Login)** acima e digite suas credenciais!")
                        else:
                            st.error(msg)

def render_user_profile_sidebar(user_data: Dict[str, Any], agent):
    """Renderiza os dados do usuário logado na barra lateral com alternador de tema e logout."""
    st.sidebar.markdown("---")
    
    user_name = user_data.get("name") or user_data.get("username", "Aventureiro")
    is_admin = user_data.get("is_admin", False)
    badge = "👑 Mestre Administrador" if is_admin else "⚔️ Jogador"
    
    st.sidebar.markdown(f"👤 **{user_name}**")
    st.sidebar.caption(f"Perfil: **{badge}**")

    # Alternador de Tema de Visualização (Modo Claro vs Modo Escuro)
    curr_theme = st.session_state.get("theme_mode", "dark")
    if curr_theme == "dark":
        if st.sidebar.button("☀️ **Modo Claro (Pergaminho)**", key="btn_toggle_theme", use_container_width=True):
            st.session_state["theme_mode"] = "light"
            st.query_params["theme"] = "light"
            st.rerun()
    else:
        if st.sidebar.button("🌙 **Modo Escuro (Grimório)**", key="btn_toggle_theme", use_container_width=True):
            st.session_state["theme_mode"] = "dark"
            st.query_params["theme"] = "dark"
            st.rerun()

    with st.sidebar.expander("🔑 **Minha Chave Gemini**", expanded=not bool(user_data.get("gemini_api_key"))):
        curr_key = user_data.get("gemini_api_key", "")
        new_key = st.text_input(
            "Chave de API Gemini:",
            value=curr_key,
            type="password",
            placeholder="Insira sua GEMINI_API_KEY",
            help="Sua chave é criptografada e salva no banco de dados."
        ).strip()
        
        if st.button("💾 Salvar Chave de API", use_container_width=True):
            if new_key != curr_key:
                update_user_api_key(user_data["username"], new_key)
                user_data["gemini_api_key"] = new_key
                agent.update_config(api_key=new_key)
                st.success("Chave de API salva com sucesso!")
                st.rerun()

    if st.sidebar.button("🚪 **Sair (Logout)**", use_container_width=True, type="secondary"):
        st.query_params.clear()
        st.session_state.clear()
        st.rerun()
