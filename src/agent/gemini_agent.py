import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from ..tools.dice import roll_dice
from ..tools.spell_lookup import lookup_spell
from ..tools.rules_lookup import lookup_rule, lookup_condition, lookup_glossary
from ..tools.character_calc import (
    calculate_ability_modifier,
    calculate_proficiency_bonus,
    calculate_spell_stats,
    calculate_attack_modifier
)
from ..rag.vector_store import DnDKnowledgeBase
from .prompts import get_system_prompt

load_dotenv()

# Definições de ferramentas para o Google Gemini
def tool_roll_dice(formula: str = "1d20", advantage: bool = False, disadvantage: bool = False, reason: str = "") -> str:
    """Rola dados de RPG (ex: '1d20+5', '2d6+3', '8d6', '4d6kh3') com suporte a vantagem/desvantagem."""
    res = roll_dice(formula=formula, advantage=advantage, disadvantage=disadvantage, reason=reason if reason else None)
    return json.dumps(res, ensure_ascii=False)

def tool_lookup_spell(query: str) -> str:
    """Busca os atributos canônicos de uma magia de D&D pelo nome em Português ou Inglês."""
    res = lookup_spell(query)
    return json.dumps(res, ensure_ascii=False)

def tool_lookup_rule(topic: str) -> str:
    """Busca a regra oficial e diferenças 2014 vs 2024 sobre um tema de combate ou mecânica."""
    res = lookup_rule(topic)
    return json.dumps(res, ensure_ascii=False)

def tool_lookup_condition(condition_name: str) -> str:
    """Busca as regras exatas de uma condição de combate (ex: Caído, Cego, Agarrado, Invisível, Exausto)."""
    res = lookup_condition(condition_name)
    return json.dumps(res, ensure_ascii=False)

def tool_lookup_glossary(term: str) -> str:
    """Busca o significado e tradução de um termo técnico de D&D (ex: CA, CD, Slot, Salvaguarda)."""
    res = lookup_glossary(term)
    return json.dumps(res, ensure_ascii=False)

def tool_calculate_spell_stats(casting_ability_score: int, character_level: int, bonus_item: int = 0) -> str:
    """Calcula a CD de Salvaguarda de Magia e o Bônus de Ataque Mágico."""
    res = calculate_spell_stats(casting_ability_score, character_level, bonus_item)
    return json.dumps(res, ensure_ascii=False)

def tool_calculate_attack_modifier(ability_score: int, character_level: int, is_proficient: bool = True, weapon_magic_bonus: int = 0) -> str:
    """Calcula o bônus total para acertar um ataque com arma."""
    res = calculate_attack_modifier(ability_score, character_level, is_proficient, weapon_magic_bonus)
    return json.dumps(res, ensure_ascii=False)

TOOLS_MAP = {
    "tool_roll_dice": tool_roll_dice,
    "tool_lookup_spell": tool_lookup_spell,
    "tool_lookup_rule": tool_lookup_rule,
    "tool_lookup_condition": tool_lookup_condition,
    "tool_lookup_glossary": tool_lookup_glossary,
    "tool_calculate_spell_stats": tool_calculate_spell_stats,
    "tool_calculate_attack_modifier": tool_calculate_attack_modifier,
}

