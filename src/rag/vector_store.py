import os
import json
import re
import math
import hashlib
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CACHE_DIR = os.path.join(DATA_DIR, "embeddings")
CACHE_FILE = os.path.join(CACHE_DIR, "vector_cache.json")

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

def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Calcula a similaridade de cosseno entre dois vetores normalizados."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)

def _text_hash(text: str) -> str:
    """Gera um hash SHA-256 curto para indexação de cache."""
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:16]

class DnDKnowledgeBase:
    """
    Motor RAG Híbrido de Alta Performance para Regras, Magias, Condições e Livros de D&D.
    Combina Embeddings Neurais Densos (text-embedding-004), busca léxica BM25/TF-IDF
    e Re-Ranking por Fusão de Ranks Recíprocos (RRF).
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.documents: List[Document] = []
        self.embedding_cache: Dict[str, List[float]] = {}
        self.doc_embeddings: Dict[str, List[float]] = {}
        self.client = None
        
        self._init_genai_client()
        self._load_cache()
        self._load_all_data()

    def _init_genai_client(self):
        """Inicializa o cliente do Google GenAI se houver API key."""
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Aviso: Não foi possível inicializar o cliente GenAI para embeddings: {e}")

    def update_api_key(self, api_key: str):
        """Atualiza a chave de API e reinicializa o cliente de embeddings."""
        if api_key and api_key != self.api_key:
            self.api_key = api_key
            self._init_genai_client()

    def _load_cache(self):
        """Carrega os embeddings cacheados em disco para evitar recomputação."""
        os.makedirs(CACHE_DIR, exist_ok=True)
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    self.embedding_cache = json.load(f)
            except Exception as e:
                print(f"Aviso ao carregar cache de vetores: {e}")
                self.embedding_cache = {}

    def _save_cache(self):
        """Persiste o cache de embeddings no disco."""
        try:
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.embedding_cache, f)
        except Exception as e:
            print(f"Aviso ao salvar cache de vetores: {e}")

    def _tokenize(self, text: str) -> List[str]:
        """Tokenizador com remoção de pontuações e normalização."""
        text = text.lower()
        return re.findall(r'\b\w{2,}\b', text)

    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """Gera embedding para um texto com consulta em cache local e chamada à API."""
        h = _text_hash(text)
        if h in self.embedding_cache:
            return self.embedding_cache[h]

        if not self.client:
            return None

        try:
            # Gerar embedding usando Google GenAI SDK (text-embedding-004)
            resp = self.client.models.embed_content(
                model="text-embedding-004",
                contents=text[:2000]
            )
            if hasattr(resp, "embedding") and resp.embedding:
                vec = resp.embedding.values
                self.embedding_cache[h] = vec
                return vec
            elif hasattr(resp, "embeddings") and resp.embeddings:
                vec = resp.embeddings[0].values
                self.embedding_cache[h] = vec
                return vec
        except Exception as e:
            # Falha transitória na API de embeddings
            pass
        return None

    def _load_all_data(self):
        """Carrega todos os conjuntos de dados canônicos e fragmentos de livros indexados."""
        self.documents = []

        # 1. Carregar Regras Canônicas
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

        # 2. Carregar Condições de Combate
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

        # 3. Carregar Catálogo de Magias
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

        # 4. Carregar Glossário Oficial
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

    def search_lexical(self, query: str, top_k: int = 10, category_filter: Optional[str] = None) -> List[tuple]:
        """Busca léxica ponderada BM25 / TF-IDF."""
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
            
            # Correspondência de frase exata
            if query.lower().strip() in doc.content.lower() or query.lower().strip() in doc.title.lower():
                score += 8.0

            for token in query_tokens:
                if token in title_tokens:
                    score += 5.0
                count = content_tokens.count(token)
                if count > 0:
                    score += 1.0 + math.log(1 + count)
                    
            if score > 0:
                scored_docs.append((score, doc))
                
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return scored_docs[:top_k]

    def search_dense(self, query: str, top_k: int = 10, category_filter: Optional[str] = None) -> List[tuple]:
        """Busca vetorial densa via text-embedding-004 com similaridade de cosseno."""
        query_vec = self._get_embedding(query)
        if not query_vec:
            return []

        scored_docs = []
        for doc in self.documents:
            if category_filter and doc.category.lower() != category_filter.lower():
                continue
                
            # Gerar ou recuperar embedding do documento
            doc_sample = f"{doc.title}\n{doc.content[:600]}"
            doc_vec = self._get_embedding(doc_sample)
            if doc_vec:
                sim = _cosine_similarity(query_vec, doc_vec)
                if sim > 0.35:  # Limiar mínimo de relevância semântica
                    scored_docs.append((sim, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return scored_docs[:top_k]

    def search(self, query: str, top_k: int = 3, category_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Busca Híbrida Neural RRF (Dense Semantic + BM25 Lexical).
        Combina os rankings através de Reciprocal Rank Fusion para máxima acurácia.
        """
        if not query or not query.strip():
            return []

        lexical_results = self.search_lexical(query, top_k=15, category_filter=category_filter)
        dense_results = self.search_dense(query, top_k=15, category_filter=category_filter)

        # Se não houver resultados densos (ex: offline ou sem chave), usar léxico diretamente
        if not dense_results:
            results = []
            for score, doc in lexical_results[:top_k]:
                results.append({
                    "id": doc.doc_id,
                    "title": doc.title,
                    "category": doc.category,
                    "content": doc.content,
                    "score": round(score, 2),
                    "metadata": doc.metadata
                })
            return results

        # Reciprocal Rank Fusion (RRF)
        # Score = sum(1 / (60 + rank))
        rrf_scores: Dict[str, float] = {}
        doc_map: Dict[str, Document] = {}

        # 1. Pontuação Léxica
        for rank, (_, doc) in enumerate(lexical_results):
            doc_map[doc.doc_id] = doc
            rrf_scores[doc.doc_id] = rrf_scores.get(doc.doc_id, 0.0) + (1.0 / (60.0 + rank + 1))

        # 2. Pontuação Densa Neural
        for rank, (_, doc) in enumerate(dense_results):
            doc_map[doc.doc_id] = doc
            rrf_scores[doc.doc_id] = rrf_scores.get(doc.doc_id, 0.0) + (1.0 / (60.0 + rank + 1))

        sorted_docs = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
        top_rrf = sorted_docs[:top_k]

        # Salvar cache atualizado em background
        self._save_cache()

        results = []
        for doc_id, score in top_rrf:
            doc = doc_map[doc_id]
            results.append({
                "id": doc.doc_id,
                "title": doc.title,
                "category": doc.category,
                "content": doc.content,
                "score": round(score * 100, 2),
                "metadata": doc.metadata
            })

        return results
