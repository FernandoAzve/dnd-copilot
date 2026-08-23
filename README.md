# 🐉 Grimório do Mestre | Agente de IA para D&D (5e & 2024)

Um assistente inteligente e mentor de regras para **Dungeons & Dragons (5ª Edição e Atualizações de 2024)** desenvolvido com **Python, Google Gemini, Streamlit e RAG (Retrieval-Augmented Generation)**.

---

## 🌟 Principais Funcionalidades

- **🧙‍♂️ Três Modos de Atuação:**
  - **Mentor para Iniciantes**: Explicações didáticas, passo a passo, detalhamento de fórmulas (CA, CD, Proficiência, Espaços de Magia) e dicas de interpretação.
  - **Árbitro Rápido de Mesa**: Respostas diretas e sucintas para consultas imediatas durante a partida sem interromper o combate.
  - **Especialista Regras 2024 (One D&D)**: Destaque claro das mudanças e novidades da edição 2024 (ex: Poção de Cura como Ação Bônus, 1 Espaço de Magia por turno, Maestrias de Armas, nova condição de Exaustão).
- **📋 Auditor & Validador de Fichas (Fotos e PDFs)**:
  - Aceita **fotos de fichas de papel manuscritas** tiradas com o celular e **PDFs digitais preenchíveis**.
  - Valida cálculos matemáticos de modificadores de atributo (`(Valor - 10) // 2`).
  - Audita Bônus de Proficiência de acordo com o nível da classe.
  - Verifica salvaguardas oficiais da classe e valores de perícias (incluindo *Expertise*).
  - Audita Classe de Armadura (CA), Pontos de Vida (PV) estimados, CD de Magias e bônus de ataque.
  - Alerta sobre novidades de 2024 (Talentos de Origem, Maestrias de Armas).
  - Gera relatório estruturado com inconsistências encontradas, correções exatas e lembretes de itens esquecidos.
- **🎲 Rolador de Dados Integrado**:
  - Suporte a fórmulas completas (`1d20+5`, `2d6+3`, `8d6`, `4d6 drop lowest`).
  - Rolagens com Vantagem e Desvantagem.
  - Detecção visual de Acertos Críticos (20 Natural) e Falhas Críticas (1 Natural).
  - Botões rápidos de 1 clique (`d4`, `d6`, `d8`, `d10`, `d12`, `d20`, `d100`).
- **📜 Base de Regras & RAG Local**:
  - Catálogo de magias canônicas em Português e Inglês.
  - Guia instantâneo de condições de combate (Caído, Cego, Agarrado, Invisível, etc.).
  - Glossário bilíngue com equivalências oficiais e comunitárias.
  - Calculadoras de CD de Magia, Bônus de Ataque e Modificadores de Atributo.

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
- Python 3.10 ou superior.

### 2. Instalar Dependências
```bash
python -m pip install -r requirements.txt
```

### 3. Configurar a Chave de API do Google Gemini
Você pode obter uma chave gratuita no [Google AI Studio](https://aistudio.google.com/app/apikey).

Crie um arquivo `.env` na raiz do projeto ou renomeie `.env.example`:
```env
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-2.5-flash
```
*(Nota: Você também pode inserir a chave diretamente no menu lateral da interface web).*

### 4. Iniciar a Aplicação Web
```bash
python -m streamlit run app.py
```
Acesse no navegador: `http://localhost:8501`

---

## 🧪 Executar os Testes Automatizados

```bash
python -m pytest
```

---

## 📁 Estrutura do Repositório

```text
Agente D&D/
├── app.py                      # Ponto de entrada da aplicação Streamlit
├── requirements.txt            # Dependências do projeto
├── .env.example                # Configuração de exemplo da API
├── README.md                   # Documentação do projeto
├── src/
│   ├── agent/                  # Agente orquestrador e prompts
│   │   ├── gemini_agent.py     # Integração Google Gemini + Function Calling
│   │   └── prompts.py          # Modos: Mentor, Árbitro, Regras 2024
│   ├── rag/                    # Motor de busca semântica e indexação
│   │   └── vector_store.py     # Base de conhecimento de regras
│   ├── tools/                  # Ferramentas integradas
│   │   ├── dice.py             # Rolador de dados com vantagem/desvantagem
│   │   ├── spell_lookup.py     # Buscador de magias
│   │   ├── rules_lookup.py     # Buscador de regras e condições
│   │   └── character_calc.py   # Calculadora de bônus e CD
│   └── ui/                     # Interface visual Streamlit
│       ├── components.py       # Barra lateral, rolador e cards
│       └── styles.py           # CSS temático de RPG
├── data/                       # Arquivos de dados JSON
│   ├── conditions/             # Condições de combate
│   ├── rules/                  # Regras 5e e 2024
│   ├── spells/                 # Catálogo de magias
│   └── glossary.json           # Glossário PT-BR <-> EN
└── tests/                      # Testes automatizados com pytest
    ├── test_agent.py
    ├── test_dice.py
    └── test_rules.py
```
