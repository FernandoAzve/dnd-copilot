import streamlit as st
import json
import os
from typing import Dict, Any, List, Optional
from ..tools.dice import roll_dice
from ..tools.rules_lookup import lookup_condition
from ..rag.pdf_ingest import PDF_DIR, ingest_all_pdfs, delete_pdf_book, CHUNKS_FILE
from ..rag.vector_store import DnDKnowledgeBase
from ..storage.chat_storage import (
    create_session,
    save_session,
    load_session,
    list_sessions,
    delete_session,
    rename_session
)
from ..storage.audit_storage import (
    list_audits,
    get_audit,
    delete_audit
)
from ..auth.auth_ui import render_user_profile_sidebar

CONDITIONS_LIST = [
    "Agarrado (Grappled)",
    "Amedrontado (Frightened)",
    "Atordoado (Stunned)",
    "Caído (Prone)",
    "Cego (Blinded)",
    "Enfeitiçado (Charmed)",
    "Envenenado (Poisoned)",
    "Exausto (Exhaustion)",
    "Incapacitado (Incapacitated)",
    "Inconsciente (Unconscious)",
    "Invisível (Invisible)",
    "Paralisado (Paralyzed)",
    "Petrificado (Petrified)",
    "Restrito / Impedido (Restrained)",
    "Surdo (Deafened)"
]

