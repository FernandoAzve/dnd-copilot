import streamlit as st
import os
import json
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
    Renderiza o módulo do Auditor de Fichas com layout unificado:
    - Tela de Nova Auditoria (Card centralizado e limpo)
    - Tela de Ficha Ativa (Chat contínuo em largura total com relatório e histórico)
    """
    # Inicializar seleção padrão se não houver
    if "selected_audit_id" not in st.session_state or not st.session_state["selected_audit_id"]:
        all_audits = list_audits(username=username)
        st.session_state["selected_audit_id"] = all_audits[0]["id"] if all_audits else "nova"

    # =======================================================
    # 1. TELA DE NOVA AUDITORIA (CARD CENTRALIZADO E ELEGANTE)
    # =======================================================
    if st.session_state["selected_audit_id"] == "nova":
        st.markdown("### 📋 **Nova Auditoria de Ficha**")
        st.markdown(
            "Envie uma **foto de uma ficha física de papel** (mesmo manuscrita) ou um **arquivo PDF digital**. "
            "O Grimório usará visão computacional combinada com os **livros oficiais indexados** para verificar cálculos e regras de D&D 2024, "
            "citando as páginas exatas."
        )
        st.divider()

        uploaded_sheet = st.file_uploader(
            "Selecione o arquivo da ficha (PDF ou Imagem):",
            type=["pdf", "png", "jpg", "jpeg", "webp"],
            key="uploader_single_view",
            help="Aceita fotos nítidas ou PDFs preenchíveis"
        )

        if uploaded_sheet:
            ext = os.path.splitext(uploaded_sheet.name)[1].lower()
            if ext in [".png", ".jpg", ".jpeg", ".webp"]:
                st.image(uploaded_sheet, caption=f"Prévia: {uploaded_sheet.name}", use_container_width=True)
            else:
                st.info(f"📄 Arquivo PDF Selecionado: **{uploaded_sheet.name}** ({uploaded_sheet.size / 1024:.1f} KB)")

        user_notes = st.text_area(
            "Observações adicionais sobre o personagem (opcional):",
            placeholder="Ex: 'Guerreiro nível 5 Campeão', 'Personagem criado com regras de 2024'",
            key="notes_single_view"
        )

        audit_btn = st.button("🚀 Iniciar Auditoria e Conversa com a Ficha", use_container_width=True, type="primary")

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

    # =======================================================
    # 2. TELA DE CHAT CONTÍNUO & RELATÓRIO DA FICHA SELECIONADA
    # =======================================================
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

        # Cabeçalho Elegante da Ficha Ativa
        st.markdown(f"### 🛡️ **{char_name}** — *{class_lvl}*")
        st.caption(f"📁 Arquivo: `{audit_data.get('filename')}` | 📅 Auditada em: {created_date} | Status: **{badge}**")
        st.divider()

        # Renderizar fluxo de conversa contínua da ficha (Iniciando com o Relatório de Auditoria completo)
        messages = audit_data.get("messages", [])
        if not messages and audit_data.get("report"):
            messages = [{"role": "model", "content": audit_data["report"]}]

        for msg in messages:
            render_chat_message(role=msg["role"], content=msg["content"])

        # Input de chat exclusivo desta ficha
        sheet_query = st.chat_input(f"Pergunte algo sobre {char_name} (ex: dano de ataque, regras 2024, talentos)...", key="sheet_active_chat_input")
        if sheet_query:
            # 1. Salvar mensagem do usuário no histórico privado
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
