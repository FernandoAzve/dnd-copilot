import streamlit as st
import os
import json
from PIL import Image
import io
from typing import Optional
from ..tools.sheet_validator import SheetValidator
from ..storage.audit_storage import (
    save_audit,
    list_audits,
    get_audit,
    delete_audit,
    append_audit_message
)
from .components import render_chat_message

def render_sheet_auditor_tab(agent, username: Optional[str] = None):
    """
    Renderiza o Auditor de Fichas em layout Master-Detail (Painel Duplo) com isolamento por usuário:
    - Coluna Esquerda: Lista de Fichas Auditadas (Histórico do usuário) + Botão de Nova Auditoria
    - Coluna Direita: Painel Interativo de Chat, Diagnóstico e Ações da Ficha Selecionada
    """
    all_audits = list_audits(username=username)
    
    # Inicializar seleção padrão
    if "selected_audit_id" not in st.session_state:
        st.session_state["selected_audit_id"] = all_audits[0]["id"] if all_audits else None

    # Se a lista estiver vazia, forçar modo nova auditoria
    if not all_audits:
        st.session_state["selected_audit_id"] = "nova"

    col_left, col_right = st.columns([1.1, 2.2], gap="medium")

    # ==========================================
    # COLUNA ESQUERDA: LISTA DE FICHAS & HISTÓRICO
    # ==========================================
    with col_left:
        st.markdown("#### 📜 **Fichas & Histórico**")
        
        # Botão para criar nova auditoria
        is_nova_active = (st.session_state["selected_audit_id"] == "nova")
        if st.button("➕ **Nova Auditoria de Ficha**", key="btn_panel_nova", use_container_width=True, type="primary" if is_nova_active else "secondary"):
            st.session_state["selected_audit_id"] = "nova"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if all_audits:
            search_query = st.text_input("🔍 Buscar ficha:", placeholder="Nome ou classe...", key="search_left_panel")
            
            filtered = all_audits
            if search_query.strip():
                q = search_query.lower()
                filtered = [
                    a for a in all_audits
                    if q in a.get("character_name", "").lower() or q in a.get("filename", "").lower() or q in a.get("class_level", "").lower()
                ]

            st.caption(f"{len(filtered)} ficha(s) salva(s):")
            
            for a in filtered:
                a_id = a["id"]
                char_name = a.get("character_name", "Personagem")
                class_lvl = a.get("class_level", "Classe")
                is_selected = (st.session_state.get("selected_audit_id") == a_id)
                has_issues = a.get("has_issues", False)
                status_icon = "⚠️" if has_issues else "✅"
                file_icon = "📄" if a.get("file_type") == "pdf" else "📸"
                
                # Card selecionável na coluna esquerda
                btn_type = "primary" if is_selected else "secondary"
                btn_label = f"{status_icon} {char_name[:18]} ({class_lvl[:10]})"
                
                col_c1, col_c2 = st.columns([4.5, 1])
                with col_c1:
                    if st.button(btn_label, key=f"sel_card_{a_id}", use_container_width=True, type=btn_type):
                        st.session_state["selected_audit_id"] = a_id
                        st.rerun()
                with col_c2:
                    if st.button("🗑️", key=f"del_left_{a_id}", help=f"Excluir {char_name}"):
                        delete_audit(a_id, username=username)
                        if st.session_state.get("selected_audit_id") == a_id:
                            remaining = list_audits(username=username)
                            st.session_state["selected_audit_id"] = remaining[0]["id"] if remaining else "nova"
                        st.rerun()
        else:
            st.info("Nenhuma ficha auditada ainda.")

    # ==========================================
    # COLUNA DIREITA: CONVERSA E DIAGNÓSTICO ATIVO
    # ==========================================
    with col_right:
        # 1. TELA DE UPLOAD / NOVA AUDITORIA
        if st.session_state["selected_audit_id"] == "nova":
            st.markdown("### 🔍 **Nova Auditoria de Ficha**")
            st.markdown(
                "Envie uma **foto de uma ficha física de papel** (mesmo manuscrita) ou um **arquivo PDF digital**. "
                "O Grimório usará visão computacional combinada com os **livros oficiais indexados** para verificar cálculos e regras, "
                "citando as páginas exatas."
            )
            st.divider()

            col_up, col_prev = st.columns([1.2, 1])
            with col_up:
                uploaded_sheet = st.file_uploader(
                    "Selecione o arquivo da ficha (PDF ou Imagem):",
                    type=["pdf", "png", "jpg", "jpeg", "webp"],
                    key="uploader_master_detail",
                    help="Aceita fotos nítidas ou PDFs preenchíveis"
                )
                
                user_notes = st.text_area(
                    "Observações adicionais sobre o personagem (opcional):",
                    placeholder="Ex: 'Guerreiro nível 5 Campeão', 'Criado com regras de 2024'",
                    key="notes_master_detail"
                )

                audit_btn = st.button("🚀 Auditar e Iniciar Conversa com a Ficha", use_container_width=True, type="primary")

            with col_prev:
                if uploaded_sheet:
                    ext = os.path.splitext(uploaded_sheet.name)[1].lower()
                    if ext in [".png", ".jpg", ".jpeg", ".webp"]:
                        st.image(uploaded_sheet, caption=f"Foto: {uploaded_sheet.name}", use_container_width=True)
                    else:
                        st.info(f"📄 PDF: **{uploaded_sheet.name}** ({uploaded_sheet.size / 1024:.1f} KB)")
                else:
                    st.info("📌 A prévia da ficha aparecerá aqui.")

            if audit_btn:
                if not uploaded_sheet:
                    st.warning("Selecione um arquivo de ficha antes de iniciar a auditoria.")
                else:
                    with st.spinner("🧙‍♂️ Executando auditoria determinística com RAG dos livros e visão computacional..."):
                        validator = SheetValidator(api_key=agent.api_key, model_name=agent.model_name)
                        file_bytes = uploaded_sheet.getvalue()
                        
                        result = validator.validate_sheet_file(
                            file_bytes=file_bytes,
                            filename=uploaded_sheet.name,
                            mime_type=uploaded_sheet.type,
                            notes=user_notes
                        )

                    if result["success"]:
                        audit_id = save_audit(
                            filename=uploaded_sheet.name,
                            report=result["report"],
                            user_notes=user_notes,
                            file_type="pdf" if uploaded_sheet.name.lower().endswith(".pdf") else "image",
                            extracted_data=result.get("extracted_data"),
                            username=username
                        )
                        st.session_state["selected_audit_id"] = audit_id
                        st.success("✅ Ficha auditada com sucesso!")
                        st.rerun()
                    else:
                        st.error(result["report"])

        # 2. TELA DE CHAT CONTÍNUO & RELATÓRIO DA FICHA SELECIONADA
        else:
            audit_id = st.session_state["selected_audit_id"]
            audit_data = get_audit(audit_id, username=username)
            
            if not audit_data:
                st.session_state["selected_audit_id"] = "nova"
                st.rerun()
                return

            char_name = audit_data.get("character_name", "Personagem")
            class_lvl = audit_data.get("class_level", "Classe")
            created_date = audit_data.get("created_at", "")[:16].replace("T", " ")
            has_issues = audit_data.get("has_issues", False)
            badge = "⚠️ Ajustes Recomendados" if has_issues else "✅ Ficha Válida"

            # Cabeçalho da Ficha Selecionada
            st.markdown(f"### 🛡️ **{char_name}** — *{class_lvl}*")
            st.caption(f"📁 Arquivo: `{audit_data.get('filename')}` | 📅 Auditada em: {created_date} | Status: **{badge}**")

            with st.expander("📄 **Clique aqui para ver o Relatório Completo de Auditoria**", expanded=False):
                st.markdown(audit_data.get("report", "Sem relatório disponível."))

            st.divider()
            st.markdown(f"##### 💬 **Conversa Contínua sobre {char_name}:**")
            st.caption("Pergunte qualquer dúvida de regras, magias, perícias, cálculos de dano ou evolução de nível deste personagem.")

            # Renderizar histórico de mensagens da conversa desta ficha
            messages = audit_data.get("messages", [])
            for idx, msg in enumerate(messages):
                if idx == 0 and "Relatório de Auditoria" in msg.get("content", ""):
                    continue
                render_chat_message(role=msg["role"], content=msg["content"])

            # Input de chat exclusivo desta ficha
            sheet_query = st.chat_input(f"Pergunte algo sobre {char_name} (ex: dano de ataque, regras 2024, talentos)...", key="sheet_active_chat_input")
            if sheet_query:
                # 1. Salvar mensagem do usuário no diretório isolado
                append_audit_message(audit_id, "user", sheet_query, username=username)
                
                # 2. Consultar Gemini com contexto estrito da ficha e livros
                with st.spinner(f"Consultando os tomos de regras sobre {char_name}..."):
                    context_prompt = (
                        f"Você está em uma conversa contínua com o jogador sobre a seguinte ficha de personagem:\n"
                        f"Nome: {char_name}\n"
                        f"Classe e Nível: {class_lvl}\n\n"
                        f"Relatório da Ficha:\n{audit_data.get('report')}\n\n"
                        f"Dados Estruturados da Ficha:\n{json.dumps(audit_data.get('extracted_data', {}), ensure_ascii=False)}\n\n"
                        f"Pergunta do Jogador: {sheet_query}\n\n"
                        f"Responda de forma precisa, didática e cite a página do livro oficial de D&D 2024 quando aplicável."
                    )
                    
                    response_data = agent.answer_query(context_prompt)
                    bot_text = response_data.get("text", "Não obtive resposta.")

                # 3. Salvar resposta da IA no histórico da ficha
                append_audit_message(audit_id, "model", bot_text, username=username)
                st.rerun()
