import os
import json
import re
from typing import Dict, Any, Optional, List, Union
from PIL import Image
import io

from ..rag.vector_store import DnDKnowledgeBase
from .character_calc import calculate_ability_modifier, calculate_proficiency_bonus

CLASS_CANONICAL_DATA = {
    "barbaro": {"saves": ["Força", "Constituição"], "hit_die": "d12", "spell_attr": None, "page_ref": "Cap. 3: Classes > Bárbaro (Pág. 51)"},
    "bardo": {"saves": ["Destreza", "Carisma"], "hit_die": "d8", "spell_attr": "Carisma", "page_ref": "Cap. 3: Classes > Bardo (Pág. 59)"},
    "bruxo": {"saves": ["Sabedoria", "Carisma"], "hit_die": "d8", "spell_attr": "Carisma", "page_ref": "Cap. 3: Classes > Bruxo (Pág. 69)"},
    "clerigo": {"saves": ["Sabedoria", "Carisma"], "hit_die": "d8", "spell_attr": "Sabedoria", "page_ref": "Cap. 3: Classes > Clérigo (Pág. 81)"},
    "druida": {"saves": ["Inteligência", "Sabedoria"], "hit_die": "d8", "spell_attr": "Sabedoria", "page_ref": "Cap. 3: Classes > Druida (Pág. 91)"},
    "feiticeiro": {"saves": ["Constituição", "Carisma"], "hit_die": "d6", "spell_attr": "Carisma", "page_ref": "Cap. 3: Classes > Feiticeiro (Pág. 103)"},
    "guardiao": {"saves": ["Força", "Destreza"], "hit_die": "d10", "spell_attr": "Sabedoria", "page_ref": "Cap. 3: Classes > Guardião (Pág. 117)"},
    "patrulheiro": {"saves": ["Força", "Destreza"], "hit_die": "d10", "spell_attr": "Sabedoria", "page_ref": "Cap. 3: Classes > Guardião (Pág. 117)"},
    "guerreiro": {"saves": ["Força", "Constituição"], "hit_die": "d10", "spell_attr": None, "page_ref": "Cap. 3: Classes > Guerreiro (Pág. 127)"},
    "ladino": {"saves": ["Destreza", "Inteligência"], "hit_die": "d8", "spell_attr": None, "page_ref": "Cap. 3: Classes > Ladino (Pág. 137)"},
    "mago": {"saves": ["Inteligência", "Sabedoria"], "hit_die": "d6", "spell_attr": "Inteligência", "page_ref": "Cap. 3: Classes > Mago (Pág. 147)"},
    "monge": {"saves": ["Força", "Destreza"], "hit_die": "d8", "spell_attr": None, "page_ref": "Cap. 3: Classes > Monge (Pág. 159)"},
    "paladino": {"saves": ["Sabedoria", "Carisma"], "hit_die": "d10", "spell_attr": "Carisma", "page_ref": "Cap. 3: Classes > Paladino (Pág. 167)"},
    "artifice": {"saves": ["Constituição", "Inteligência"], "hit_die": "d8", "spell_attr": "Inteligência", "page_ref": "Cap. 3: Classes > Artífice"}
}

EXTRACTION_PROMPT = """Você é um especialista em OCR e análise estruturada de fichas de RPG Dungeons & Dragons.
Examine cuidadosamente o documento / foto fornecido e extraia todos os dados visíveis no formato JSON estrito:

{
  "character_name": "Nome completo do personagem",
  "species_race": "Espécie ou Raça",
  "class_name": "Classe principal (ex: Guerreiro, Ladino, Mago)",
  "subclass_name": "Subclasse (se houver, ex: Campeão, Assassino)",
  "level": 1,
  "background": "Antecedente (ex: Soldado, Acólito)",
  "attributes": {
    "FOR": {"score": 10, "written_mod": "+0"},
    "DES": {"score": 10, "written_mod": "+0"},
    "CON": {"score": 10, "written_mod": "+0"},
    "INT": {"score": 10, "written_mod": "+0"},
    "SAB": {"score": 10, "written_mod": "+0"},
    "CAR": {"score": 10, "written_mod": "+0"}
  },
  "proficiency_bonus_written": "+2",
  "saving_throws_marked": ["FOR", "CON"],
  "saving_throws_written_values": {"FOR": "+2", "DES": "+0", "CON": "+2", "INT": "+0", "SAB": "+0", "CAR": "+0"},
  "skills_marked": ["Atletismo", "Percepção"],
  "skills_written_values": {"Atletismo": "+2"},
  "armor_class_written": 10,
  "hit_points_max_written": 10,
  "passive_perception_written": 10,
  "equipped_armor": "Nome da armadura e escudo",
  "weapons_attacks": [{"name": "Espada", "attack_bonus": "+4", "damage": "1d8+2"}],
  "magic_items": ["Itens mágicos e sintonias"],
  "feats_and_traits": ["Talentos e habilidades especiais anotadas"]
}

Retorne APENAS o bloco JSON válido, sem texto adicional.
"""

