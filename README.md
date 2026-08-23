# 🐉 D&D Copilot | Grimório do Mestre & Mentor de Regras (5e & 2024)

Um assistente inteligente, mentor e validador de fichas para **Dungeons & Dragons (5ª Edição e Atualizações de 2024)** desenvolvido com **Python, Google Gemini, Streamlit, RAG (Retrieval-Augmented Generation)**, autenticação multi-usuário e suporte a **Docker**.

---

## 🌟 Principais Funcionalidades

- **👥 Sistema Multi-Usuário & Autenticação Segura**:
  - Contas individuais com senhas protegidas via **PBKDF2-HMAC-SHA256** (100.000 iterações + Salt).
  - **Chaves do Gemini Individuais**: Criptografadas com **AES-256 (Fernet)** no banco de dados e descriptografadas apenas em memória.
  - **Perfis de Acesso (RBAC)**:
    - 👑 **Mestre Administrador**: Gerencia e atualiza a biblioteca compartilhada de PDFs de regras.
    - ⚔️ **Jogador**: Acesso a todas as regras, com histórico de chat e fichas 100% privado e isolado.
- **🧙‍♂️ Três Modos de Atuação da IA:**
  - **Mentor para Iniciantes**: Explicações didáticas, passo a passo e fórmulas detalhadas.
  - **Árbitro Rápido de Mesa**: Respostas diretas e sucintas para consultas imediatas durante o combate.
  - **Especialista Regras 2024 (One D&D)**: Destaque claro das mudanças e novidades da edição 2024.
- **📋 Auditor & Validador de Fichas (Fotos e PDFs)**:
  - Aceita **fotos de celular de fichas manuscritas** e **PDFs digitais**.
  - Validação determinística de atributos, salvaguardas da classe, proficiências, CA, PV e magias.
  - **Chat Contínuo por Personagem**: Converse diretamente com a IA sobre a ficha auditada com histórico persistente.
- **🎲 Rolador de Dados Integrado**:
  - Suporte a fórmulas completas (`1d20+5`, `2d6+3`, `8d6`, `4d6 drop lowest`, Vantagem/Desvantagem).
  - Detecção visual de Acertos Críticos (20 Natural) e Falhas Críticas (1 Natural).
- **📚 Biblioteca de Livros em PDF & RAG Ultra-Rápido**:
  - Extração com PyMuPDF C-Engine (processa livros inteiros em menos de 1 segundo).
  - Mapeamento automático de capítulos e seções do sumário.

---

## 🐳 Como Executar com Docker & Docker Compose (Recomendado)

A forma mais simples e rápida de rodar o D&D Copilot é utilizando o Docker Compose:

### 1. Iniciar o Container
```bash
docker compose up -d --build
```

### 2. Acessar no Navegador
Acesse: **`http://localhost:8501`**

### 3. Parar o Container
```bash
docker compose down
```

> **Nota de Persistência:** O volume `./data` garante que seus usuários cadastrados, histórico de conversas, fichas e livros em PDF permaneçam salvos mesmo após reiniciar os containers.

---

## 💻 Como Executar Localmente (Sem Docker)

### 1. Pré-requisitos
- Python 3.10 ou superior.

### 2. Instalar Dependências
```bash
python -m pip install -r requirements.txt
```

### 3. Iniciar a Aplicação
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
├── app.py                      # Aplicação principal Streamlit (Auth Gate + Navegação)
├── Dockerfile                  # Imagem Docker otimizada Python 3.11 Slim
├── docker-compose.yml          # Orquestração com persistência de volumes
├── requirements.txt            # Dependências do projeto
├── README.md                   # Documentação do projeto
├── src/
│   ├── agent/                  # Orquestrador Gemini e personas
│   ├── auth/                   # Autenticação, criptografia PBKDF2/AES-256 e RBAC
│   ├── rag/                    # Ingestão de PDFs e busca semântica
│   ├── storage/                # Persistência de chats e auditorias por usuário
│   ├── tools/                  # Rolador de dados, auditor de fichas e calculadoras
│   └── ui/                     # Interface visual Streamlit e estilos de grimório
├── data/                       # Banco de dados SQLite, regras e manuais
└── tests/                      # 22 Testes automatizados com pytest
```
