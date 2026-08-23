import os
import json
import re
import math
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

class Document:
    def __init__(self, doc_id: str, title: str, category: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        self.doc_id = doc_id
        self.title = title
        self.category = category
        self.content = content
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.doc_id,
            "title": self.title,
            "category": self.category,
            "content": self.content,
            "metadata": self.metadata
        }

class DnDKnowledgeBase:
    """Base de conhecimento RAG para regras, magias, condições e termos de D&D."""
    
    def __init__(self):
        self.documents: List[Document] = []
        self._load_all_data()
        
    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        return re.findall(r'\b\w{2,}\b', text)

    def _load_all_data(self):
        # 1. Carregar Regras
        rules_file = os.path.join(DATA_DIR, "rules", "rules_5e_2024.json")
        if os.path.exists(rules_file):
            with open(rules_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for idx, r in enumerate(data.get("rules", [])):
                    body = f"Tópico: {r.get('topic')}\nCategoria: {r.get('category')}\n"
                    if "rule" in r:
                        body += f"Regra: {r['rule']}\n"
                    if "edition_2014" in r:
                        body += f"Versão 2014: {r['edition_2014']}\n"
                    if "edition_2024" in r:
                        body += f"Versão 2024: {r['edition_2024']}\n"
                    if "rolls" in r:
                        body += f"Rolagens: {r['rolls']}\n"
                    if "masteries" in r:
                        body += "Maestrias: " + "; ".join(r['masteries']) + "\n"
                    if "faq" in r:
                        body += f"FAQ/Dica: {r['faq']}\n"
                        
                    self.documents.append(Document(
                        doc_id=f"rule_{idx}",
                        title=r.get("topic", "Regra"),
                        category="Regras",
                        content=body,
                        metadata=r
                    ))

        # 2. Carregar Condições
        cond_file = os.path.join(DATA_DIR, "conditions", "conditions.json")
        if os.path.exists(cond_file):
            with open(cond_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for idx, c in enumerate(data.get("conditions", [])):
                    body = f"Condição: {c.get('name_pt')} ({c.get('name_en')})\nEfeitos:\n"
                    if "effects" in c:
                        body += "\n".join(c["effects"])
                    if "effects_2014" in c:
                        body += "\n2014: " + "\n".join(c["effects_2014"])
                    if "effects_2024" in c:
                        body += "\n2024: " + "\n".join(c["effects_2024"])
                    if "changes_2024" in c:
                        body += f"\n2024 Changes: {c['changes_2024']}"
                        
                    self.documents.append(Document(
                        doc_id=f"cond_{idx}",
                        title=f"Condição: {c.get('name_pt')}",
                        category="Condições",
                        content=body,
                        metadata=c
                    ))

        # 3. Carregar Magias
        spells_file = os.path.join(DATA_DIR, "spells", "spells_srd.json")
        if os.path.exists(spells_file):
            with open(spells_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for idx, s in enumerate(data.get("spells", [])):
                    lvl = "Truque" if s["level"] == 0 else f"{s['level']}º Nível"
                    body = (
                        f"Magia: {s.get('name_pt')} ({s.get('name_en')})\n"
                        f"Nível: {lvl} de {s.get('school')}\n"
                        f"Tempo: {s.get('casting_time')} | Alcance: {s.get('range')} | Componentes: {s.get('components')}\n"
                        f"Duração: {s.get('duration')} | Classes: {', '.join(s.get('classes', []))}\n"
                        f"Descrição: {s.get('description')}\n"
                    )
                    if "higher_levels" in s:
                        body += f"Níveis Superiores: {s['higher_levels']}\n"
                        
                    self.documents.append(Document(
                        doc_id=f"spell_{idx}",
                        title=f"Magia: {s.get('name_pt')}",
                        category="Magias",
                        content=body,
                        metadata=s
                    ))

        # 4. Carregar Glossário
        gloss_file = os.path.join(DATA_DIR, "glossary.json")
        if os.path.exists(gloss_file):
            with open(gloss_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for idx, g in enumerate(data.get("terms", [])):
                    body = (
                        f"Termo: {g.get('pt')} ({g.get('en')}) [{g.get('abbr', '')}]\n"
                        f"Categoria: {g.get('category')}\n"
                        f"Definição: {g.get('description')}\n"
                    )
                    self.documents.append(Document(
                        doc_id=f"gloss_{idx}",
                        title=f"Termo: {g.get('pt')}",
                        category="Glossário",
                        content=body,
                        metadata=g
                    ))

        # 5. Carregar Fragmentos de Livros/PDFs Indexados
        chunks_file = os.path.join(DATA_DIR, "processed_chunks.json")
        if os.path.exists(chunks_file):
            with open(chunks_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for c in data.get("chunks", []):
                    self.documents.append(Document(
                        doc_id=c.get("id", f"pdf_chunk_{len(self.documents)}"),
                        title=c.get("title", "Trecho de Livro"),
                        category=c.get("category", "Livro Oficial"),
                        content=c.get("content", ""),
                        metadata={"source": c.get("source"), "page": c.get("page")}
                    ))


    def search(self, query: str, top_k: int = 3, category_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Busca semântica / BM25 ponderada nos documentos de D&D."""
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        scored_docs = []
        for doc in self.documents:
            if category_filter and doc.category.lower() != category_filter.lower():
                continue
                
            title_tokens = self._tokenize(doc.title)
            content_tokens = self._tokenize(doc.content)
            
            score = 0.0
            
            for token in query_tokens:
                # Bônus alto para correspondência no título
                if token in title_tokens:
                    score += 5.0
                # Correspondência no conteúdo
                count = content_tokens.count(token)
                if count > 0:
                    score += 1.0 + math.log(1 + count)
                    
            if score > 0:
                scored_docs.append((score, doc))
                
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        top_matches = scored_docs[:top_k]
        
        results = []
        for score, doc in top_matches:
            results.append({
                "id": doc.doc_id,
                "title": doc.title,
                "category": doc.category,
                "content": doc.content,
                "score": round(score, 2),
                "metadata": doc.metadata
            })
            
        return results
