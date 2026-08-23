import os
import json
import re
import time
from typing import List, Dict, Any, Callable, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PDF_DIR = os.path.join(BASE_DIR, "data", "pdf_books")
CHUNKS_FILE = os.path.join(BASE_DIR, "data", "processed_chunks.json")

def clean_text(text: str) -> str:
    """Limpa quebras de linha excessivas mantendo a estrutura dos parágrafos."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return "\n".join(lines)

def build_toc_map(doc) -> Dict[int, str]:
    """Mapeia cada página do livro para o seu capítulo/seção correspondente do sumário."""
    toc_map = {}
    try:
        toc = doc.get_toc() # [[level, title, page_num], ...]
        if not toc:
            return toc_map
            
        current_section = "Introdução / Regras Gerais"
        sorted_toc = sorted(toc, key=lambda x: x[2])
        
        toc_idx = 0
        total_toc = len(sorted_toc)
        
        for page_num in range(1, len(doc) + 1):
            while toc_idx < total_toc and sorted_toc[toc_idx][2] <= page_num:
                level, title, _ = sorted_toc[toc_idx]
                if level == 1:
                    current_section = title
                elif level == 2:
                    current_section = f"{current_section} > {title}"
                toc_idx += 1
            toc_map[page_num] = current_section
    except Exception as e:
        print(f"Aviso ao extrair TOC: {e}")
        
    return toc_map

def extract_full_pages_from_pdf(pdf_path: str, progress_callback: Optional[Callable[[int, int, str], None]] = None) -> List[Dict[str, Any]]:
    """
    Extrai cada página completa do PDF preservando 100% das tabelas, regras,
    magias e contexto, mapeando o capítulo exato do sumário.
    """
    pdf_name = os.path.basename(pdf_path)
    pages_data = []
    
    try:
        import pymupdf
        doc = pymupdf.open(pdf_path)
        total_pages = len(doc)
        toc_map = build_toc_map(doc)
        
        for page_idx in range(total_pages):
            page_num = page_idx + 1
            if progress_callback and (page_num % 10 == 0 or page_num == total_pages):
                progress_callback(page_num, total_pages, pdf_name)
                
            page = doc[page_idx]
            page_text = page.get_text() or ""
            
            cleaned_page = clean_text(page_text)
            if len(cleaned_page) < 30: # Ignorar páginas em branco
                continue
                
            section_title = toc_map.get(page_num, "Regras Oficiais")
            full_title = f"{pdf_name} - {section_title} (Pág. {page_num})"
            
            pages_data.append({
                "id": f"{pdf_name}_p{page_num}",
                "source": pdf_name,
                "page": page_num,
                "section": section_title,
                "title": full_title,
                "category": "Livro Oficial",
                "content": cleaned_page
            })
            
        doc.close()
        return pages_data

    except ImportError:
        # Fallback usando pypdf caso pymupdf não esteja presente
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        
        for page_idx in range(total_pages):
            page_num = page_idx + 1
            if progress_callback and (page_num % 10 == 0 or page_num == total_pages):
                progress_callback(page_num, total_pages, pdf_name)
                
            page_text = reader.pages[page_idx].extract_text() or ""
            cleaned_page = clean_text(page_text)
            if len(cleaned_page) < 30:
                continue
                
            pages_data.append({
                "id": f"{pdf_name}_p{page_num}",
                "source": pdf_name,
                "page": page_num,
                "section": "Regras Oficiais",
                "title": f"{pdf_name} (Pág. {page_num})",
                "category": "Livro Oficial",
                "content": cleaned_page
            })
            
    return pages_data

def ingest_all_pdfs(progress_callback: Optional[Callable[[int, int, str], None]] = None) -> Dict[str, Any]:
    """Processa todos os PDFs na pasta data/pdf_books mantendo páginas completas e sem cortes."""
    start_time = time.time()
    
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR, exist_ok=True)
        return {"success": False, "count": 0, "message": "Pasta data/pdf_books criada. Coloque seus PDFs nela."}
        
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        return {"success": False, "count": 0, "message": "Nenhum arquivo .pdf encontrado em data/pdf_books/."}
        
    all_pages = []
    
    for f_idx, filename in enumerate(pdf_files):
        pdf_path = os.path.join(PDF_DIR, filename)
        pages = extract_full_pages_from_pdf(pdf_path, progress_callback)
        all_pages.extend(pages)
        
    # Salvar páginas completas processadas em JSON
    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        json.dump({"chunks": all_pages}, f, ensure_ascii=False, indent=2)
        
    elapsed = round(time.time() - start_time, 2)
    
    return {
        "success": True,
        "files_processed": pdf_files,
        "total_chunks": len(all_pages),
        "elapsed_seconds": elapsed,
        "output_file": CHUNKS_FILE,
        "message": f"Concluido em {elapsed}s! {len(pdf_files)} livro(s) indexado(s) com {len(all_pages)} paginas COMPLETAS e estruturadas com titulos de capitulos."
    }

def delete_pdf_book(filename: str) -> Dict[str, Any]:
    """Exclui um livro em PDF da biblioteca e atualiza a base indexada."""
    pdf_path = os.path.join(PDF_DIR, filename)
    if os.path.exists(pdf_path):
        try:
            os.remove(pdf_path)
        except Exception as e:
            return {"success": False, "message": f"Erro ao remover arquivo físico: {e}"}
    
    # Atualizar o arquivo processed_chunks.json
    if os.path.exists(CHUNKS_FILE):
        try:
            with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            remaining_chunks = [c for c in data.get("chunks", []) if c.get("source") != filename]
            
            with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
                json.dump({"chunks": remaining_chunks}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            return {"success": False, "message": f"Erro ao atualizar índice de fragmentos: {e}"}
            
    return {
        "success": True,
        "message": f"Livro '{filename}' removido com sucesso da biblioteca e do índice."
    }

if __name__ == "__main__":
    print("Iniciando indexacao completa de paginas e capitulos de D&D...")
    
    def cli_progress(curr, total, name):
        if curr % 25 == 0 or curr == total:
            print(f"[{name}] Pagina {curr}/{total}...")
            
    res = ingest_all_pdfs(cli_progress)
    print("\n" + res["message"])

