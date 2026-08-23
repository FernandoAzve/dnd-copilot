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

def render_sidebar(agent):
    """Renderiza a barra lateral com histórico de chats, configurações, dados e livros."""
    with st.sidebar:
        st.markdown("## 🧙‍♂️ **Grimório do Sábio**")
        st.caption("Assistente & Mentor de D&D 5e / 2024")
        
        # 1. Gerenciador de Sessões de Chat
        if st.button("➕ **Nova Conversa**", use_container_width=True, type="primary"):
            new_id = create_session(mode=agent.mode, model=agent.model_name)
            st.session_state["current_session_id"] = new_id
            session_data = load_session(new_id)
            if session_data:
                st.session_state["messages"] = session_data.get("messages", [])
            agent.reset_chat()
            st.rerun()

        # Histórico de Conversas Salvas
        with st.expander("📜 **Histórico de Conversas**", expanded=False):
            sessions = list_sessions()
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
                        btn_label = f"{s['title'][:24]}{badge}"
                        if st.button(btn_label, key=f"load_sess_{s_id}", use_container_width=True, disabled=is_active):
                            loaded = load_session(s_id)
                            if loaded:
                                st.session_state["current_session_id"] = s_id
                                st.session_state["messages"] = loaded.get("messages", [])
                                agent.update_config(mode=loaded.get("mode"), model_name=loaded.get("model"))
                                st.rerun()
                    with col_del:
                        if st.button("🗑️", key=f"del_sess_{s_id}", help=f"Excluir '{s['title']}'"):
                            delete_session(s_id)
                            if s_id == current_id:
                                # Se deletou a atual, cria uma nova
                                new_id = create_session()
                                st.session_state["current_session_id"] = new_id
                                st.session_state["messages"] = load_session(new_id)["messages"]
                            st.rerun()

        st.divider()

        # 2. Configurações da IA
        with st.expander("⚙️ **Configurações & Chave API**", expanded=not bool(agent.api_key)):
            api_key = st.text_input(
                "Chave Google Gemini:",
                value=agent.api_key,
                type="password",
                placeholder="Insira sua GEMINI_API_KEY",
                help="Obtenha uma chave gratuita no Google AI Studio (https://aistudio.google.com/app/apikey)"
            )
            
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
                options=["gemini-3.6-flash", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
                index=0
            )

            if api_key != agent.api_key or selected_mode != agent.mode or model_name != agent.model_name:
                agent.update_config(api_key=api_key, model_name=model_name, mode=selected_mode)
                st.success("Configurações atualizadas!")

        st.divider()

        # 3. Rolador de Dados Rápido
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

        # 4. Guia Rápido de Condições
        with st.expander("🛡️ **Consulta Rápida: Condições**", expanded=False):
            cond_chosen = st.selectbox("Selecione uma condição:", options=CONDITIONS_LIST)
            if cond_chosen:
                base_name = cond_chosen.split(" ")[0]
                cond_info = lookup_condition(base_name)
                if cond_info.get("found"):
                    st.markdown(cond_info["card"])

        st.divider()

        # 5. Ingestão e Biblioteca de Livros (PDFs)
        with st.expander("📚 **Biblioteca de Livros (PDFs)**", expanded=False):
            st.caption("Gerencie os manuais e suplementos de D&D indexados na memória.")
            
            os.makedirs(PDF_DIR, exist_ok=True)
            existing_pdfs = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
            
            if existing_pdfs:
                st.markdown("**Livros disponíveis:**")
                for p in existing_pdfs:
                    file_size_mb = os.path.getsize(os.path.join(PDF_DIR, p)) / (1024 * 1024)
                    st.markdown(f"📖 `{p}` ({file_size_mb:.1f} MB)")
                
                # Exclusão de livros
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
            else:
                st.info("Nenhum livro PDF encontrado em `data/pdf_books/`.")

            st.markdown("---")
            st.markdown("**Adicionar novo livro:**")
            
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

def render_chat_message(role: str, content: str, tool_logs: Optional[List[Dict[str, Any]]] = None):
    """Renderiza uma mensagem de chat com visual temático."""
    avatar = "🧙‍♂️" if role == "model" or role == "assistant" else "👤"
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)
        if tool_logs:
            with st.expander("🛠️ Ações executadas pelo Grimório", expanded=False):
                for t in tool_logs:
                    st.code(f"Ferramenta: {t.get('tool')}\nParâmetros: {json.dumps(t.get('args', {}), ensure_ascii=False)}\nResultado: {t.get('result')}", language="json")
