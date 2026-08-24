import streamlit as st
import json
import re
from typing import Optional, Dict, Any, List

from ..storage.character_storage import (
    save_character,
    get_character,
    list_characters,
    delete_character,
    get_active_character_id,
    set_active_character_id,
    get_default_character_data
)
from ..tools.character_importer import extract_and_build_character_from_file
from ..tools.pdf_exporter import generate_sheet_pdf
from ..tools.dnd_catalog import (
    CLASSES_2024,
    SPECIES_2024,
    BACKGROUNDS_2024,
    WEAPONS_2024,
    ARMOR_2024,
    FEATS_2024,
    MAGIC_ITEMS_2024,
    SPELLS_CATALOG,
    get_classes_list,
    get_subclasses_for_class,
    get_species_list,
    get_backgrounds_list,
    get_weapons_list,
    get_armor_list,
    get_spells_list,
    get_feats_list,
    get_magic_items_list
)
from .components import render_chat_message

SKILLS_LIST = [
    ("Acrobacia", "acrobacia", "DES"),
    ("Arcanismo", "arcanismo", "INT"),
    ("Atletismo", "atletismo", "FOR"),
    ("Atuação", "atuacao", "CAR"),
    ("Enganação", "enganacao", "CAR"),
    ("Furtividade", "furtividade", "DES"),
    ("História", "historia", "INT"),
    ("Intimidação", "intimidacao", "CAR"),
    ("Intuição", "intuicao", "SAB"),
    ("Investigação", "investigacao", "INT"),
    ("Lidar com Animais", "lidar_com_animais", "SAB"),
    ("Medicina", "medicina", "SAB"),
    ("Natureza", "natureza", "INT"),
    ("Percepção", "percepcao", "SAB"),
    ("Persuasão", "persuasao", "CAR"),
    ("Prestidigitação", "prestidigitacao", "DES"),
    ("Religião", "religiao", "INT"),
    ("Sobrevivência", "sobrevivencia", "SAB")
]

