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
    ALIGNMENTS_2024,
    EQUIPMENT_PACKS_2024,
    LANGUAGES_2024,
    PROFICIENCIES_ARMOR_WEAPONS,
    get_classes_list,
    get_subclasses_for_class,
    get_class_features_list,
    get_species_list,
    get_backgrounds_list,
    get_alignments_list,
    get_weapons_list,
    get_armor_list,
    get_cantrips_list,
    get_leveled_spells_list,
    is_spellcaster_class,
    get_class_default_spell_ability,
    get_background_details,
    get_species_details,
    get_feats_list,
    get_magic_items_list,
    get_equipment_packs_list,
    get_languages_list,
    get_armor_weapon_proficiencies_list
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
    Renderiza a Central de Heróis & Personagens D&D 2024 Reativa e Inteligente:
    - Validação Canônica D&D 2024 com Dropdowns Dependentes
    - Condicionamento Estrito de Subclasses, Magias, Habilidades e Talentos por Classe e Antecedente
    - Importação Inteligente Multimodal e Exportação em PDF
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
                
                with st.expander(f"🛡️ **{c['name']}** — *{c['class_name']} {c.get('subclass', '')} Nível {c['level']}* {' 🟢 [ATIVO NO CHAT]' if is_active else ''}", expanded=is_active):
                    col_info1, col_info2, col_info3 = st.columns(3)
                    with col_info1:
                        st.markdown(f"**Espécie:** {full_c.get('species', 'Aventureiro')}")
                        st.markdown(f"**Antecedente:** {full_c.get('background', 'Indefinido')}")
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
    # ABA 3: CRIAR OU EDITAR FICHA MANUALMENTE (REATIVO E CONDICIONAL D&D 2024)
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
                
        # 1. IDENTIFICAÇÃO BÁSICA COM REATIVIDADE INSTANTÂNEA
        st.markdown("#### 👤 1. Identificação & Origem")
        col_id1, col_id2, col_id3 = st.columns(3)
        with col_id1:
            name_val = st.text_input("Nome do Personagem:", value=form_data.get("name", ""), placeholder="Ex: Eladrin Arcanista")
            
            # Espécies 2024
            all_species = ["-- Selecione uma Espécie --"] + get_species_list()
            curr_species = form_data.get("species", "")
            species_idx = all_species.index(curr_species) if curr_species in all_species else 0
            species_selected = st.selectbox("Espécie / Raça Oficial (2024):", all_species, index=species_idx)
            species_val = species_selected if species_selected != "-- Selecione uma Espécie --" else ""

            if species_val:
                sp_info = get_species_details(species_val)
                st.caption(f"🧬 **Traços:** {sp_info.get('traits', '')}")

        with col_id2:
            # Classes 2024
            all_classes = ["-- Selecione uma Classe --"] + get_classes_list()
            curr_class = form_data.get("class_name", "")
            class_idx = all_classes.index(curr_class) if curr_class in all_classes else 0
            class_selected = st.selectbox("Classe Principal (2024):", all_classes, index=class_idx)
            class_val = class_selected if class_selected != "-- Selecione uma Classe --" else ""
            
            # Subclasses Dependentes e Condicionadas à Classe
            if not class_val:
                st.selectbox("Subclasse Oficial (2024):", ["Selecione uma classe primeiro..."], disabled=True)
                subclass_val = ""
            else:
                available_subclasses = ["Nenhuma / A Escolher"] + get_subclasses_for_class(class_val)
                curr_subclass = form_data.get("subclass", "")
                subclass_idx = available_subclasses.index(curr_subclass) if curr_subclass in available_subclasses else 0
                subclass_selected = st.selectbox(f"Subclasse de {class_val} (2024):", available_subclasses, index=subclass_idx)
                subclass_val = subclass_selected if subclass_selected != "Nenhuma / A Escolher" else ""

        with col_id3:
            level_val = st.number_input("Nível do Personagem:", min_value=1, max_value=20, value=int(form_data.get("level", 1)))
            
            # Antecedentes 2024
            all_backgrounds = ["-- Selecione um Antecedente --"] + get_backgrounds_list()
            curr_bg = form_data.get("background", "")
            bg_idx = all_backgrounds.index(curr_bg) if curr_bg in all_backgrounds else 0
            bg_selected = st.selectbox("Antecedente Oficial (2024):", all_backgrounds, index=bg_idx)
            background_val = bg_selected if bg_selected != "-- Selecione um Antecedente --" else ""

            if background_val:
                bg_info = get_background_details(background_val)
                st.caption(f"📜 **Talento de Origem:** `{bg_info.get('feat', '')}` | **Atributos:** `{bg_info.get('attributes', '')}`")

            # Alinhamento / Tendência Oficial
            all_alignments = ["-- Selecione um Alinhamento --"] + get_alignments_list()
            curr_align = form_data.get("alignment", "")
            align_idx = all_alignments.index(curr_align) if curr_align in all_alignments else 0
            align_selected = st.selectbox("Alinhamento / Tendência:", all_alignments, index=align_idx)
            alignment_val = align_selected if align_selected != "-- Selecione um Alinhamento --" else ""

        st.divider()

        # 2. ATRIBUTOS BASE & MODIFICADORES
        st.markdown("#### ⚔️ 2. Valores de Atributo")
        pb_calc = 2 + (max(1, int(level_val)) - 1) // 4
        st.caption(f"Bônus de Proficiência Calculado: **+{pb_calc}** (Nível {level_val})")
        abilities_current = form_data.get("abilities", {})
        col_a1, col_a2, col_a3, col_a4, col_a5, col_a6 = st.columns(6)
        with col_a1:
            str_val = st.number_input("FOR (Força):", min_value=1, max_value=30, value=int(abilities_current.get("str", 10)))
            st.caption(f"Mod: `{'+' if (str_val-10)//2 >= 0 else ''}{(str_val-10)//2}`")
        with col_a2:
            dex_val = st.number_input("DES (Destreza):", min_value=1, max_value=30, value=int(abilities_current.get("dex", 10)))
            st.caption(f"Mod: `{'+' if (dex_val-10)//2 >= 0 else ''}{(dex_val-10)//2}`")
        with col_a3:
            con_val = st.number_input("CON (Constituição):", min_value=1, max_value=30, value=int(abilities_current.get("con", 10)))
            st.caption(f"Mod: `{'+' if (con_val-10)//2 >= 0 else ''}{(con_val-10)//2}`")
        with col_a4:
            int_val = st.number_input("INT (Inteligência):", min_value=1, max_value=30, value=int(abilities_current.get("int", 10)))
            st.caption(f"Mod: `{'+' if (int_val-10)//2 >= 0 else ''}{(int_val-10)//2}`")
        with col_a5:
            wis_val = st.number_input("SAB (Sabedoria):", min_value=1, max_value=30, value=int(abilities_current.get("wis", 10)))
            st.caption(f"Mod: `{'+' if (wis_val-10)//2 >= 0 else ''}{(wis_val-10)//2}`")
        with col_a6:
            cha_val = st.number_input("CAR (Carisma):", min_value=1, max_value=30, value=int(abilities_current.get("cha", 10)))
            st.caption(f"Mod: `{'+' if (cha_val-10)//2 >= 0 else ''}{(cha_val-10)//2}`")

        st.divider()

        # 3. COMBATE & VITAIS
        st.markdown("#### 🛡️ 3. Combate & Defesas")
        col_c1, col_c2, col_c3, col_c4 = st.columns(4)
        with col_c1:
            ac_val = st.number_input("Classe de Armadura (CA):", min_value=1, max_value=40, value=int(form_data.get("armor_class", 10)))
            default_speed = SPECIES_2024.get(species_val, {}).get("speed", "9m (30 ft)") if species_val else "9m (30 ft)"
            speed_val = st.text_input("Deslocamento:", value=form_data.get("speed", default_speed))
        with col_c2:
            hp_max_val = st.number_input("PV Máximo:", min_value=1, max_value=1000, value=int(form_data.get("hit_points_max", 10)))
            hp_cur_val = st.number_input("PV Atual:", min_value=0, max_value=1000, value=int(form_data.get("hit_points_current", 10)))
        with col_c3:
            hp_tmp_val = st.number_input("PV Temporário:", min_value=0, max_value=500, value=int(form_data.get("hit_points_temp", 0)))
            default_hit_die = CLASSES_2024.get(class_val, {}).get("hit_die", "1d8") if class_val else "1d8"
            hit_dice_val = st.text_input("Dados de Vida:", value=form_data.get("hit_dice", default_hit_die), placeholder="Ex: 1d10, 1d8, 1d6")
        with col_c4:
            init_val = st.number_input("Bônus de Iniciativa:", min_value=-10, max_value=20, value=int(form_data.get("initiative_bonus", 0)))
            xp_val = st.number_input("Pontos de Experiência (XP):", min_value=0, max_value=1000000, value=int(form_data.get("experience_points", 0)))

        st.divider()

        # 4. SALVAGUARDAS & PERÍCIAS
        st.markdown("#### 🎯 4. Salvaguardas & Perícias Proficientes")
        native_saves = CLASSES_2024.get(class_val, {}).get("saving_throws", []) if class_val else []
        if native_saves:
            st.caption(f"💡 **Salvaguardas Nativas de {class_val}:** `{', '.join(s.upper() for s in native_saves)}`")
        
        saving_current = form_data.get("saving_throw_proficiencies", [])
        
        col_s1, col_s2, col_s3, col_s4, col_s5, col_s6 = st.columns(6)
        with col_s1:
            save_str = st.checkbox("Salv. FOR" + (" ⭐" if "str" in native_saves else ""), value=("str" in saving_current))
        with col_s2:
            save_dex = st.checkbox("Salv. DES" + (" ⭐" if "dex" in native_saves else ""), value=("dex" in saving_current))
        with col_s3:
            save_con = st.checkbox("Salv. CON" + (" ⭐" if "con" in native_saves else ""), value=("con" in saving_current))
        with col_s4:
            save_int = st.checkbox("Salv. INT" + (" ⭐" if "int" in native_saves else ""), value=("int" in saving_current))
        with col_s5:
            save_wis = st.checkbox("Salv. SAB" + (" ⭐" if "wis" in native_saves else ""), value=("wis" in saving_current))
        with col_s6:
            save_cha = st.checkbox("Salv. CAR" + (" ⭐" if "cha" in native_saves else ""), value=("cha" in saving_current))

        # Perícias Sugeridas pelo Antecedente
        bg_skills = BACKGROUNDS_2024.get(background_val, {}).get("skills", []) if background_val else []
        if bg_skills:
            st.caption(f"💡 **Perícias do Antecedente {background_val}:** `{', '.join(s.capitalize() for s in bg_skills)}`")

        skills_current = [s.lower() for s in form_data.get("skill_proficiencies", [])]
        col_sk1, col_sk2, col_sk3 = st.columns(3)
        selected_skills = []
        
        for idx, (sk_name, sk_key, sk_attr) in enumerate(SKILLS_LIST):
            col_target = col_sk1 if idx < 6 else (col_sk2 if idx < 12 else col_sk3)
            with col_target:
                is_bg_skill = (sk_key in bg_skills)
                checked = st.checkbox(f"{sk_name} ({sk_attr})" + (" 📜" if is_bg_skill else ""), value=(sk_key in skills_current or sk_name.lower() in skills_current), key=f"chk_sk_{sk_key}")
                if checked:
                    selected_skills.append(sk_key)

        st.divider()

        # 5. ARMAS & ATAQUES COM MAESTRIA 2024
        st.markdown("#### 🗡️ 5. Ataques, Armas & Maestrias (2024)")
        if class_val:
            wm_count = CLASSES_2024.get(class_val, {}).get("weapon_mastery_count", 0)
            if wm_count > 0:
                st.info(f"⚔️ **{class_val} (2024)** possui proficiência em **{wm_count} Maestrias de Arma** (*Weapon Mastery*)!")
        
        attacks_current = form_data.get("attacks", [])
        attacks_json_str = json.dumps(attacks_current, ensure_ascii=False, indent=2)
        
        attacks_text = st.text_area(
            "Configuração de Ataques (Lista JSON de armas):",
            value=attacks_json_str,
            placeholder="Exemplo:\n[\n  {\n    \"name\": \"Espada Longa\",\n    \"attack_bonus\": \"+5\",\n    \"damage\": \"1d8+3\",\n    \"damage_type\": \"Cortante\",\n    \"mastery\": \"Empurrão (Push)\"\n  }\n]",
            help="Lista de armas contendo nome, bônus de ataque, dano, tipo de dano e maestria oficial de 2024."
        )

        st.divider()

        # 6. ITENS MÁGICOS, SINTONIAS & MOCHILA
        st.markdown("#### 🎒 6. Itens Mágicos, Sintonias & Equipamento")
        col_item1, col_item2 = st.columns(2)
        with col_item1:
            all_magic_items_preset = get_magic_items_list()
            curr_items = form_data.get("magic_items", [])
            def_items = [p for p in all_magic_items_preset if any(item.lower() in p.lower() for item in curr_items)]
            selected_magic_items = st.multiselect(
                "Itens Mágicos Canônicos (D&D 2024):",
                options=all_magic_items_preset,
                default=def_items
            )
            magic_items_custom = st.text_area(
                "Outros Itens Mágicos / Customizados (um por linha):",
                value="\n".join([i for i in curr_items if not any(i.lower() in p.lower() for p in all_magic_items_preset)]),
                placeholder="Ex: Anel de Resistência a Fogo"
            )

        with col_item2:
            all_packs = get_equipment_packs_list()
            curr_equip = form_data.get("equipment", "")
            def_packs = [p for p in all_packs if curr_equip and (p in curr_equip or p.split(" (")[0] in curr_equip)]
            selected_packs = st.multiselect(
                "Pacotes de Aventureiro & Kits Pré-definidos:",
                options=all_packs,
                default=def_packs
            )
            equipment_custom = st.text_area(
                "Outros Equipamentos Avulsos na Mochila:",
                value=curr_equip,
                placeholder="Ex: 50m de corda de seda, 2 tochas, 1 cantil..."
            )

        # Moedas
        st.markdown("**💰 Moedas & Tesouro:**")
        curr = form_data.get("currency", {"cp": 0, "sp": 0, "ep": 0, "gp": 0, "pp": 0})
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        with col_m1: cp_val = st.number_input("PC (Cobre):", min_value=0, value=int(curr.get("cp", 0)))
        with col_m2: sp_val = st.number_input("PP (Prata):", min_value=0, value=int(curr.get("sp", 0)))
        with col_m3: ep_val = st.number_input("PE (Electrum):", min_value=0, value=int(curr.get("ep", 0)))
        with col_m4: gp_val = st.number_input("PO (Ouro):", min_value=0, value=int(curr.get("gp", 0)))
        with col_m5: pp_val = st.number_input("PL (Platina):", min_value=0, value=int(curr.get("pp", 0)))

        st.divider()

        # 7. MAGIAS & GRIMÓRIO (CONDICIONADO RIGOROSAMENTE À CLASSE)
        st.markdown("#### 🔮 7. Conjuração de Magias & Grimório")
        is_caster = is_spellcaster_class(class_val, subclass_val)
        
        if not is_caster:
            st.info(
                f"🛡️ **{class_val or 'Esta classe'} não é uma conjuradora nativa.** "
                "(A menos que possua truques raciais, talentos ou uma subclasse mágica como Cavaleiro Arcano)."
            )
            with st.expander("✨ Expandir Grimório para Magias de Raça ou Talentos"):
                sp_data = form_data.get("spellcasting", {})
                col_sp1, col_sp2, col_sp3 = st.columns(3)
                with col_sp1:
                    sp_ability_val = st.selectbox("Atributo de Conjuração:", ["None", "int", "wis", "cha"], index=0, key="sp_ability_non_caster")
                with col_sp2:
                    sp_dc_val = st.number_input("CD de Magia:", min_value=8, max_value=30, value=int(sp_data.get("save_dc", 10)), key="sp_dc_non_caster")
                with col_sp3:
                    sp_atk_val = st.text_input("Bônus de Ataque Mágico:", value=str(sp_data.get("attack_bonus", "+0")), key="sp_atk_non_caster")

                all_cantrips_preset = get_cantrips_list()
                all_leveled_spells_preset = get_leveled_spells_list()
                curr_cantrips = sp_data.get("cantrips", [])
                def_cantrips = [c for c in all_cantrips_preset if any(c_name.lower() in c.lower() for c_name in curr_cantrips)]
                selected_cantrips = st.multiselect("Truques Conhecidos:", options=all_cantrips_preset, default=def_cantrips, key="sp_cantrips_non_caster")
                custom_cantrips = st.text_area("Truques Extras:", value="\n".join([c for c in curr_cantrips if not any(c.lower() in p.lower() for p in all_cantrips_preset)]), key="sp_custom_c_non_caster")

                curr_spells = sp_data.get("spells_known_or_prepared", [])
                def_spells = [s for s in all_leveled_spells_preset if any(s_name.lower() in s.lower() for s_name in curr_spells)]
                selected_spells = st.multiselect("Magias Preparadas:", options=all_leveled_spells_preset, default=def_spells, key="sp_spells_non_caster")
                custom_spells = st.text_area("Magias Extras:", value="\n".join([s for s in curr_spells if not any(s.lower() in p.lower() for p in all_leveled_spells_preset)]), key="sp_custom_s_non_caster")
        else:
            sp_data = form_data.get("spellcasting", {})
            class_spell_attr = get_class_default_spell_ability(class_val)
            
            col_sp1, col_sp2, col_sp3 = st.columns(3)
            with col_sp1:
                spell_attr_opts = ["int", "wis", "cha", "None"]
                attr_default_idx = spell_attr_opts.index(class_spell_attr) if class_spell_attr in spell_attr_opts else 0
                sp_ability_val = st.selectbox(
                    f"Atributo de Conjuração ({class_val}):",
                    spell_attr_opts,
                    index=attr_default_idx
                )
            with col_sp2:
                # Calcular CD com base no atributo
                attr_mod = 0
                if sp_ability_val == "int": attr_mod = (int_val - 10) // 2
                elif sp_ability_val == "wis": attr_mod = (wis_val - 10) // 2
                elif sp_ability_val == "cha": attr_mod = (cha_val - 10) // 2
                suggested_dc = 8 + pb_calc + attr_mod
                sp_dc_val = st.number_input("CD de Salvaguarda de Magia:", min_value=8, max_value=30, value=int(sp_data.get("save_dc", suggested_dc)))
            with col_sp3:
                suggested_atk = f"+{pb_calc + attr_mod}"
                sp_atk_val = st.text_input("Bônus de Ataque Mágico:", value=str(sp_data.get("attack_bonus", suggested_atk)))

            # Filtrar Magias Específicas da Classe
            class_cantrips_preset = get_cantrips_list(class_filter=class_val)
            class_spells_preset = get_leveled_spells_list(class_filter=class_val)
            
            col_sp_list1, col_sp_list2 = st.columns(2)
            with col_sp_list1:
                curr_cantrips = sp_data.get("cantrips", [])
                def_cantrips = [c for c in class_cantrips_preset if any(c_name.lower() in c.lower() for c_name in curr_cantrips)]
                selected_cantrips = st.multiselect(
                    f"Truques Oficiais de {class_val} (Nível 0):",
                    options=class_cantrips_preset,
                    default=def_cantrips
                )
                custom_cantrips = st.text_area("Truques Customizados (um por linha):", value="\n".join([c for c in curr_cantrips if not any(c.lower() in p.lower() for p in class_cantrips_preset)]), placeholder="Ex: Rajada de Luz")
                
            with col_sp_list2:
                curr_spells = sp_data.get("spells_known_or_prepared", [])
                def_spells = [s for s in class_spells_preset if any(s_name.lower() in s.lower() for s_name in curr_spells)]
                selected_spells = st.multiselect(
                    f"Magias Oficiais de {class_val} (1º ao 9º Círculo):",
                    options=class_spells_preset,
                    default=def_spells
                )
                custom_spells = st.text_area("Magias Customizadas (uma por linha):", value="\n".join([s for s in curr_spells if not any(s.lower() in p.lower() for p in class_spells_preset)]), placeholder="Ex: Magia Customizada")

        st.divider()

        # 8. HABILIDADES DE CLASSE, TALENTOS & PROFICIÊNCIAS (CONDICIONAMENTO ESTRITO)
        st.markdown("#### 📜 8. Habilidades de Classe, Talentos & Idiomas")
        
        # Habilidades Condicionadas à Classe Selecionada
        if not class_val:
            st.info("ℹ️ Selecione uma classe no topo da página para carregar suas habilidades oficiais.")
            selected_features = []
            custom_features = st.text_area("Características Especiais / Traços:", value=form_data.get("features_and_traits", ""), placeholder="Traços do personagem...")
        else:
            class_features_preset = get_class_features_list(class_val)
            curr_features_str = form_data.get("features_and_traits", "")
            def_features = [f for f in class_features_preset if curr_features_str and f.split("(")[0].strip().lower() in curr_features_str.lower()]
            selected_features = st.multiselect(
                f"Habilidades Oficiais de {class_val} (D&D 2024):",
                options=class_features_preset,
                default=def_features
            )
            custom_features = st.text_area(f"Outras Características Especiais de {class_val} / Subclasse:", value=curr_features_str, placeholder="Ex: Características raciais, habilidades de subclasse ou poderes...")

        col_ft1, col_ft2 = st.columns(2)
        with col_ft1:
            # Talentos Oficiais 2024
            all_feats_preset = get_feats_list()
            curr_feats = form_data.get("feats", [])
            
            # Se antecedente selecionado, auto-sugerir o talento de origem
            bg_feat_name = BACKGROUNDS_2024.get(background_val, {}).get("feat", "") if background_val else ""
            def_feats = [f for f in all_feats_preset if any(f_name.lower() in f.lower() for f_name in curr_feats) or (bg_feat_name and bg_feat_name.lower() in f.lower())]
            
            selected_feats = st.multiselect(
                "Talentos Oficiais D&D 2024 (Origem & Gerais):",
                options=all_feats_preset,
                default=def_feats
            )
            custom_feats = st.text_area("Outros Talentos (um por linha):", value="\n".join([f for f in curr_feats if not any(f.lower() in p.lower() for p in all_feats_preset)]), placeholder="Ex: Talento Customizado")

        with col_ft2:
            # Idiomas Oficiais
            all_languages_preset = get_languages_list()
            curr_lang_str = form_data.get("proficiencies_languages", "")
            def_langs = [l for l in all_languages_preset if curr_lang_str and any(l.split(" (")[0].lower() in part.lower() for part in curr_lang_str.split("|"))]
                
            selected_languages = st.multiselect(
                "Idiomas Falados e Escritos:",
                options=all_languages_preset,
                default=def_langs
            )
            
            # Proficiências de Armas & Armaduras
            all_profs_preset = get_armor_weapon_proficiencies_list()
            def_profs = [p for p in all_profs_preset if curr_lang_str and any(p.split(" (")[0].lower() in part.lower() for part in curr_lang_str.split("|"))]
            selected_profs = st.multiselect(
                "Proficiências de Armas e Armaduras:",
                options=all_profs_preset,
                default=def_profs
            )

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botão de Salvamento
        if st.button("💾 **Salvar Ficha do Personagem**", type="primary", use_container_width=True, key="btn_save_character_reactive"):
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

            # Consolidar Itens Mágicos
            merged_magic_items = list(selected_magic_items) + [i.strip() for i in magic_items_custom.split("\n") if i.strip()]
            
            # Consolidar Equipamentos
            merged_equip = ", ".join(selected_packs)
            if equipment_custom.strip():
                merged_equip = f"{merged_equip} | {equipment_custom.strip()}" if merged_equip else equipment_custom.strip()

            # Consolidar Magias
            merged_cantrips = [c.split(" (")[0] for c in selected_cantrips] + [c.strip() for c in custom_cantrips.split("\n") if c.strip()]
            merged_spells = [s.split(" (")[0] for s in selected_spells] + [s.strip() for s in custom_spells.split("\n") if s.strip()]

            # Consolidar Talentos
            merged_feats = list(selected_feats) + [f.strip() for f in custom_feats.split("\n") if f.strip()]

            # Consolidar Habilidades
            merged_features = ", ".join(selected_features)
            if custom_features.strip():
                merged_features = f"{merged_features}\n{custom_features.strip()}" if merged_features else custom_features.strip()

            # Consolidar Proficiências e Idiomas
            lang_str = f"Idiomas: {', '.join(selected_languages)}"
            prof_str = f"Proficiências: {', '.join(selected_profs)}"
            merged_profs_lang = f"{prof_str} | {lang_str}"

            char_name_final = name_val.strip() or "Aventureiro Sem Nome"
            updated_character = {
                "id": editing_id,
                "name": char_name_final,
                "species": species_val.strip(),
                "class_name": class_val.strip(),
                "subclass": subclass_val.strip(),
                "level": int(level_val),
                "background": background_val.strip(),
                "alignment": alignment_val.strip(),
                "experience_points": int(xp_val),
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
                    "cantrips": merged_cantrips,
                    "spells_known_or_prepared": merged_spells
                },
                "equipment": merged_equip,
                "magic_items": merged_magic_items,
                "currency": {"cp": int(cp_val), "sp": int(sp_val), "ep": int(ep_val), "gp": int(gp_val), "pp": int(pp_val)},
                "feats": merged_feats,
                "features_and_traits": merged_features,
                "proficiencies_languages": merged_profs_lang,
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
