import os
import re
from bs4 import BeautifulSoup

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

# ---------------------------------------------------------
# Numbered Canvas for "Page X of Y" Footer and Header
# ---------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
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
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        
        # Colors
        header_color = HexColor("#334155")
        footer_color = HexColor("#64748b")
        border_color = HexColor("#cbd5e1")
        
        # Header (Top Margin: 48, so we draw at y=805)
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(header_color)
        self.drawString(36, 805, "SIH INTERNAL HACKATHON: TOP 10 SMART AUTOMATION PROBLEM STATEMENTS")
        self.setStrokeColor(border_color)
        self.setLineWidth(0.5)
        self.line(36, 798, 559, 798)
            
        # Footer (Bottom Margin: 48, so we draw line at y=40, text at y=28)
        self.setFont("Helvetica", 8)
        self.setFillColor(footer_color)
        self.setStrokeColor(border_color)
        self.setLineWidth(0.5)
        self.line(36, 40, 559, 40)
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(559, 28, page_str)
        self.drawString(36, 28, "Confidential | Software-Only Smart Automation Solutions")
        self.restoreState()

# ---------------------------------------------------------
# HTML Parser to Extract Problem Statements
# ---------------------------------------------------------
def parse_problem_statements(html_path):
    print(f"Parsing HTML from: {html_path}")
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        
    problem_statements = []
    cards = soup.find_all(class_="ps-card")
    for card in cards:
        # Extract Number
        num_div = card.find(class_="ps-number")
        num = num_div.get_text(strip=True) if num_div else ""
        
        # Extract Title
        title_div = card.find(class_="ps-title")
        title = title_div.get_text(strip=True) if title_div else ""
        
        # Extract Category/Color
        color = card.get("data-color", "blue")
        
        # Extract Tags
        tags = []
        meta_div = card.find(class_="ps-meta")
        if meta_div:
            tags = [t.get_text(strip=True) for t in meta_div.find_all(class_="ps-tag")]
            
        # Extract Subtitle containing Target, Feasibility, Impact
        subtitle_div = card.find(class_="ps-subtitle")
        subtitle_text = subtitle_div.get_text(strip=True) if subtitle_div else ""
        subtitle_text = subtitle_text.replace("\xa0", " ") # clean non-breaking spaces
        
        target = "N/A"
        feasibility = "N/A"
        impact = "N/A"
        if subtitle_text:
            parts = [p.strip() for p in subtitle_text.split("|")]
            for part in parts:
                if part.lower().startswith("target:"):
                    target = part.split(":", 1)[1].strip()
                elif part.lower().startswith("feasibility:"):
                    feasibility = part.split(":", 1)[1].strip()
                elif part.lower().startswith("impact:"):
                    impact = part.split(":", 1)[1].strip()
                    
        # Extract Problem Text
        prob_div = card.find(class_="ps-problem")
        problem = prob_div.get_text(strip=True) if prob_div else ""
        
        # Extract Solution Text
        sol_div = card.find(class_="ps-solution")
        solution = sol_div.get_text(strip=True) if sol_div else ""
        
        # Extract Winning Edge
        winning_edge = ""
        scores_div = card.find(class_="scores")
        if scores_div:
            badges = scores_div.find_all(class_="score-badge")
            for badge in badges:
                label_span = badge.find(class_="label")
                if label_span and label_span.get_text(strip=True).lower() == "winning edge":
                    val_span = badge.find(class_="value")
                    if val_span:
                        winning_edge = val_span.get_text(strip=True)
                        
        # Extract Govt Schemes from scaling-box
        govt_schemes = []
        scaling_box = card.find(class_="scaling-box")
        if scaling_box:
            schemes = scaling_box.find_all(class_="govt-scheme")
            for scheme in schemes:
                scheme_text = scheme.get_text(strip=True)
                if scheme_text not in govt_schemes:
                    govt_schemes.append(scheme_text)
                    
        problem_statements.append({
            "num": num,
            "title": title,
            "color": color,
            "tags": tags,
            "target": target,
            "feasibility": feasibility,
            "impact": impact,
            "problem": problem,
            "solution": solution,
            "winning_edge": winning_edge,
            "govt_schemes": govt_schemes
        })
        
    print(f"Successfully extracted {len(problem_statements)} problem statements.")
    return problem_statements

