import os
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CHAT_DIR = os.path.join(BASE_DIR, "data", "chat_history")

os.makedirs(CHAT_DIR, exist_ok=True)

def _generate_session_id() -> str:
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    short_uuid = uuid.uuid4().hex[:6]
    return f"chat_{now_str}_{short_uuid}"

def create_session(title: str = "Nova Conversa", mode: str = "mentor", model: str = "gemini-3.6-flash") -> str:
    """Cria uma nova sessão de chat persistente e retorna seu ID."""
    session_id = _generate_session_id()
    now_iso = datetime.now().isoformat()
    
    initial_data = {
        "id": session_id,
        "title": title,
        "mode": mode,
        "model": model,
        "created_at": now_iso,
        "updated_at": now_iso,
        "messages": [
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
    }
    
    file_path = os.path.join(CHAT_DIR, f"{session_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(initial_data, f, ensure_ascii=False, indent=2)
        
    return session_id

def save_session(
    session_id: str,
    messages: List[Dict[str, Any]],
    title: Optional[str] = None,
    mode: Optional[str] = None,
    model: Optional[str] = None
) -> bool:
    """Salva o estado atual de uma sessão de conversa."""
    if not session_id:
        return False
        
    file_path = os.path.join(CHAT_DIR, f"{session_id}.json")
    existing_data = {}
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except Exception:
            existing_data = {}
            
    now_iso = datetime.now().isoformat()
    
    # Auto-gerar título a partir da primeira pergunta do usuário se o título ainda for genérico
    current_title = title or existing_data.get("title", "Conversa D&D")
    if current_title in ["Nova Conversa", "Conversa D&D"] and len(messages) > 1:
        for m in messages:
            if m.get("role") == "user":
                user_text = m.get("content", "").strip()
                if user_text:
                    current_title = (user_text[:35] + "...") if len(user_text) > 35 else user_text
                break

    data = {
        "id": session_id,
        "title": current_title,
        "mode": mode or existing_data.get("mode", "mentor"),
        "model": model or existing_data.get("model", "gemini-3.6-flash"),
        "created_at": existing_data.get("created_at", now_iso),
        "updated_at": now_iso,
        "messages": messages
    }
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    return True

def load_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Carrega uma sessão específica pelo ID."""
    file_path = os.path.join(CHAT_DIR, f"{session_id}.json")
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar sessão {session_id}: {e}")
        return None

def list_sessions() -> List[Dict[str, Any]]:
    """Lista todas as sessões salvas ordenadas da mais recente para a mais antiga."""
    if not os.path.exists(CHAT_DIR):
        return []
        
    sessions = []
    for fname in os.listdir(CHAT_DIR):
        if fname.endswith(".json"):
            file_path = os.path.join(CHAT_DIR, fname)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    sessions.append({
                        "id": data.get("id", fname.replace(".json", "")),
                        "title": data.get("title", "Conversa sem título"),
                        "mode": data.get("mode", "mentor"),
                        "model": data.get("model", "gemini-3.6-flash"),
                        "updated_at": data.get("updated_at", ""),
                        "messages_count": len(data.get("messages", []))
                    })
            except Exception as e:
                print(f"Erro ao ler arquivo {fname}: {e}")
                
    # Ordenar por data de atualização decrescente
    sessions.sort(key=lambda s: s.get("updated_at", ""), reverse=True)
    return sessions

def delete_session(session_id: str) -> bool:
    """Exclui uma sessão salva."""
    file_path = os.path.join(CHAT_DIR, f"{session_id}.json")
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception:
            return False
    return False

def rename_session(session_id: str, new_title: str) -> bool:
    """Renomeia o título de uma sessão."""
    data = load_session(session_id)
    if not data:
        return False
    data["title"] = new_title
    data["updated_at"] = datetime.now().isoformat()
    file_path = os.path.join(CHAT_DIR, f"{session_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True
