from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
from reportlab.platypus import Image
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Line
import io

import os

class PDFGenerator:
    def __init__(self):
        pass
    
    def pdf_base(self, table_data, type, header, period, company):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        nunito_regular_path = os.path.join(base_dir, 'Nunito-Regular.ttf')
        nunito_bold_path = os.path.join(base_dir, 'Nunito-Bold.ttf')

        pdfmetrics.registerFont(TTFont('Nunito', nunito_regular_path))
        pdfmetrics.registerFont(TTFont('Nunito-Bold', nunito_bold_path))

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50, leftMargin=50, topMargin=40, bottomMargin=40
        )
        elements = []
        
        logo_path = os.path.join(base_dir, 'logo.png')
        
        logo = Image(logo_path)
        logo.drawHeight = 0.40 * inch
        logo.drawWidth = 2.7 * inch
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 20))
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='Title',
            fontName='Nunito-Bold',
            fontSize=11,
            alignment=2,
            spaceAfter=3
        )
        normal_style = ParagraphStyle(
            name='Normal',
            fontName='Nunito-Bold',
            fontSize=12,
        )

        title = Paragraph(type, title_style)
        elements.append(title)
        elements.append(Spacer(1, 5)) 
        
        line = Drawing(500, 1)
        line.add(Line(0, 0, 500, 0))
        elements.append(line)
        elements.append(Spacer(1, 20))

        company_info = [
            Paragraph(f"CNPJ da Empresa: {company}", normal_style),
            Paragraph(f"Período: {period[0]} a {period[1]}", normal_style),
        ]
        for info in company_info:
            elements.append(info)
            elements.append(Spacer(1, 8))
            
        elements.append(Spacer(1, 8))

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#606eee')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Nunito-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        
        available_width = A4[0] - doc.leftMargin - doc.rightMargin
        col_widths = [available_width / len(header)] * len(header)
        
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(table_style)
        elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        
        return buffer.getvalue()     
    
    def create_report(self, data, type, header, period, company):
        table_data = []
        table_data.append(header)
        for row in data:
            table_data.append(row)
            
        pdf = self.pdf_base(table_data, type, header, period, company)

        return pdf