STRICT_SYNTHESIS_PROMPT = """Você é o **Auditor Mestre Oficial de Fichas de D&D 5e e 2024**.
Sua missão é gerar um relatório de auditoria 100% EXATO, DETERMINÍSTICO, SEM ALUCINAÇÕES e CITANDO AS PÁGINAS E REGRAS EXATAS FORNECIDAS ABAIXO.

### REGRAS FUNDAMENTAIS:
1. Baseie-se rigorosamente nos **Dados Verificados por Código** e nos **Trechos de Livros Oficiais Recuperados pelo RAG** fornecidos abaixo.
2. Em cada seção e cada correção, você DEVE citar a fonte e a página exata informada nos trechos recuperados.
3. Se houver divergências matemáticas ou de regras, explique o erro com a fórmula oficial e informe a correção exata.

---

Gere o relatório exatamente nesta estrutura Markdown:

# 📋 Relatório de Auditoria da Ficha: [Nome do Personagem]

### 🧙‍♂️ 1. Identificação do Personagem
- **Nome:** [Nome]
- **Espécie / Raça:** [Raça] *(Fonte: [Citação do Livro e Página])*
- **Classe e Subclasse:** [Classe] ([Subclasse]) - Nível [Nível] *(Fonte: [Citação do Livro e Página])*
- **Antecedente:** [Antecedente] *(Fonte: [Citação do Livro e Página])*
- **Bônus de Proficiência:** +[X] *(Status: [✅ Correto / ❌ Incorreto] para Nível [X] | Fonte: Livro do Jogador 2024, Cap. 1, pág. 13)*

---

### 📊 2. Matriz de Auditoria de Atributos (Checklist Obrigatório)
| Atributo | Valor Ficha | Mod. na Ficha | Mod. Correto pela Regra | Status | Fonte Oficial |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **FOR** (Força) | [Val] | [Mod Ficha] | [Mod Correto] | [✅ Correto / ❌ Incorreto] | *Livro do Jogador 2024, Cap. 1, pág. 15* |
| **DES** (Destreza) | [Val] | [Mod Ficha] | [Mod Correto] | [✅ Correto / ❌ Incorreto] | *Livro do Jogador 2024, Cap. 1, pág. 15* |
| **CON** (Constituição) | [Val] | [Mod Ficha] | [Mod Correto] | [✅ Correto / ❌ Incorreto] | *Livro do Jogador 2024, Cap. 1, pág. 15* |
| **INT** (Inteligência) | [Val] | [Mod Ficha] | [Mod Correto] | [✅ Correto / ❌ Incorreto] | *Livro do Jogador 2024, Cap. 1, pág. 15* |
| **SAB** (Sabedoria) | [Val] | [Mod Ficha] | [Mod Correto] | [✅ Correto / ❌ Incorreto] | *Livro do Jogador 2024, Cap. 1, pág. 15* |
| **CAR** (Carisma) | [Val] | [Mod Ficha] | [Mod Correto] | [✅ Correto / ❌ Incorreto] | *Livro do Jogador 2024, Cap. 1, pág. 15* |

---

### 🛡️ 3. Auditoria de Salvaguardas & Perícias
- **Salvaguardas Oficiais da Classe:** [Salvaguarda 1] e [Salvaguarda 2] *(Fonte: [Citação do Livro e Página])*
- **Itens / Efeitos Ativos:** [Ex: Capa de Proteção, etc. se houver]
- **Status das Salvaguardas:** [Detalhamento de cada salvaguarda com a soma `Mod + Prof + Bônus de Itens`]
- **Perícias Marcadas:** [Verificação matemática de cada perícia: `Mod + Prof (+ Prof se Expertise)`]
- **Percepção Passiva:** Anotado [X] | Correto: `10 + Mod SAB (+ Prof se proficiente)` = **[Y]** *(Fonte: Livro do Jogador 2024, Cap. 1, pág. 10)*

---

### ⚔️ 4. Combate, Defesas, Vida & Armas
- **Classe de Armadura (CA):** Anotado [X] | Cálculo Oficial: [Equipamento + Mod DES + Escudo + Itens] = **[Y]** *(Fonte: Livro do Jogador 2024, Cap. 6, pág. 219)*
- **Pontos de Vida (PV Máximo):** Anotado [X] | Estimativa Oficial: [Dado de Vida + CON por nível] *(Fonte: Livro do Jogador 2024, Cap. 1, pág. 27)*
- **Ataques com Armas:** [Verificação do Bônus de Ataque `Mod + Prof + Mágico` e Dano `Dado + Mod`]

---

### 🔮 5. Magias e Conjuração *(se aplicável)*
- **Atributo de Conjuração:** [Atributo]
- **CD de Salvaguarda de Magia:** `8 + Prof + Mod` = **[Valor]** *(Fonte: Livro do Jogador 2024, Cap. 7, pág. 236)*
- **Bônus de Ataque Mágico:** `Prof + Mod` = **[Valor]** *(Fonte: Livro do Jogador 2024, Cap. 7, pág. 236)*

---

### ⚠️ 6. Inconsistências Encontradas & Correções Exatas
*(Liste de forma clara cada divergência com a explicação matemática, regra e valor corrigido. Se não houver divergências, afirme que a ficha está 100% correta).*

---

### 💡 7. Lembretes Oficiais, Talentos & Habilidades da Classe
*(Liste as habilidades chave da classe para o nível do personagem e talentos do antecedente com as referências dos livros).*
"""

