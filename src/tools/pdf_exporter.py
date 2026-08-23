import io
import re
import html
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas customizado para adicionar cabeçalho e rodapé elegante com número de páginas."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Borda nobre de página
        self.setStrokeColor(colors.HexColor("#cfc1a5"))
        self.setLineWidth(0.75)
        self.rect(20, 20, letter[0] - 40, letter[1] - 40)
        
        # Linha interna dourada
        self.setStrokeColor(colors.HexColor("#c99a4e"))
        self.setLineWidth(0.5)
        self.rect(23, 23, letter[0] - 46, letter[1] - 46)

        # Rodapé
        self.setFont("Helvetica-Oblique", 8)
        self.setFillColor(colors.HexColor("#665e52"))
        self.drawString(30, 28, "🐉 Grimório do Mestre & Mentor D&D 5e / 2024 — Relatório Oficial de Auditoria")
        
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(letter[0] - 30, 28, page_text)
        
        self.restoreState()


def _clean_markdown_to_reportlab(text: str) -> str:
    """Converte formatação básica de markdown para tags XML suportadas pelo ReportLab Paragraph."""
    if not text:
        return ""
    
    # Escapar entidades HTML primeiro
    text = html.escape(text)
    
    # Negrito: **texto** ou __texto__ -> <b>texto</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
    
    # Itálico: *texto* ou _texto_ -> <i>texto</i>
    text = re.sub(r'\*([^\*]+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_([^_]+?)_', r'<i>\1</i>', text)
    
    # Código / Destaque: `código` -> <font name="Courier" color="#7c2223">código</font>
    text = re.sub(r'`([^`]+?)`', r'<font name="Courier" color="#7c2223"><b>\1</b></font>', text)
    
    return text


