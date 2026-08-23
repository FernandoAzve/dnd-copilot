# 🐉 AGENTS.md — Diretrizes de Engenharia, Arquitetura & Contexto do Projeto

Este documento é a **Fonte Única de Verdade (Single Source of Truth)** para agentes de IA e desenvolvedores que trabalham no repositório **Grimório do Mestre & Mentor D&D**.

---

## 🎯 1. Visão Geral do Projeto
O **Grimório do Mestre** é uma aplicação completa de assistência a RPG Dungeons & Dragons (D&D 5ª Edição e Revisão Oficial de 2024), desenvolvida em **Python** e **Streamlit**, integrando a API do **Google Gemini (google-genai SDK)**, **RAG** sobre livros de regras oficiais, **Visão Computacional Multimodal** para fichas, **Exportador de PDF** e **Sistema Multi-usuário Seguro**.

---

## 🏗️ 2. Estrutura do Código & Arquitetura

```
├── app.py                          # Ponto de entrada, Auth Gate, roteamento e injeção de contexto
├── requirements.txt                # Dependências do projeto
├── docs/
│   └── DESIGN_SYSTEM_GUIDE.md      # Guia canônico de cores, tipografia e contraste
├── src/
│   ├── agent/
│   │   ├── gemini_agent.py         # Chat AFC, streaming em tempo real e cascata de contingência
│   │   └── prompts.py              # System prompts das personas (Mentor, Árbitro, Regras 2024)
│   ├── auth/
│   │   ├── security.py             # PBKDF2 (100k iterações) e Fernet AES-256 (tokens & API keys)
│   │   ├── user_manager.py         # Banco SQLite RBAC de usuários e perfis
│   │   └── auth_ui.py              # Telas de Login, Registro e Gerenciamento de Perfil
│   ├── rag/
│   │   ├── pdf_ingest.py           # Ingestão de PDFs (PyMuPDF) com preservação de estrutura
│   │   └── vector_store.py         # Base de conhecimento e busca de trechos de regras
│   ├── storage/
│   │   ├── chat_storage.py         # Histórico de sessões de chat particionado por usuário
│   │   ├── audit_storage.py        # Histórico de auditoria de fichas particionado por usuário
│   │   └── character_storage.py    # Fichas de personagens cadastradas e contexto ativo
│   ├── tools/
│   │   ├── character_calc.py       # Cálculos determinísticos de regras (Mods, PB, CD, Ataque)
│   │   ├── character_importer.py   # Extração automática de personagens via PDF/Imagem
│   │   ├── dice.py                 # Rolador de dados (1d20, vantagem, desvantagem, drop lowest)
│   │   ├── pdf_exporter.py         # Exportação de fichas e relatórios em PDF com ReportLab
│   │   ├── rules_lookup.py         # Consulta canônica de regras e condições de combate
│   │   ├── sheet_validator.py      # Auditoria de fichas em 3 etapas (Visão -> Python Math -> RAG)
│   │   └── spell_lookup.py         # Consulta oficial de magias
│   └── ui/
│       ├── components.py           # Barra lateral, rolador de dados e renderização de mensagens
│       ├── character_view.py       # Central de Heróis (lista, importação e editor manual)
│       ├── sheet_view.py           # Auditor de fichas e chat contínuo por personagem
│       └── styles.py               # Sistema visual dual-theme (Grimório Escuro vs Pergaminho Claro)
└── tests/                          # Suíte de testes unitários automatizados com Pytest
```

---

## 🌿 3. Fluxo de Trabalho Git & Branches

1. **Branch `main` (Produção)**:
   * Conectada diretamente ao deploy do **Streamlit Cloud**.
   * **REGRA:** Nenhum commit de feature experimental deve ser feito diretamente na `main`.
2. **Branch `develop` (Desenvolvimento Ativo)**:
   * Onde todas as novas features, refatorações e correções de bugs devem ser criadas e testadas.
   * Só deve ser feito merge para a `main` após **100% dos testes unitários passarem** e a usabilidade ser validada.

---

## 🎨 4. Diretrizes de UI & Sistema Visual (Design System)

> **OBRIGATÓRIO:** Toda interface criada DEVE obedecer ao [`docs/DESIGN_SYSTEM_GUIDE.md`](docs/DESIGN_SYSTEM_GUIDE.md).

### Regras Visuais Críticas:
1. **Suporte Dual-Theme Estrito**:
   * **Modo Escuro (Grimório Sombrio)**: Fundo `#0f1115`, barra lateral `#14171d`, dourado `#c99a4e`/`#e5b967`, texto `#e8e3d9`.
   * **Modo Claro (Pergaminho Arcano)**: Fundo `#f7f4ec`, barra lateral `#ece5d6`, bronze `#8a5d14`/`#6b3f02`, texto `#1c1813`.
2. **Contraste & Legibilidade**:
   * Proibido texto branco sobre fundo claro ou cinza escuro sobre fundo escuro.
   * Placeholders devem conter `-webkit-text-fill-color` e `opacity: 1` para manter nitidez.
3. **Botões**:
   * Mapear sempre todas as variantes do Streamlit: `.stButton > button`, `div[data-testid="stDownloadButton"] button`, `div[data-testid="stFormSubmitButton"] button`, `div[data-testid="stFileUploader"] button`.
4. **Chat Input**:
   * Manter Flexbox em linha única (`flex-direction: row; align-items: center`), garantindo que o botão de envio e a caixa de texto nunca quebrem linha.

---

## 🎲 5. Regras Canônicas de D&D (5e & 2024 Revision)

* **Modificador de Atributo**: `(Valor - 10) // 2`
* **Bônus de Proficiência (PB)**: `2 + (Nível - 1) // 4`
* **Salvaguardas**:
  * Não Proficiente: $\text{Mod} + \text{Bônus de Itens Mágicos (ex: Capa de Proteção)}$
  * Proficiente: $\text{Mod} + \text{PB} + \text{Bônus de Itens Mágicos}$
* **CD de Salvaguarda de Magia**: $8 + \text{PB} + \text{Modificador do Atributo de Conjuração} + \text{Bônus de Itens}$
* **Verificação de Checkboxes em Fichas**: Uma bolinha pintada/marcada (●) indica proficiência; a mera anotação do modificador básico NÃO significa proficiência.

---

## ⚡ 6. Resiliência do Gemini & Cascata de Contingência

Ao chamar a API do Gemini, utilize sempre o mecanismo de redundância e backoff:
1. `gemini-3.5-flash` (Padrão)
2. `gemini-3.5-flash-lite` (Fallback rápido)
3. `gemini-flash-latest` (Fallback secundário)
4. `gemini-3.6-flash` / `gemini-3-flash-preview`
5. Fallback local offline baseado no RAG e tabelas canônicas.

---

## ✅ 7. Protocolo de Qualidade Obrigatório para Agentes

Antes de concluir qualquer tarefa ou propor commit:
1. **Executar Testes Unitários**: Rodar `python -m pytest` e garantir 100% de sucesso.
2. **Verificar ambos os Temas**: O componente foi validado no modo claro e escuro?
3. **Garantir Não-Regressão**: Nenhuma funcionalidade anterior (como persistência de login, streaming ou PDF) foi quebrada?
4. **Documentar Código**: Manter docstrings e tipagem estrita no Python.