STRICT_AUDITOR_SYSTEM_PROMPT = STRICT_SYNTHESIS_PROMPT
SHEET_AUDITOR_PROMPT = STRICT_SYNTHESIS_PROMPT

class SheetValidator:
    """Validador de fichas com arquitetura em dois passos (Visão + RAG + Verificação Determinística)."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.6-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        self.kb = DnDKnowledgeBase()
        self._init_client()

    def _init_client(self):
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Erro ao inicializar cliente para validação de ficha: {e}")

    def update_config(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        if api_key is not None:
            self.api_key = api_key
            self._init_client()
        if model_name is not None:
            self.model_name = model_name

    def validate_sheet_file(self, file_bytes: bytes, filename: str, mime_type: str, notes: str = "") -> Dict[str, Any]:
        """
        Analisa e valida uma ficha combinando extração visual, RAG de regras dos livros e validação matemática.
        """
        if not self.client:
            return {
                "success": False,
                "report": (
                    "⚠️ **Chave de API do Gemini não configurada.**\n\n"
                    "Por favor insira sua `GEMINI_API_KEY` na barra lateral à esquerda para realizar a auditoria de fichas."
                ),
                "extracted_data": {}
            }

        try:
            from google.genai import types

            # 1. Determinar tipo MIME
            ext = os.path.splitext(filename)[1].lower()
            if ext == ".pdf":
                inferred_mime = "application/pdf"
            elif ext in [".jpg", ".jpeg"]:
                inferred_mime = "image/jpeg"
            elif ext == ".png":
                inferred_mime = "image/png"
            elif ext == ".webp":
                inferred_mime = "image/webp"
            else:
                inferred_mime = mime_type or "application/octet-stream"

            file_part = types.Part.from_bytes(data=file_bytes, mime_type=inferred_mime)

            # PASSO 1: Extração estruturada com Visão do Gemini
            extract_prompt = EXTRACTION_PROMPT
            if notes.strip():
                extract_prompt += f"\n\nObservações extras: {notes}"

            extract_resp = self.client.models.generate_content(
                model=self.model_name,
                contents=[file_part, extract_prompt],
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    top_p=1.0
                )
            )

            raw_json = extract_resp.text or "{}"
            json_match = re.search(r'\{.*\}', raw_json, re.DOTALL)
            extracted_data = {}
            if json_match:
                try:
                    extracted_data = json.loads(json_match.group(0))
                except Exception:
                    extracted_data = {}

            # PASSO 2: Verificação Matemática Determinística em Python
            char_class = (extracted_data.get("class_name") or "Guerreiro").lower().strip()
            char_level = int(extracted_data.get("level") or 1)
            char_species = extracted_data.get("species_race") or "Humano"
            char_bg = extracted_data.get("background") or "Soldado"

            math_verification = {}
            raw_attrs = extracted_data.get("attributes", {})
            for attr_name, attr_info in raw_attrs.items():
                if isinstance(attr_info, dict):
                    score = int(attr_info.get("score", 10))
                    written = str(attr_info.get("written_mod", "+0"))
                else:
                    score = int(attr_info)
                    written = "+0"
                calc_mod = calculate_ability_modifier(score)
                mod_str = f"{calc_mod:+d}"
                math_verification[attr_name] = {
                    "score": score,
                    "written_mod": written,
                    "correct_mod": mod_str,
                    "is_correct": (written == mod_str or written == str(calc_mod))
                }

            correct_pb = calculate_proficiency_bonus(char_level)
            class_info = CLASS_CANONICAL_DATA.get(char_class, {
                "saves": ["Força", "Constituição"],
                "hit_die": "d10",
                "spell_attr": None,
                "page_ref": "Livro do Jogador 2024, Cap. 3"
            })

            # PASSO 3: Recuperação RAG Exata dos Livros
            rag_queries = [
                f"{char_class} {extracted_data.get('subclass_name', '')}",
                f"{char_species} Espécie",
                f"{char_bg} Antecedente",
                "Modificadores de Atributo",
                "Classe de Armadura",
                "Pontos de Vida"
            ]
            
            rag_context_blocks = []
            for q in rag_queries:
                search_res = self.kb.search(q, top_k=1)
                for r in search_res:
                    rag_context_blocks.append(f"[{r['title']}]\n{r['content']}")

            rag_grounding_text = "\n\n---\n\n".join(rag_context_blocks[:4])

            # PASSO 4: Síntese Grounded Determinística com Citações Oficiais
            synthesis_input = f"""
