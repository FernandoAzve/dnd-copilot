# 🎨 Guia Oficial de Design & Sistema Visual (Grimório D&D)

> **Regra de Ouro:** Todos os componentes, botões, modais, formulários e textos devem respeitar estritamente o contraste e as diretrizes deste guia tanto no **Modo Escuro (Grimório Sombrio)** quanto no **Modo Claro (Pergaminho Arcano)**.

---

## 🧭 1. Paleta de Cores & Tokens Semânticos

### 🌙 Modo Escuro (Grimório Sombrio)
| Token | Valor Hex | Finalidade |
| :--- | :--- | :--- |
| **`--app-bg`** | `#0f1115` | Fundo principal da aplicação, topo (header) e rodapé (footer) |
| **`--sidebar-bg`** | `#14171d` | Fundo da barra lateral |
| **`--primary-gold`** | `#c99a4e` | Dourado nobre (bordas ativas, botões primários, ícones) |
| **`--bright-gold`** | `#e5b967` | Dourado luminoso (títulos H1-H6, textos em destaque, hover) |
| **`--text-main`** | `#e8e3d9` | Texto principal de leitura (marfim suave, contraste AAA) |
| **`--text-muted`** | `#a09a8f` | Subtítulos, captions e metadados |
| **`--border-color`** | `#3d3424` | Bordas de cards, expansores e divisórias |
| **`--card-bg`** | `#171b22` | Balões de chat, cards de fichas e dropzone |
| **`--input-bg`** | `#1a1e27` | Caixas de texto, `st.chat_input` e inputs |

### ☀️ Modo Claro (Pergaminho Arcano)
| Token | Valor Hex | Finalidade |
| :--- | :--- | :--- |
| **`--app-bg`** | `#f7f4ec` | Fundo pergaminho da aplicação, topo e rodapé |
| **`--sidebar-bg`** | `#ece5d6` | Fundo da barra lateral |
| **`--primary-gold`** | `#8a5d14` | Bronze dourado escuro (alta legibilidade) |
| **`--bright-gold`** | `#6b3f02` | Bronze queimado (títulos H1-H6, botões primários) |
| **`--text-main`** | `#1c1813` | Texto principal de leitura (preto-sépia profundo) |
| **`--text-muted`** | `#4e4436` | Subtítulos e captions |
| **`--border-color`** | `#cfc1a5` | Bordas de pergaminho |
| **`--card-bg`** | `#ffffff` | Balões de chat e cartões brancos com borda sépia |
| **`--input-bg`** | `#ffffff` | Caixas de texto e inputs |

---

## 🎛️ 2. Padrões de Botões e Controles Interativos

### A. Botões Primários (`type="primary"` ou Ação Principal)
* **Uso**: Botão de Enviar, Ações de Destaque (*ex: Baixar PDF, Nova Conversa, Rolar Expressão, Entrar*).
* **Modo Escuro**:
  * Gradiente: `linear-gradient(180deg, #c99a4e 0%, #a8792c 100%)`
  * Texto: `#1a1408` (Preto em negrito `font-weight: 700`)
  * Borda: `1px solid #7c581d`
  * Hover: `linear-gradient(180deg, #dfb15b 0%, #bd8c36 100%)` com Glow dourado.
* **Modo Claro**:
  * Gradiente: `linear-gradient(180deg, #a36f1c 0%, #7c500c 100%)`
  * Texto: `#ffffff` (Branco em negrito `font-weight: 700`)
  * Borda: `1px solid #5a3804`

### B. Botões Secundários & Botões de Download
* **Uso**: Itens da lista de sessões, botões de alternância, botões padrão do Streamlit (`st.button`, `st.download_button`, `st.file_uploader`).
* **Modo Escuro**:
  * Gradiente: `linear-gradient(180deg, #282f3c 0%, #191e27 100%)`
  * Texto: `#f1ebd9` (Marfim claro)
  * Borda: `1px solid #3d3424`
  * Hover: Fundo `#374154`, borda `#e5b967`, texto `#ffffff`.
* **Modo Claro**:
  * Gradiente: `linear-gradient(180deg, #ffffff 0%, #eee6d6 100%)`
  * Texto: `#1c1813` (Preto sépia)
  * Borda: `1px solid #c9b999`
  * Hover: Borda `#8a5d14`, texto `#6b3f02`.

---

## 💬 3. Chat, Inputs e Placeholders

* **Estrutura Horizontal Única**: `div[data-testid="stChatInput"] > div` deve ser **estritamente Flexbox em linha única** (`flex-direction: row !important; align-items: center !important`).
* **Contraste de Placeholder**:
  * No Modo Escuro: `-webkit-text-fill-color: #e0dcd2 !important; opacity: 1 !important;` (Marfim luminoso).
  * No Modo Claro: `-webkit-text-fill-color: #4a4030 !important; opacity: 1 !important;` (Sépia escuro).
* **Proibição**: Nunca aplicar bordas internas no `<textarea>` do chat que possam quebrar a linha do botão de envio.

---

## 📦 4. Cards, Uploaders e Tooltips

1. **File Uploader (`st.file_uploader`)**:
   * Borda sólida elegante de `1px solid var(--border-color)` com `border-radius: 8px` (nunca bordas pontilhadas/dashed soltas).
   * Fundo escuro `#171b22` (Modo Escuro) / `#f2ece0` (Modo Claro).
2. **Tooltips (`help="..."` ou `stTooltipIcon`)**:
   * Ícone `?`: Dourado `#e5b967` (Escuro) / Bronze `#8a5d14` (Claro).
   * Popover (Caixa flutuante ao passar o mouse): Fundo `#1f2530`, borda `#d4af37`, texto em **Branco Puro (`#ffffff`)** com 100% de legibilidade.

---

## 📱 5. Responsividade Obrigatória

* **Desktop (> 992px)**: Layout amplo em duas colunas, barra lateral expansível, cabeçalho horizontal com pílula de perfil à direita.
* **Tablets (640px – 992px)**: Título `1.45rem`, pílula compacta.
* **Celulares (< 640px)**:
  * Cabeçalho vertical (`flex-direction: column; align-items: stretch`).
  * Altura mínima de toque em botões: `min-height: 42px`.
  * Tabelas com rolagem horizontal fluida (`overflow-x: auto; display: block`).

---

## ✅ Checklist Obrigatório antes de qualquer Deploy:

- [ ] Testou o componente no **Modo Escuro (Grimório)**?
- [ ] Testou o componente no **Modo Claro (Pergaminho)**?
- [ ] O texto tem contraste nítido (não há texto cinza sobre cinza ou branco sobre branco)?
- [ ] Os botões possuem feedback de hover com brilho temático?
- [ ] A tela se adapta suavemente em tela de celular (largura < 450px)?
- [ ] Todos os 25 testes unitários passaram (`python -m pytest`)?