# ---------------------------------------------------------
# PDF Document Generator
# ---------------------------------------------------------
def generate_pdf(problem_statements, output_pdf_path):
    print(f"Generating PDF: {output_pdf_path}")
    
    # Page setup - A4 with 36pt (0.5 inch) margins
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=48,
        bottomMargin=48
    )
    
    # Styles Setup
    styles = getSampleStyleSheet()
    
    # Colors
    TEXT_DARK = HexColor("#1e293b")
    TEXT_MUTED = HexColor("#475569")
    
    COLOR_MAP = {
        "green": HexColor("#16a34a"),
        "red": HexColor("#dc2626"),
        "blue": HexColor("#2563eb"),
        "teal": HexColor("#0d9488"),
        "orange": HexColor("#ea580c"),
        "cyan": HexColor("#0891b2"),
        "purple": HexColor("#7c3aed"),
        "pink": HexColor("#db2777"),
        "indigo": HexColor("#4f46e5"),
        "yellow": HexColor("#ca8a04")
    }
    
    LIGHT_COLOR_MAP = {
        "green": HexColor("#f0fdf4"),
        "red": HexColor("#fef2f2"),
        "blue": HexColor("#eff6ff"),
        "teal": HexColor("#f0fdfa"),
        "orange": HexColor("#fff7ed"),
        "cyan": HexColor("#ecfeff"),
        "purple": HexColor("#f5f3ff"),
        "pink": HexColor("#fdf2f8"),
        "indigo": HexColor("#e0e7ff"),
        "yellow": HexColor("#fefce8")
    }
    
    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'PSTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=TEXT_DARK
    )
    
    num_style = ParagraphStyle(
        'PSNum',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        alignment=TA_CENTER
    )
    
    meta_style = ParagraphStyle(
        'PSMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT_MUTED
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12
    )
    
    body_style = ParagraphStyle(
        'PSBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK,
        alignment=TA_JUSTIFY
    )
    
    story = []
    
    # Document Header Title (only on the first page at the top)
    story.append(Paragraph("SIH INTERNAL HACKATHON: TOP 10 PROBLEM STATEMENTS", 
                           ParagraphStyle('DocHeaderTitle', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=HexColor("#1e293b"), alignment=TA_CENTER)))
    story.append(Paragraph("Curated Software-Only Smart Automation Solutions for College Selection Round", 
                           ParagraphStyle('DocHeaderSub', fontName='Helvetica', fontSize=9, leading=12, textColor=TEXT_MUTED, alignment=TA_CENTER)))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=HexColor("#1e293b"), spaceAfter=15))
    
    num_statements = len(problem_statements)
    
    for idx, ps in enumerate(problem_statements):
        card_elements = []
        
        # Color mapping
        accent_color = COLOR_MAP.get(ps['color'], HexColor("#2563eb"))
        bg_color = LIGHT_COLOR_MAP.get(ps['color'], HexColor("#eff6ff"))
        
        # 1. PS Number & Title Block
        num_p = Paragraph(f"<font color='{accent_color.hexval()}'><b>{ps['num']}</b></font>", num_style)
        title_p = Paragraph(f"<b>{ps['title']}</b>", title_style)
        
        title_table = Table([[num_p, title_p]], colWidths=[40, 483])
        title_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_color),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (0,-1), 6),
            ('RIGHTPADDING', (0,0), (0,-1), 2),
            ('LEFTPADDING', (1,0), (1,-1), 6),
            ('RIGHTPADDING', (1,0), (1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LINELEFT', (0,0), (0,-1), 4, accent_color),
        ]))
        card_elements.append(title_table)
        card_elements.append(Spacer(1, 6))
        
        # 2. Metadata Block
        meta_lines = []
        
        # Tags line
        tags_text = " • ".join(ps['tags'])
        meta_lines.append(f"<font color='{accent_color.hexval()}'><b>Tags:</b> {tags_text}</font>")
        
        # Target details line
        target_details = f"<b>Target:</b> {ps['target']}  |  <b>Feasibility:</b> {ps['feasibility']}  |  <b>Impact:</b> {ps['impact']}"
        if ps['winning_edge']:
            target_details += f"  |  <b>Winning Edge:</b> {ps['winning_edge']}"
        meta_lines.append(target_details)
        
        # Government schemes line
        if ps['govt_schemes']:
            schemes_text = ", ".join(ps['govt_schemes'])
            meta_lines.append(f"<b>Aligned Govt Schemes:</b> {schemes_text}")
            
        meta_p = Paragraph("<br/>".join(meta_lines), meta_style)
        
        meta_table = Table([[meta_p]], colWidths=[523])
        meta_table.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        card_elements.append(meta_table)
        card_elements.append(Spacer(1, 6))
        
        # 3. The Problem Box
        prob_heading = Paragraph("<font color='#dc2626'><b>🔴 The Problem</b></font>", section_title_style)
        prob_text = Paragraph(ps['problem'], body_style)
        prob_table = Table([[ [prob_heading, Spacer(1, 4), prob_text] ]], colWidths=[523])
        prob_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor("#fef2f2")),
            ('LINELEFT', (0,0), (0,-1), 3, HexColor("#ef4444")),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        card_elements.append(prob_table)
        card_elements.append(Spacer(1, 6))
        
        # 4. The Solution Box
        sol_heading = Paragraph("<font color='#16a34a'><b>🟢 Proposed Solution</b></font>", section_title_style)
        sol_text = Paragraph(ps['solution'], body_style)
        sol_table = Table([[ [sol_heading, Spacer(1, 4), sol_text] ]], colWidths=[523])
        sol_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor("#f0fdf4")),
            ('LINELEFT', (0,0), (0,-1), 3, HexColor("#22c55e")),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        card_elements.append(sol_table)
        
        # 5. Spacer and/or Separator
        if idx < num_statements - 1:
            card_elements.append(Spacer(1, 10))
            card_elements.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#cbd5e1"), spaceAfter=10))
        else:
            card_elements.append(Spacer(1, 10))
            
        story.append(KeepTogether(card_elements))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {output_pdf_path}")

# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    base_dir = r"d:\Testing\Research\SIH"
    html_file = os.path.join(base_dir, "SIH_Problem_Statements.html")
    output_pdf = os.path.join(base_dir, "SIH_Problem_Statements_Basic.pdf")
    
    statements = parse_problem_statements(html_file)
    generate_pdf(statements, output_pdf)