def generate_sheet_pdf(audit_data: Dict[str, Any]) -> bytes:
    """
    Gera um documento PDF de alta qualidade e diagramação profissional
    com o resumo do personagem, grade de atributos e relatório completo de auditoria.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=35,
        rightMargin=35,
        topMargin=35,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    # Estilos customizados temáticos de RPG
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#6b3f02'),
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4e4436'),
        alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#6b3f02'),
        spaceBefore=10,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#8a5d14'),
        spaceBefore=8,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1c1813'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1c1813'),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1c1813')
    )

    story = []

    # 1. CABEÇALHO DO DOCUMENTO
    story.append(Paragraph("🛡️ GRIMÓRIO D&D — RELATÓRIO DE AUDITORIA", title_style))
    story.append(Paragraph("Análise de Ficha de Personagem & Conformidade de Regras Oficiais (D&D 5e / 2024)", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#c99a4e"), spaceAfter=12))

    # 2. CARTÃO DE IDENTIFICAÇÃO DO PERSONAGEM
    char_name = audit_data.get("character_name", "Personagem")
    class_lvl = audit_data.get("class_level", "Não informada")
    filename = audit_data.get("filename", "Ficha")
    created_at = audit_data.get("created_at", "")[:16].replace("T", " ")
    has_issues = audit_data.get("has_issues", False)
    status_label = "⚠️ AJUSTES RECOMENDADOS" if has_issues else "✅ FICHA VÁLIDA E REGULAR"
    status_bg = colors.HexColor("#fff3cd") if has_issues else colors.HexColor("#d4edda")
    status_color = colors.HexColor("#856404") if has_issues else colors.HexColor("#155724")

    id_data = [
        [
            Paragraph(f"<b>Personagem:</b> {html.escape(char_name)}", body_style),
            Paragraph(f"<b>Classe / Nível:</b> {html.escape(class_lvl)}", body_style),
        ],
        [
            Paragraph(f"<b>Arquivo:</b> {html.escape(filename)}", body_style),
            Paragraph(f"<b>Data da Auditoria:</b> {created_at}", body_style)
        ],
        [
            Paragraph(f"<b>Status Geral:</b> <font color='{status_color.hexval()}'><b>{status_label}</b></font>", body_style),
            Paragraph("<b>Edição Base:</b> D&D 2024 Player's Handbook", body_style)
        ]
    ]

    id_table = Table(id_data, colWidths=[260, 260])
    id_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#faf7f0")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cfc1a5")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ede5d5")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(id_table)
    story.append(Spacer(1, 12))

    # 3. GRADE DE ATRIBUTOS E SALVAGUARDAS (se disponível no extracted_data)
    extracted = audit_data.get("extracted_data", {})
    attrs = extracted.get("ability_scores", {})
    saves = extracted.get("saving_throws", {})
    
    if attrs and any(attrs.values()):
        story.append(Paragraph("⚔️ <b>Atributos & Modificadores</b>", h1_style))
        
        attr_order = [("FOR", "str"), ("DES", "dex"), ("CON", "con"), ("INT", "int"), ("SAB", "wis"), ("CAR", "cha")]
        
        header_row = ["Atributo", "FOR (Força)", "DES (Destreza)", "CON (Constituição)", "INT (Inteligência)", "SAB (Sabedoria)", "CAR (Carisma)"]
        val_row = ["Valor Base"]
        mod_row = ["Modificador"]
        save_row = ["Salvaguarda"]

        for label, k in attr_order:
            val = attrs.get(k, 10)
            try:
                val_int = int(val)
                mod = (val_int - 10) // 2
                mod_str = f"+{mod}" if mod >= 0 else str(mod)
            except Exception:
                val_int = 10
                mod_str = "+0"

            save_val = saves.get(k, mod_str)
            if isinstance(save_val, int):
                save_str = f"+{save_val}" if save_val >= 0 else str(save_val)
            else:
                save_str = str(save_val)

            val_row.append(str(val_int))
            mod_row.append(mod_str)
            save_row.append(save_str)

        attr_table_data = [
            [Paragraph(f"<b>{c}</b>", ParagraphStyle('Th', parent=body_style, fontName='Helvetica-Bold', fontSize=8, alignment=TA_CENTER, textColor=colors.HexColor('#6b3f02'))) for c in header_row],
            [Paragraph(c, ParagraphStyle('Td', parent=body_style, fontName='Helvetica-Bold', fontSize=9, alignment=TA_CENTER)) for c in val_row],
            [Paragraph(f"<b>{c}</b>", ParagraphStyle('TdMod', parent=body_style, fontName='Helvetica-Bold', fontSize=9, alignment=TA_CENTER, textColor=colors.HexColor('#8a5d14'))) for c in mod_row],
            [Paragraph(c, ParagraphStyle('TdSave', parent=body_style, fontSize=8.5, alignment=TA_CENTER)) for c in save_row]
        ]

        attr_table = Table(attr_table_data, colWidths=[75, 74, 74, 74, 74, 74, 74])
        attr_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#ebd8b8")),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#ffffff")),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor("#f8f4ec")),
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor("#ffffff")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cfc1a5")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ded3bc")),
            ('PADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(attr_table)
        story.append(Spacer(1, 14))

    # 4. PARSER DO RELATÓRIO COMPLETO EM MARKDOWN
    report_text = audit_data.get("report", "")
    
    if report_text:
        story.append(Paragraph("📜 <b>Diagnóstico Detalhado da Auditoria</b>", h1_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#cfc1a5"), spaceAfter=8))
        
        lines = report_text.split("\n")
        in_table = False
        table_rows = []

        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                if in_table and table_rows:
                    # Finalizar e desenhar tabela pendente
                    story.append(_render_reportlab_table(table_rows, body_style))
                    story.append(Spacer(1, 6))
                    table_rows = []
                    in_table = False
                continue

            # Detectar Tabela Markdown
            if trimmed.startswith("|") and trimmed.endswith("|"):
                # Ignorar linha de separador |--|--|
                if re.match(r'^\|[\s\:\-\|]+\|$', trimmed):
                    continue
                in_table = True
                cols = [c.strip() for c in trimmed.strip("|").split("|")]
                table_rows.append(cols)
                continue
            else:
                if in_table and table_rows:
                    story.append(_render_reportlab_table(table_rows, body_style))
                    story.append(Spacer(1, 6))
                    table_rows = []
                    in_table = False

            # Detectar Títulos H1/H2/H3
            if trimmed.startswith("### "):
                clean_title = _clean_markdown_to_reportlab(trimmed[4:])
                story.append(Paragraph(f"<b>{clean_title}</b>", h2_style))
            elif trimmed.startswith("## "):
                clean_title = _clean_markdown_to_reportlab(trimmed[3:])
                story.append(Paragraph(f"<b>{clean_title}</b>", h1_style))
            elif trimmed.startswith("# "):
                clean_title = _clean_markdown_to_reportlab(trimmed[2:])
                story.append(Paragraph(f"<b>{clean_title}</b>", title_style))

            # Detectar Lista com Marcadores (- ou *)
            elif trimmed.startswith("- ") or trimmed.startswith("* "):
                bullet_content = _clean_markdown_to_reportlab(trimmed[2:])
                story.append(Paragraph(f"• {bullet_content}", bullet_style))

            # Detectar Alertas / Callout Boxes (> [!NOTE] ou > Nota)
            elif trimmed.startswith(">"):
                callout_content = _clean_markdown_to_reportlab(trimmed.lstrip("> ").strip())
                callout_data = [[Paragraph(f"💡 <b>Nota do Grimório:</b> {callout_content}", callout_style)]]
                callout_tbl = Table(callout_data, colWidths=[520])
                callout_tbl.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#fffdf5")),
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#c99a4e")),
                    ('PADDING', (0, 0), (-1, -1), 6),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                story.append(Spacer(1, 4))
                story.append(callout_tbl)
                story.append(Spacer(1, 4))

            # Parágrafo Normal
            else:
                p_content = _clean_markdown_to_reportlab(trimmed)
                story.append(Paragraph(p_content, body_style))

        # Se sobrou tabela aberta no final do documento
        if in_table and table_rows:
            story.append(_render_reportlab_table(table_rows, body_style))
            story.append(Spacer(1, 6))

    # Construir PDF com o canvas customizado de páginas numeradas
    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer.getvalue()


def _render_reportlab_table(rows: list, base_style: ParagraphStyle) -> Table:
    """Renderiza uma tabela markdown em um elemento Table do ReportLab com larguras autoajustadas."""
    if not rows:
        return Spacer(1, 1)

    col_count = max(len(r) for r in rows)
    total_width = 520
    col_width = total_width / col_count

    table_data = []
    for r_idx, row in enumerate(rows):
        # Preencher colunas faltantes se houver
        padded = row + [""] * (col_count - len(row))
        row_paragraphs = []
        for c in padded:
            clean_c = _clean_markdown_to_reportlab(c)
            if r_idx == 0:
                p = Paragraph(f"<b>{clean_c}</b>", ParagraphStyle('ThRpt', parent=base_style, fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor('#6b3f02')))
            else:
                p = Paragraph(clean_c, ParagraphStyle('TdRpt', parent=base_style, fontSize=8))
            row_paragraphs.append(p)
        table_data.append(row_paragraphs)

    t = Table(table_data, colWidths=[col_width] * col_count)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f0e8d8")),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#ffffff")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cfc1a5")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ede5d5")),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t