def render_sidebar(agent, user_data: Optional[Dict[str, Any]] = None):
    """Renderiza a barra lateral unificada com navegação de módulos, histórico contextual, dados e livros."""
    username = user_data.get("username") if user_data else None
    is_admin = user_data.get("is_admin", False) if user_data else True
    current_view = st.session_state.get("main_view", "chat")

    with st.sidebar:
        st.markdown("## 🧙‍♂️ **Grimório do Sábio**")
        st.caption("Assistente & Mentor de D&D 5e / 2024")
        
        # 1. NAVEGAÇÃO PRINCIPAL ENTRE OS 3 MÓDULOS
        col_nav1, col_nav2, col_nav3 = st.columns(3)
        is_chat_active = (current_view == "chat")
        is_chars_active = (current_view == "characters")
        is_sheets_active = (current_view in ["sheets", "audit"])
        
        with col_nav1:
            if st.button("💬 **Grimório**", key="nav_btn_chat", use_container_width=True, type="primary" if is_chat_active else "secondary"):
                st.session_state["main_view"] = "chat"
                st.rerun()
        with col_nav2:
            if st.button("🛡️ **Heróis**", key="nav_btn_chars", use_container_width=True, type="primary" if is_chars_active else "secondary"):
                st.session_state["main_view"] = "characters"
                st.rerun()
        with col_nav3:
            if st.button("📋 **Auditoria**", key="nav_btn_sheets", use_container_width=True, type="primary" if is_sheets_active else "secondary"):
                st.session_state["main_view"] = "sheets"
                st.rerun()

        # Destaque do Personagem Ativo no Contexto
        try:
            from ..storage.character_storage import get_active_character_id, get_character
            act_id = get_active_character_id(username)
            act_char = get_character(act_id, username) if act_id else None
            if act_char:
                st.markdown(
                    f"<div style='background-color: var(--input-bg); border: 1px solid var(--primary-gold); border-radius: 6px; padding: 4px 8px; margin: 8px 0; font-size: 0.78rem; text-align: center;'>"
                    f"🛡️ <b>Ativo no Chat:</b> {act_char.get('name', 'Herói')} ({act_char.get('class_name', '')} {act_char.get('level', 1)})"
                    f"</div>",
                    unsafe_allow_html=True
                )
        except Exception:
            pass

        st.markdown("<hr style='margin: 8px 0; border-color: var(--border-color);'>", unsafe_allow_html=True)

        # 2. HISTÓRICO CONTEXTUAL
        if current_view == "chat":
            # Botão Nova Conversa
            if st.button("➕ **Nova Conversa**", key="btn_new_chat", use_container_width=True, type="primary"):
                new_id = create_session(mode=agent.mode, model=agent.model_name, username=username)
                st.session_state["current_session_id"] = new_id
                session_data = load_session(new_id, username=username)
                if session_data:
                    st.session_state["messages"] = session_data.get("messages", [])
                agent.reset_chat()
                st.rerun()

            # Lista de Conversas de Chat Salvas
            with st.expander("📜 **Conversas de Regras**", expanded=True):
                sessions = list_sessions(username=username)
                if not sessions:
                    st.caption("Nenhuma conversa salva ainda.")
                else:
                    current_id = st.session_state.get("current_session_id")
                    for s in sessions:
                        s_id = s["id"]
                        is_active = (s_id == current_id)
                        badge = " 🟢" if is_active else ""
                        
                        col_btn, col_del = st.columns([4, 1])
                        with col_btn:
                            btn_label = f"{s['title'][:20]}{badge}"
                            if st.button(btn_label, key=f"load_sess_{s_id}", use_container_width=True, type="primary" if is_active else "secondary"):
                                if not is_active:
                                    loaded = load_session(s_id, username=username)
                                    if loaded:
                                        st.session_state["current_session_id"] = s_id
                                        st.session_state["messages"] = loaded.get("messages", [])
                                        agent.update_config(mode=loaded.get("mode"), model_name=loaded.get("model"))
                                        st.rerun()
                        with col_del:
                            if st.button("🗑️", key=f"del_sess_{s_id}", help=f"Excluir '{s['title']}'"):
                                delete_session(s_id, username=username)
                                if s_id == current_id:
                                    new_id = create_session(username=username)
                                    st.session_state["current_session_id"] = new_id
                                    st.session_state["messages"] = load_session(new_id, username=username)["messages"]
                                st.rerun()

        elif current_view == "characters":
            if st.button("➕ **Novo Herói**", key="btn_new_hero", use_container_width=True, type="primary"):
                st.session_state["editing_character_id"] = ""
                st.session_state["character_form_data"] = None
                st.rerun()

        else:
            # Botão Nova Ficha
            is_nova_active = (st.session_state.get("selected_audit_id") == "nova")
            if st.button("➕ **Nova Auditoria de Ficha**", key="btn_new_audit", use_container_width=True, type="primary" if is_nova_active else "secondary"):
                st.session_state["selected_audit_id"] = "nova"
                st.rerun()

            # Lista de Fichas Auditadas
            with st.expander("📜 **Fichas Auditadas**", expanded=True):
                audits = list_audits(username=username)
                if not audits:
                    st.caption("Nenhuma ficha auditada ainda.")
                else:
                    curr_audit = st.session_state.get("selected_audit_id")
                    for a in audits:
                        a_id = a["id"]
                        is_selected = (a_id == curr_audit)
                        char_name = a.get("character_name", "Ficha")
                        class_lvl = a.get("class_level", "")
                        has_issues = a.get("has_issues", False)
                        status_icon = "⚠️" if has_issues else "✅"
                        badge = " 🟢" if is_selected else ""
                        
                        col_btn, col_del = st.columns([4, 1])
                        with col_btn:
                            btn_label = f"{status_icon} {char_name[:14]}{badge}"
                            if st.button(btn_label, key=f"sel_aud_{a_id}", use_container_width=True, type="primary" if is_selected else "secondary"):
                                if not is_selected:
                                    st.session_state["selected_audit_id"] = a_id
                                    st.rerun()
                        with col_del:
                            if st.button("🗑️", key=f"del_aud_{a_id}", help=f"Excluir ficha de {char_name}"):
                                delete_audit(a_id, username=username)
                                if curr_audit == a_id:
                                    st.session_state["selected_audit_id"] = "nova"
                                st.rerun()

        st.divider()

        # 3. Configurações de Atuação da IA
        with st.expander("⚙️ **Modo de Atuação da IA**", expanded=False):
            mode_options = {
                "mentor": "🧙‍♂️ Mentor de Iniciantes",
                "arbitro": "⚔️ Árbitro Rápido de Mesa",
                "regras_2024": "📖 Especialista Regras 2024"
            }
            
            selected_mode = st.selectbox(
                "Modo de Atuação:",
                options=list(mode_options.keys()),
                format_func=lambda x: mode_options[x],
                index=0 if agent.mode == "mentor" else (1 if agent.mode == "arbitro" else 2)
            )

            model_name = st.selectbox(
                "Modelo Gemini:",
                options=["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-flash-latest", "gemini-3.6-flash"],
                index=0
            )

            if selected_mode != agent.mode or model_name != agent.model_name:
                agent.update_config(model_name=model_name, mode=selected_mode)
                st.success("Configurações atualizadas!")

        st.divider()

        # 4. Rolador de Dados Rápido
        st.markdown("### 🎲 **Rolador de Dados**")
        
        cols = st.columns(4)
        quick_dice = ["d4", "d6", "d8", "d10"]
        for idx, d in enumerate(quick_dice):
            with cols[idx]:
                if st.button(d, key=f"btn_{d}", use_container_width=True):
                    res = roll_dice(f"1{d}")
                    st.session_state["last_dice_roll"] = res["breakdown"]

        cols2 = st.columns(3)
        quick_dice_2 = ["d12", "d20", "d100"]
        for idx, d in enumerate(quick_dice_2):
            with cols2[idx]:
                if st.button(d, key=f"btn_{d}", use_container_width=True):
                    res = roll_dice(f"1{d}")
                    st.session_state["last_dice_roll"] = res["breakdown"]

        with st.form("custom_dice_form", clear_on_submit=False):
            custom_formula = st.text_input("Fórmula:", value="1d20+5", placeholder="Ex: 2d6+3, 8d6, 4d6kh3")
            adv_col1, adv_col2 = st.columns(2)
            with adv_col1:
                adv = st.checkbox("Vantagem", value=False)
            with adv_col2:
                disadv = st.checkbox("Desvantagem", value=False)
                
            submitted = st.form_submit_button("🎯 Rolar Expressão", use_container_width=True)
            if submitted and custom_formula:
                res = roll_dice(formula=custom_formula, advantage=adv, disadvantage=disadv)
                st.session_state["last_dice_roll"] = res["breakdown"]

        if "last_dice_roll" in st.session_state and st.session_state["last_dice_roll"]:
            st.info(st.session_state["last_dice_roll"])

        st.divider()

        # 5. Guia Rápido de Condições
        with st.expander("🛡️ **Consulta Rápida: Condições**", expanded=False):
            cond_chosen = st.selectbox("Selecione uma condição:", options=CONDITIONS_LIST)
            if cond_chosen:
                base_name = cond_chosen.split(" ")[0]
                cond_info = lookup_condition(base_name)
                if cond_info.get("found"):
                    st.markdown(cond_info["card"])

        st.divider()

        # 6. Ingestão e Biblioteca de Livros (PDFs) com Controle de Acesso (RBAC)
        with st.expander("📚 **Biblioteca de Livros (PDFs)**", expanded=False):
            st.caption("Manuais e suplementos de D&D indexados na memória compartilhada.")
            
            os.makedirs(PDF_DIR, exist_ok=True)
            existing_pdfs = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
            
            if existing_pdfs:
                st.markdown("**Livros disponíveis no sistema:**")
                for p in existing_pdfs:
                    file_size_mb = os.path.getsize(os.path.join(PDF_DIR, p)) / (1024 * 1024)
                    st.markdown(f"📖 `{p}` ({file_size_mb:.1f} MB)")
            else:
                st.info("Nenhum livro PDF encontrado em `data/pdf_books/`.")

            # Controle Exclusivo para Mestre / Administrador
            if is_admin:
                st.markdown("---")
                st.markdown("👑 **Gerenciamento do Mestre:**")
                
                # Exclusão de livros
                if existing_pdfs:
                    book_to_delete = st.selectbox("Excluir livro:", options=["-- Selecione --"] + existing_pdfs, key="sel_del_book")
                    if book_to_delete and book_to_delete != "-- Selecione --":
                        if st.button(f"🗑️ Excluir '{book_to_delete}'", type="secondary", use_container_width=True):
                            del_res = delete_pdf_book(book_to_delete)
                            if del_res["success"]:
                                st.success(del_res["message"])
                                agent.kb = DnDKnowledgeBase()
                                st.rerun()
                            else:
                                st.error(del_res["message"])

                st.markdown("**Adicionar novo livro (PDF):**")
                if "processed_upload_names" not in st.session_state:
                    st.session_state["processed_upload_names"] = set()

                uploaded_files = st.file_uploader(
                    "Selecione um PDF:",
                    type=["pdf"],
                    accept_multiple_files=True,
                    key="pdf_file_uploader",
                    help="Faça upload do Livro do Jogador, Livro do Mestre, etc."
                )
                
                new_files_to_save = []
                if uploaded_files:
                    for up_file in uploaded_files:
                        if up_file.name not in st.session_state["processed_upload_names"]:
                            new_files_to_save.append(up_file)

                if new_files_to_save:
                    if st.button(f"📥 Salvar e Indexar {len(new_files_to_save)} Livro(s)", use_container_width=True):
                        for up_file in new_files_to_save:
                            save_path = os.path.join(PDF_DIR, up_file.name)
                            with open(save_path, "wb") as f:
                                f.write(up_file.getbuffer())
                            st.session_state["processed_upload_names"].add(up_file.name)
                        
                        prog_bar = st.progress(0, text="Lendo páginas do livro...")
                        status_text = st.empty()
                        
                        def ui_progress(curr, total, name):
                            pct = int((curr / total) * 100)
                            prog_bar.progress(pct, text=f"Lendo {name}: pág. {curr}/{total} ({pct}%)")
                            status_text.caption(f"⚡ Extraindo página {curr} de {total}...")
                            
                        res = ingest_all_pdfs(ui_progress)
                        status_text.empty()
                        prog_bar.empty()
                        
                        if res["success"]:
                            st.success(res["message"])
                            agent.kb = DnDKnowledgeBase()
                            st.rerun()
                        else:
                            st.warning(res["message"])

                elif st.button("⚡ Re-indexar Livros Existentes", use_container_width=True):
                    prog_bar = st.progress(0, text="Iniciando re-indexação...")
                    status_text = st.empty()
                    
                    def ui_progress(curr, total, name):
                        pct = int((curr / total) * 100)
                        prog_bar.progress(pct, text=f"Lendo {name}: pág. {curr}/{total} ({pct}%)")
                        status_text.caption(f"⚡ Extraindo página {curr} de {total}...")
                        
                    res = ingest_all_pdfs(ui_progress)
                    status_text.empty()
                    prog_bar.empty()
                    
                    if res["success"]:
                        st.success(res["message"])
                        agent.kb = DnDKnowledgeBase()
                        st.rerun()
                    else:
                        st.warning(res["message"])
            else:
                st.caption("🛡️ *Apenas o Mestre Administrador pode adicionar ou remover livros da biblioteca.*")

        # 7. Painel de Perfil e Logout
        if user_data:
            render_user_profile_sidebar(user_data, agent)

def render_chat_message(role: str, content: str, tool_logs: Optional[List[Dict[str, Any]]] = None):
    """Renderiza uma mensagem de chat com visual temático e limpo."""
    avatar = "🧙‍♂️" if role == "model" or role == "assistant" else "👤"
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)
        if tool_logs:
            with st.expander("🛠️ Ações executadas pelo Grimório", expanded=False):
                for t in tool_logs:
                    st.code(f"Ferramenta: {t.get('tool')}\nParâmetros: {json.dumps(t.get('args', {}), ensure_ascii=False)}\nResultado: {t.get('result')}", language="json")