### DADOS EXTRAÍDOS DA FICHA DO JOGADOR:
```json
{json.dumps(extracted_data, ensure_ascii=False, indent=2)}
```

### VERIFICAÇÃO MATEMÁTICA REALIZADA PELO SISTEMA:
- **Cálculo de Modificadores:** {json.dumps(math_verification, ensure_ascii=False)}
- **Bônus de Proficiência Calculado para Nível {char_level}:** +{correct_pb}
- **Salvaguardas Canônicas Oficiais da Classe {char_class.capitalize()}:** {class_info['saves']} ({class_info['page_ref']})
- **Dado de Vida Oficial:** {class_info['hit_die']}

### TRECHOS E PÁGINAS OFICIAIS RECUPERADOS DOS LIVROS (RAG):
{rag_grounding_text}

---
Gere o relatório completo de auditoria rigorosamente estruturado, citando exatamente as fontes e páginas acima.
"""

            synth_resp = self.client.models.generate_content(
                model=self.model_name,
                contents=[synthesis_input],
                config=types.GenerateContentConfig(
                    system_instruction=STRICT_SYNTHESIS_PROMPT,
                    temperature=0.0,
                    top_p=1.0
                )
            )

            report_text = synth_resp.text or "Relatório de auditoria gerado."

            return {
                "success": True,
                "report": report_text,
                "filename": filename,
                "extracted_data": extracted_data
            }

        except Exception as e:
            return {
                "success": False,
                "report": f"⚠️ Erro durante a auditoria da ficha: {str(e)}",
                "filename": filename,
                "extracted_data": {}
            }