def render_character_management_tab(agent, username: Optional[str] = None):
    """
    Renderiza a Central de Heróis & Personagens D&D 2024:
    - Lista de Personagens e Seleção de Ativo no Chat
    - Importação Inteligente Multimodal (PDF / Foto)
    - Editor Oficial 2024 com Menus Interativos de Seleção e Busca
    """
    st.markdown("## 🛡️ **Central de Heróis do Jogador**")
    st.markdown(
        "Cadastre suas fichas para que o **Sábio do Grimório** conheça seus atributos, itens mágicos, "
        "bônus de ataque, maestrias e magias **automaticamente em todas as conversas**!"
    )
    
    # Obter personagem ativo atual
    active_char_id = get_active_character_id(username)
    active_char_data = get_character(active_char_id, username) if active_char_id else None
    
    # Barra de Status do Personagem Ativo
    col_act_bar1, col_act_bar2 = st.columns([4, 1.2])
    with col_act_bar1:
        if active_char_data:
            active_name = active_char_data.get("name", "Personagem")
            active_cls = active_char_data.get("class_name", "Classe")
            active_subcls = active_char_data.get("subclass", "")
            active_lvl = active_char_data.get("level", 1)
            st.info(f"🌟 **Personagem Ativo no Chat:** `{active_name}` — *{active_cls} {f'({active_subcls})' if active_subcls else ''} Nível {active_lvl}*")
        else:
            st.warning("⚠️ **Nenhum personagem ativo no momento.** Suas conversas no chat utilizarão o modo de consulta genérica de regras.")
    with col_act_bar2:
        if active_char_data:
            if st.button("⚪ **Desativar Contexto**", key="btn_clear_active_char", use_container_width=True):
                set_active_character_id("", username=username)
                st.rerun()

    st.divider()

    # Abas de Gestão
    tab_list, tab_import, tab_manual = st.tabs([
        "📜 **Meus Personagens**",
        "📥 **Importar Ficha (PDF / Foto)**",
        "✨ **Criar / Editar Manualmente**"
    ])

    # =========================================================================
    # ABA 1: LISTA DE PERSONAGENS CADASTRADOS
    # =========================================================================
    with tab_list:
        chars = list_characters(username=username)
        if not chars:
            st.info("Você ainda não tem nenhum herói cadastrado. Importe uma ficha em PDF/Foto ou crie uma ficha manualmente nas abas acima!")
        else:
            for c in chars:
                c_id = c["id"]
                full_c = get_character(c_id, username=username)
                if not full_c:
                    continue
                    
                is_active = (c_id == active_char_id)
                
                # Card do Personagem
                with st.expander(f"🛡️ **{c['name']}** — *{c['class_name']} {c.get('subclass', '')} Nível {c['level']}* {' 🟢 [ATIVO NO CHAT]' if is_active else ''}", expanded=is_active):
                    col_info1, col_info2, col_info3 = st.columns(3)
                    with col_info1:
                        st.markdown(f"**Espécie:** {full_c.get('species', 'Humano')}")
                        st.markdown(f"**Antecedente:** {full_c.get('background', 'Soldado')}")
                        st.markdown(f"**Classe de Armadura (CA):** `{full_c.get('armor_class', 10)}`")
                    with col_info2:
                        st.markdown(f"**Pontos de Vida:** `{full_c.get('hit_points_current', 10)} / {full_c.get('hit_points_max', 10)}`")
                        st.markdown(f"**Deslocamento:** {full_c.get('speed', '9m')}")
                        pb = 2 + (max(1, full_c.get('level', 1)) - 1) // 4
                        st.markdown(f"**Bônus de Proficiência:** `+{pb}`")
                    with col_info3:
                        abilities = full_c.get("abilities", {})
                        st.markdown(
                            f"**Atributos:** FOR `{abilities.get('str', 10)}` | DES `{abilities.get('dex', 10)}` | CON `{abilities.get('con', 10)}`<br>"
                            f"INT `{abilities.get('int', 10)}` | SAB `{abilities.get('wis', 10)}` | CAR `{abilities.get('cha', 10)}`",
                            unsafe_allow_html=True
                        )

                    # Ataques e Magias Resumidos
                    attacks = full_c.get("attacks", [])
                    if attacks:
                        atk_strs = [f"⚔️ **{a.get('name')}:** Acerto {a.get('attack_bonus')}, Dano {a.get('damage')} ({a.get('damage_type')})" for a in attacks if a.get("name")]
                        st.markdown("<br>".join(atk_strs), unsafe_allow_html=True)

                    # Ações do Personagem
                    st.markdown("<br>", unsafe_allow_html=True)
                    col_act1, col_act2, col_act3, col_act4 = st.columns([2, 1.5, 1.5, 1])
                    with col_act1:
                        if not is_active:
                            if st.button("⭐ **Tornar Ativo no Chat**", key=f"set_act_{c_id}", type="primary", use_container_width=True):
                                set_active_character_id(c_id, username)
                                st.success(f"'{c['name']}' agora é seu personagem ativo no chat!")
                                st.rerun()
                        else:
                            st.success("✅ Ativo no Chat")
                    
                    with col_act2:
                        if st.button("✏️ **Editar Ficha**", key=f"edit_btn_{c_id}", use_container_width=True):
                            st.session_state["editing_character_id"] = c_id
                            st.session_state["character_form_data"] = full_c
                            st.rerun()

                    with col_act3:
                        # Gerar PDF da Ficha
                        try:
                            mock_audit_for_pdf = {
                                "character_name": full_c.get("name", "Personagem"),
                                "class_level": f"{full_c.get('class_name', '')} {full_c.get('subclass', '')} Nível {full_c.get('level', 1)}",
                                "filename": "Ficha Cadastrada",
                                "created_at": full_c.get("created_at", ""),
                                "has_issues": False,
                                "report": (
                                    f"### 📋 Ficha de Personagem: {full_c.get('name')}\n\n"
                                    f"**Espécie:** {full_c.get('species')} | **Antecedente:** {full_c.get('background')}\n\n"
                                    f"**Equipamento & Itens:** {', '.join(full_c.get('magic_items', [])) or 'Nenhum'}\n\n"
                                    f"**Habilidades & Talentos:** {full_c.get('features_and_traits', '')}"
                                ),
                                "extracted_data": {
                                    "ability_scores": full_c.get("abilities", {}),
                                    "saving_throws": full_c.get("abilities", {})
                                }
                            }
                            pdf_bytes = generate_sheet_pdf(mock_audit_for_pdf)
                            safe_name = "".join(c for c in full_c.get("name", "Ficha") if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
                            st.download_button(
                                label="📄 **Baixar PDF**",
                                data=pdf_bytes,
                                file_name=f"Ficha_{safe_name}.pdf",
                                mime="application/pdf",
                                key=f"dl_pdf_{c_id}",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.caption(f"Erro PDF: {e}")

                    with col_act4:
                        if st.button("🗑️", key=f"del_char_{c_id}", help="Excluir este personagem"):
                            delete_character(c_id, username=username)
                            st.rerun()

    # =========================================================================
    # ABA 2: IMPORTAÇÃO INTELIGENTE VIA PDF OU FOTO
    # =========================================================================
    with tab_import:
        st.markdown("### 📥 **Importar Ficha Digital ou Manuscrita**")
        st.markdown(
            "Envie o arquivo PDF digital da sua ficha ou fotos nítidas de uma ficha de papel. "
            "A inteligência artificial extrairá automaticamente os atributos, armas, magias e perícias "
            "e cadastrará o personagem na sua conta."
        )
        
        uploaded_file = st.file_uploader(
            "Selecione o arquivo da ficha (PDF ou Imagem):",
            type=["pdf", "png", "jpg", "jpeg", "webp"],
            key="char_import_uploader"
        )
        
        if uploaded_file is not None:
            if st.button("⚡ **Processar e Cadastrar Personagem**", type="primary", key="btn_run_char_import"):
                with st.spinner("Decifrando a ficha e estruturando os dados do aventureiro..."):
                    file_bytes = uploaded_file.read()
                    char_extracted = extract_and_build_character_from_file(
                        file_bytes=file_bytes,
                        filename=uploaded_file.name,
                        api_key=agent.api_key
                    )
                    
                    new_char_id = save_character(char_extracted, username=username)
                    set_active_character_id(new_char_id, username=username)
                    
                    st.success(f"🎉 Personagem **{char_extracted['name']}** ({char_extracted['class_name']} Nível {char_extracted['level']}) importado e ativado com sucesso!")
                    st.rerun()

    # =========================================================================
    # ABA 3: CRIAR OU EDITAR FICHA MANUALMENTE COM MENUS D&D 2024
    # =========================================================================
    with tab_manual:
        editing_id = st.session_state.get("editing_character_id", "")
        if "character_form_data" not in st.session_state or not st.session_state["character_form_data"]:
            st.session_state["character_form_data"] = get_default_character_data()
            
        form_data = st.session_state["character_form_data"]
        
        st.markdown(f"### {'✏️ **Editar Personagem:** ' + form_data.get('name', '') if editing_id else '✨ **Criar Novo Personagem Oficial D&D 2024**'}")
        if editing_id:
            if st.button("➕ **Criar Nova Ficha em Branco**", key="btn_cancel_edit"):
                st.session_state["editing_character_id"] = ""
                st.session_state["character_form_data"] = get_default_character_data()
                st.rerun()
                
        with st.form(key="manual_character_form_2024"):
            # 1. IDENTIFICAÇÃO BÁSICA COM CATÁLOGO
            st.markdown("#### 👤 1. Identificação & Origem")
            col_id1, col_id2, col_id3 = st.columns(3)
            with col_id1:
                name_val = st.text_input("Nome do Personagem:", value=form_data.get("name", "Novo Aventureiro"))
                
                # Menu de Espécies 2024
                all_species = get_species_list()
                curr_species = form_data.get("species", "Humano")
                species_idx = all_species.index(curr_species) if curr_species in all_species else 0
                species_val = st.selectbox("Espécie / Raça Oficial (2024):", all_species, index=species_idx)

            with col_id2:
                # Menu de Classes 2024
                all_classes = get_classes_list()
                curr_class = form_data.get("class_name", "Guerreiro")
                class_idx = all_classes.index(curr_class) if curr_class in all_classes else 0
                class_val = st.selectbox("Classe Principal (2024):", all_classes, index=class_idx)
                
                # Menu Dinâmico de Subclasses
                available_subclasses = get_subclasses_for_class(class_val)
                curr_subclass = form_data.get("subclass", "")
                subclass_idx = available_subclasses.index(curr_subclass) if curr_subclass in available_subclasses else 0
                subclass_val = st.selectbox("Subclasse Oficial (2024):", available_subclasses, index=subclass_idx)

            with col_id3:
                level_val = st.number_input("Nível do Personagem:", min_value=1, max_value=20, value=int(form_data.get("level", 1)))
                
                # Menu de Antecedentes 2024
                all_backgrounds = get_backgrounds_list()
                curr_bg = form_data.get("background", "Soldado")
                bg_idx = all_backgrounds.index(curr_bg) if curr_bg in all_backgrounds else 0
                background_val = st.selectbox("Antecedente Oficial (2024):", all_backgrounds, index=bg_idx)

            st.divider()

            # 2. ATRIBUTOS BASE & MODIFICADORES
            st.markdown("#### ⚔️ 2. Valores de Atributo")
            st.caption("O Bônus de Proficiência (PB) e os modificadores são calculados automaticamente.")
            abilities_current = form_data.get("abilities", {})
            col_a1, col_a2, col_a3, col_a4, col_a5, col_a6 = st.columns(6)
            with col_a1:
                str_val = st.number_input("FOR (Força):", min_value=1, max_value=30, value=int(abilities_current.get("str", 10)))
            with col_a2:
                dex_val = st.number_input("DES (Destreza):", min_value=1, max_value=30, value=int(abilities_current.get("dex", 10)))
            with col_a3:
                con_val = st.number_input("CON (Constituição):", min_value=1, max_value=30, value=int(abilities_current.get("con", 10)))
            with col_a4:
                int_val = st.number_input("INT (Inteligência):", min_value=1, max_value=30, value=int(abilities_current.get("int", 10)))
            with col_a5:
                wis_val = st.number_input("SAB (Sabedoria):", min_value=1, max_value=30, value=int(abilities_current.get("wis", 10)))
            with col_a6:
                cha_val = st.number_input("CAR (Carisma):", min_value=1, max_value=30, value=int(abilities_current.get("cha", 10)))

            st.divider()

            # 3. COMBATE & VITAIS
            st.markdown("#### 🛡️ 3. Combate & Defesas")
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            with col_c1:
                ac_val = st.number_input("Classe de Armadura (CA):", min_value=1, max_value=40, value=int(form_data.get("armor_class", 10)))
                speed_val = st.text_input("Deslocamento:", value=form_data.get("speed", "9m (30 ft)"))
            with col_c2:
                hp_max_val = st.number_input("PV Máximo:", min_value=1, max_value=1000, value=int(form_data.get("hit_points_max", 10)))
                hp_cur_val = st.number_input("PV Atual:", min_value=0, max_value=1000, value=int(form_data.get("hit_points_current", 10)))
            with col_c3:
                hp_tmp_val = st.number_input("PV Temporário:", min_value=0, max_value=500, value=int(form_data.get("hit_points_temp", 0)))
                default_hit_die = CLASSES_2024.get(class_val, {}).get("hit_die", "1d10")
                hit_dice_val = st.text_input("Dados de Vida:", value=form_data.get("hit_dice", default_hit_die))
            with col_c4:
                init_val = st.number_input("Bônus de Iniciativa:", min_value=-10, max_value=20, value=int(form_data.get("initiative_bonus", 0)))
                alignment_val = st.text_input("Alinhamento:", value=form_data.get("alignment", "Neutro e Bom"))

            st.divider()

            # 4. SALVAGUARDAS & PERÍCIAS
            st.markdown("#### 🎯 4. Salvaguardas & Perícias Proficientes")
            st.caption("Marque as salvaguardas e perícias em que o personagem possui proficiência (●):")
            
            saving_current = form_data.get("saving_throw_proficiencies", [])
            class_native_saves = CLASSES_2024.get(class_val, {}).get("saving_throws", [])
            
            col_s1, col_s2, col_s3, col_s4, col_s5, col_s6 = st.columns(6)
            with col_s1:
                save_str = st.checkbox("Salv. FOR", value=("str" in saving_current or "str" in class_native_saves))
            with col_s2:
                save_dex = st.checkbox("Salv. DES", value=("dex" in saving_current or "dex" in class_native_saves))
            with col_s3:
                save_con = st.checkbox("Salv. CON", value=("con" in saving_current or "con" in class_native_saves))
            with col_s4:
                save_int = st.checkbox("Salv. INT", value=("int" in saving_current or "int" in class_native_saves))
            with col_s5:
                save_wis = st.checkbox("Salv. SAB", value=("wis" in saving_current or "wis" in class_native_saves))
            with col_s6:
                save_cha = st.checkbox("Salv. CAR", value=("cha" in saving_current or "cha" in class_native_saves))

            skills_current = [s.lower() for s in form_data.get("skill_proficiencies", [])]
            col_sk1, col_sk2, col_sk3 = st.columns(3)
            selected_skills = []
            
            for idx, (sk_name, sk_key, sk_attr) in enumerate(SKILLS_LIST):
                col_target = col_sk1 if idx < 6 else (col_sk2 if idx < 12 else col_sk3)
                with col_target:
                    checked = st.checkbox(f"{sk_name} ({sk_attr})", value=(sk_key in skills_current or sk_name.lower() in skills_current), key=f"chk_sk_{sk_key}")
                    if checked:
                        selected_skills.append(sk_key)

            st.divider()

            # 5. ARMAS & ATAQUES COM MAESTRIA 2024
            st.markdown("#### 🗡️ 5. Ataques, Armas & Maestrias (2024)")
            attacks_current = form_data.get("attacks", [])
            
            # Seletor de Armas Rápidas do Catálogo Oficial
            weapon_catalog_options = get_weapons_list()
            selected_weapon_template = st.selectbox(
                "Adicionar Arma do Catálogo Oficial 2024 (com Maestria):",
                ["-- Escolha uma arma para carregar configurações --"] + weapon_catalog_options
            )
            
            attacks_json_str = json.dumps(attacks_current, ensure_ascii=False, indent=2)
            attacks_text = st.text_area(
                "Configuração de Ataques (Lista JSON):",
                value=attacks_json_str,
                help="Lista de armas contendo nome, bônus de ataque, dano, tipo de dano e maestria oficial de 2024."
            )
            
            col_eq1, col_eq2 = st.columns(2)
            with col_eq1:
                magic_items_options = get_magic_items_list()
                magic_items_text = st.text_area(
                    "Itens Mágicos & Sintonias (um por linha):",
                    value="\n".join(form_data.get("magic_items", [])),
                    help="Ex: Capa de Proteção (Sintonizado) (+1 CA e Salvaguardas)"
                )
            with col_eq2:
                equipment_text = st.text_area(
                    "Outros Equipamentos & Mochila:",
                    value=form_data.get("equipment", "")
                )

            st.divider()

            # 6. MAGIAS & GRIMÓRIO (OPCIONAL PARA CONJURADORES)
            st.markdown("#### 🔮 6. Conjuração de Magias & Grimório")
            sp_data = form_data.get("spellcasting", {})
            class_spell_attr = CLASSES_2024.get(class_val, {}).get("spell_ability", "None")
            
            col_sp1, col_sp2, col_sp3 = st.columns(3)
            with col_sp1:
                sp_ability_val = st.selectbox(
                    "Atributo de Conjuração:",
                    ["None", "int", "wis", "cha"],
                    index=["None", "int", "wis", "cha"].index(sp_data.get("ability", class_spell_attr)) if sp_data.get("ability", class_spell_attr) in ["None", "int", "wis", "cha"] else 0
                )
            with col_sp2:
                sp_dc_val = st.number_input("CD de Salvaguarda de Magia:", min_value=8, max_value=30, value=int(sp_data.get("save_dc", 10)))
            with col_sp3:
                sp_atk_val = st.text_input("Bônus de Ataque Mágico:", value=str(sp_data.get("attack_bonus", "+2")))

            # Seletores de Magias Oficiais
            spells_options = get_spells_list()
            col_sp_list1, col_sp_list2 = st.columns(2)
            with col_sp_list1:
                cantrips_text = st.text_area("Truques Conhecidos (um por linha):", value="\n".join(sp_data.get("cantrips", [])))
            with col_sp_list2:
                spells_text = st.text_area("Magias Conhecidas / Preparadas (uma por linha):", value="\n".join(sp_data.get("spells_known_or_prepared", [])))

            st.divider()

            # 7. TALENTOS & BIOGRAFIA
            st.markdown("#### 📜 7. Talentos Oficiais (2024) & Habilidades")
            features_val = st.text_area("Habilidades de Classe & Características Especiais:", value=form_data.get("features_and_traits", ""))
            feats_text = st.text_area("Talentos (um por linha):", value="\n".join(form_data.get("feats", [])))
            profs_lang_val = st.text_area("Proficiências & Idiomas:", value=form_data.get("proficiencies_languages", ""))

            # Botão de Submissão do Formulário
            submit_btn = st.form_submit_button("💾 **Salvar Ficha do Personagem**", type="primary", use_container_width=True)
            
            if submit_btn:
                new_saves = []
                if save_str: new_saves.append("str")
                if save_dex: new_saves.append("dex")
                if save_con: new_saves.append("con")
                if save_int: new_saves.append("int")
                if save_wis: new_saves.append("wis")
                if save_cha: new_saves.append("cha")

                try:
                    parsed_attacks = json.loads(attacks_text)
                    if not isinstance(parsed_attacks, list):
                        parsed_attacks = []
                except Exception:
                    parsed_attacks = [{"name": "Arma", "attack_bonus": "+0", "damage": "1d6", "damage_type": "Dano", "notes": ""}]

                parsed_magic_items = [i.strip() for i in magic_items_text.split("\n") if i.strip()]
                parsed_feats = [f.strip() for f in feats_text.split("\n") if f.strip()]
                parsed_cantrips = [c.strip() for c in cantrips_text.split("\n") if c.strip()]
                parsed_spells = [s.strip() for s in spells_text.split("\n") if s.strip()]

                updated_character = {
                    "id": editing_id,
                    "name": name_val.strip(),
                    "species": species_val.strip(),
                    "class_name": class_val.strip(),
                    "subclass": subclass_val.strip(),
                    "level": int(level_val),
                    "background": background_val.strip(),
                    "alignment": alignment_val.strip(),
                    "experience_points": form_data.get("experience_points", 0),
                    "abilities": {
                        "str": int(str_val),
                        "dex": int(dex_val),
                        "con": int(con_val),
                        "int": int(int_val),
                        "wis": int(wis_val),
                        "cha": int(cha_val)
                    },
                    "saving_throw_proficiencies": new_saves,
                    "armor_class": int(ac_val),
                    "initiative_bonus": int(init_val),
                    "speed": speed_val.strip(),
                    "hit_points_max": int(hp_max_val),
                    "hit_points_current": int(hp_cur_val),
                    "hit_points_temp": int(hp_tmp_val),
                    "hit_dice": hit_dice_val.strip(),
                    "death_saves": form_data.get("death_saves", {"successes": 0, "failures": 0}),
                    "skill_proficiencies": selected_skills,
                    "skill_expertises": form_data.get("skill_expertises", []),
                    "attacks": parsed_attacks,
                    "spellcasting": {
                        "ability": sp_ability_val,
                        "save_dc": int(sp_dc_val),
                        "attack_bonus": sp_atk_val.strip(),
                        "spell_slots": sp_data.get("spell_slots", {}),
                        "cantrips": parsed_cantrips,
                        "spells_known_or_prepared": parsed_spells
                    },
                    "equipment": equipment_text.strip(),
                    "magic_items": parsed_magic_items,
                    "currency": form_data.get("currency", {"cp": 0, "sp": 0, "ep": 0, "gp": 0, "pp": 0}),
                    "feats": parsed_feats,
                    "features_and_traits": features_val.strip(),
                    "proficiencies_languages": profs_lang_val.strip(),
                    "personality_traits": form_data.get("personality_traits", ""),
                    "ideals": form_data.get("ideals", ""),
                    "bonds": form_data.get("bonds", ""),
                    "flaws": form_data.get("flaws", ""),
                    "backstory": form_data.get("backstory", ""),
                    "notes": form_data.get("notes", ""),
                    "created_at": form_data.get("created_at", "")
                }

                saved_id = save_character(updated_character, username=username)
                set_active_character_id(saved_id, username=username)
                
                st.session_state["editing_character_id"] = ""
                st.session_state["character_form_data"] = None
                st.success(f"🎉 Personagem **{updated_character['name']}** salvo e ativado com sucesso!")
                st.rerun()