class DnDAgent:
    """Agente especialista em D&D que integra Gemini (Chat AFC), RAG e Ferramentas de Jogo."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.6-flash", mode: str = "mentor"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        self.mode = mode
        self.kb = DnDKnowledgeBase()
        self.chat_session = None
        self.history: List[Dict[str, Any]] = []
        self._init_client()

    def _init_client(self):
        self.client = None
        self.chat_session = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Erro ao inicializar Google GenAI Client: {e}")

    def update_config(self, api_key: Optional[str] = None, model_name: Optional[str] = None, mode: Optional[str] = None):
        changed = False
        if api_key is not None and api_key != self.api_key:
            self.api_key = api_key
            changed = True
        if model_name is not None and model_name != self.model_name:
            self.model_name = model_name
            changed = True
        if mode is not None and mode != self.mode:
            self.mode = mode
            changed = True
            
        if changed:
            self._init_client()

    def reset_chat(self):
        self.history = []
        self.chat_session = None

    def _get_or_create_chat(self, system_instruction: str):
        """Cria ou recupera a sessão de Chat com Automatic Function Calling (AFC)."""
        from google.genai import types

        tools_list = [
            tool_roll_dice,
            tool_lookup_spell,
            tool_lookup_rule,
            tool_lookup_condition,
            tool_lookup_glossary,
            tool_calculate_spell_stats,
            tool_calculate_attack_modifier
        ]

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=tools_list,
            temperature=0.4
        )

        return self.client.chats.create(
            model=self.model_name,
            config=config
        )

    def answer_query(self, user_message: str) -> Dict[str, Any]:
        """Processa a mensagem do usuário via Chat com AFC do Google Gemini."""
        # 1. Recuperar contexto do RAG
        rag_results = self.kb.search(user_message, top_k=3)
        rag_context = ""
        if rag_results:
            rag_context = "\n### Contexto do Grimório (Base de Regras e Livros Indexados):\n"
            for r in rag_results:
                rag_context += f"[{r['category']} - {r['title']}]\n{r['content']}\n---\n"

        system_instruction = get_system_prompt(self.mode)
        if rag_context:
            system_instruction += f"\n\n{rag_context}\nUse as informações acima para enriquecer suas explicações com citações exatas de regras e páginas quando aplicável."

        tool_logs = []

        # Se não houver cliente configurado com chave
        if not self.client:
            return self._offline_fallback_response(user_message, rag_results)

        try:
            # Criar ou atualizar a sessão de chat com as instruções atuais
            chat = self._get_or_create_chat(system_instruction)
            
            # Executar envio da mensagem via Chat.send_message (Usa Automatic Function Calling nativo e sem avisos)
            response = chat.send_message(user_message)
            
            final_text = response.text or "Sem resposta textual."

            # Salvar no histórico
            self.history.append({"role": "user", "content": user_message})
            self.history.append({"role": "model", "content": final_text})

            return {
                "text": final_text,
                "tool_logs": tool_logs,
                "rag_results": rag_results
            }

        except Exception as e:
            return {
                "text": f"⚠️ Erro ao consultar o modelo Gemini: {str(e)}\n\n*Alternativa local utilizada para responder com a base de regras:*",
                "tool_logs": tool_logs,
                "rag_results": rag_results,
                "fallback": self._offline_fallback_response(user_message, rag_results)["text"]
            }

    def _offline_fallback_response(self, user_message: str, rag_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Modo de contingência sem API Key: responde usando as ferramentas locais e o motor RAG."""
        tool_logs = []
        msg_lower = user_message.lower()

        # Checar se pediu rolagem de dados
        if "rol" in msg_lower or "d20" in msg_lower or "dado" in msg_lower or "d6" in msg_lower or "d8" in msg_lower:
            import re
            d_match = re.search(r'(\d+d\d+([+-]\d+)?)', msg_lower)
            formula = d_match.group(1) if d_match else "1d20"
            is_adv = "vantagem" in msg_lower and "desvantagem" not in msg_lower
            is_disadv = "desvantagem" in msg_lower
            res = roll_dice(formula=formula, advantage=is_adv, disadvantage=is_disadv)
            tool_logs.append({"tool": "roll_dice", "result": json.dumps(res, ensure_ascii=False)})
            text = f"🎲 **Rolagem Efetuada:**\n{res['breakdown']}\n\n*(Configure sua chave GEMINI_API_KEY na barra lateral para habilitar a inteligência completa do agente!)*"
            return {"text": text, "tool_logs": tool_logs, "rag_results": rag_results}

        # Checar se encontrou regras no RAG
        if rag_results:
            top_match = rag_results[0]
            text = (
                f"### 🧙‍♂️ Resposta do Grimório (Modo Offline):\n\n"
                f"Encontrei uma correspondência na base de regras oficial:\n\n"
                f"**{top_match['title']}** ({top_match['category']})\n\n"
                f"{top_match['content']}\n\n"
                f"---\n💡 *Para conversas dinâmicas, análises de personagens e explicações didáticas completas, insira sua GEMINI_API_KEY no painel lateral.*"
            )
            return {"text": text, "tool_logs": tool_logs, "rag_results": rag_results}

        return {
            "text": (
                "👋 **Bem-vindo ao Grimório do D&D!**\n\n"
                "Para desbloquear todo o poder do agente com explicações inteligentes, raciocínio tático e mentoria para novatos, "
                "por favor adicione sua **Chave de API do Google Gemini** no menu lateral à esquerda.\n\n"
                "Você pode obter uma chave gratuita no [Google AI Studio](https://aistudio.google.com/app/apikey).\n\n"
                "Enquanto isso, você já pode usar o **Rolador de Dados** e a consulta rápida de regras e condições na barra lateral!"
            ),
            "tool_logs": tool_logs,
            "rag_results": rag_results
        }
