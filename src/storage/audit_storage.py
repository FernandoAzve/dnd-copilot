import os
import json
import uuid
import re
from datetime import datetime
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DEFAULT_AUDIT_DIR = os.path.join(BASE_DIR, "data", "audit_history")
USERS_ROOT = os.path.join(BASE_DIR, "data", "users")

def _get_audit_dir(username: Optional[str] = None) -> str:
    """Retorna o diretório de auditoria apropriado (específico do usuário ou global)."""
    if username and username.strip():
        user_clean = username.strip().lower()
        d = os.path.join(USERS_ROOT, user_clean, "audit_history")
    else:
        d = DEFAULT_AUDIT_DIR
    os.makedirs(d, exist_ok=True)
    return d

def _extract_summary_from_report(report_text: str, filename: str) -> Dict[str, str]:
    """Extrai informações chave do relatório gerado para indexação rápida."""
    char_name = "Personagem Não Identificado"
    char_class = "Classe Desconhecida"
    
    name_match = re.search(r'#+\s*📋?\s*Relatório de Auditoria da Ficha:\s*(.+)', report_text, re.IGNORECASE)
    if name_match:
        char_name = name_match.group(1).strip()
    elif filename:
        char_name = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ")
        
    class_match = re.search(r'Classe(?:\s*e\s*Subclasse)?\s*[\*:]+\s*([^\n\*\-]+)', report_text, re.IGNORECASE)
    if class_match:
        char_class = class_match.group(1).strip()
        
    return {
        "character_name": char_name,
        "class_level": char_class
    }

def save_audit(
    filename: str,
    report: str,
    user_notes: str = "",
    file_type: str = "pdf",
    extracted_data: Optional[Dict[str, Any]] = None,
    username: Optional[str] = None
) -> str:
    """Salva um relatório de auditoria de ficha no histórico persistente do usuário."""
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    short_uuid = uuid.uuid4().hex[:6]
    audit_id = f"audit_{now_str}_{short_uuid}"
    now_iso = datetime.now().isoformat()
    audit_dir = _get_audit_dir(username)
    
    summary = _extract_summary_from_report(report, filename)
    has_errors = "Inconsistências" in report and ("❌" in report or "Incorreto" in report)
    
    initial_messages = [
        {
            "role": "model",
            "content": f"📋 **Relatório de Auditoria da Ficha Gerado:**\n\n{report}",
            "created_at": now_iso
        }
    ]
    
    audit_data = {
        "id": audit_id,
        "username": username or "",
        "filename": filename,
        "character_name": summary["character_name"],
        "class_level": summary["class_level"],
        "file_type": file_type,
        "created_at": now_iso,
        "updated_at": now_iso,
        "user_notes": user_notes,
        "has_issues": has_errors,
        "report": report,
        "extracted_data": extracted_data or {},
        "messages": initial_messages
    }
    
    file_path = os.path.join(audit_dir, f"{audit_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, ensure_ascii=False, indent=2)
        
    return audit_id

def append_audit_message(audit_id: str, role: str, content: str, username: Optional[str] = None) -> bool:
    """Adiciona uma mensagem à conversa contínua sobre a ficha auditada."""
    audit_dir = _get_audit_dir(username)
    file_path = os.path.join(audit_dir, f"{audit_id}.json")
    
    if not os.path.exists(file_path):
        # Fallback para o diretório padrão
        fallback = os.path.join(DEFAULT_AUDIT_DIR, f"{audit_id}.json")
        if os.path.exists(fallback):
            file_path = fallback
        else:
            return False
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if "messages" not in data:
            data["messages"] = []
            
        data["messages"].append({
            "role": role,
            "content": content,
            "created_at": datetime.now().isoformat()
        })
        data["updated_at"] = datetime.now().isoformat()
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao adicionar mensagem à auditoria {audit_id}: {e}")
        return False

def list_audits(username: Optional[str] = None) -> List[Dict[str, Any]]:
    """Lista todas as auditorias salvas do usuário ordenadas da mais recente para a mais antiga."""
    audit_dir = _get_audit_dir(username)
    if not os.path.exists(audit_dir):
        return []
        
    audits = []
    for fname in os.listdir(audit_dir):
        if fname.endswith(".json"):
            file_path = os.path.join(audit_dir, fname)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    audits.append({
                        "id": data.get("id", fname.replace(".json", "")),
                        "filename": data.get("filename", "Ficha"),
                        "character_name": data.get("character_name", "Personagem"),
                        "class_level": data.get("class_level", ""),
                        "file_type": data.get("file_type", "pdf"),
                        "created_at": data.get("created_at", ""),
                        "updated_at": data.get("updated_at", data.get("created_at", "")),
                        "has_issues": data.get("has_issues", False),
                        "user_notes": data.get("user_notes", ""),
                        "messages_count": len(data.get("messages", []))
                    })
            except Exception as e:
                print(f"Erro ao ler auditoria {fname}: {e}")
                
    audits.sort(key=lambda a: a.get("updated_at", a.get("created_at", "")), reverse=True)
    return audits

def get_audit(audit_id: str, username: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Recupera os detalhes completos de uma auditoria salva."""
    audit_dir = _get_audit_dir(username)
    file_path = os.path.join(audit_dir, f"{audit_id}.json")
    if not os.path.exists(file_path):
        fallback = os.path.join(DEFAULT_AUDIT_DIR, f"{audit_id}.json")
        if os.path.exists(fallback):
            file_path = fallback
        else:
            return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao ler auditoria {audit_id}: {e}")
        return None

def delete_audit(audit_id: str, username: Optional[str] = None) -> bool:
    """Exclui uma auditoria do histórico do usuário."""
    audit_dir = _get_audit_dir(username)
    file_path = os.path.join(audit_dir, f"{audit_id}.json")
    if not os.path.exists(file_path):
        fallback = os.path.join(DEFAULT_AUDIT_DIR, f"{audit_id}.json")
        if os.path.exists(fallback):
            file_path = fallback
        else:
            return False
    try:
        os.remove(file_path)
        return True
    except Exception:
        return False
