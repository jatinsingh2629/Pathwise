"""
utils/certificate.py - PDF Certificate Generator.
Uses ReportLab to generate a professional learning completion certificate.
"""

import os
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


def generate_certificate(
    user_name: str,
    course_title: str,
    completion_date: datetime,
    output_dir: str,
    certificate_id: str
) -> Optional[str]:
    """
    Generate a PDF completion certificate.

    Args:
        user_name: Learner's full name
        course_title: Name of the completed learning path
        completion_date: Date of completion
        output_dir: Directory to save the certificate
        certificate_id: Unique certificate identifier

    Returns:
        Path to generated PDF file, or None on failure
    """
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib import colors
        from reportlab.lib.units import inch, cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from reportlab.pdfgen import canvas

        os.makedirs(output_dir, exist_ok=True)
        filename = f"certificate_{certificate_id}.pdf"
        filepath = os.path.join(output_dir, filename)

        # Use canvas for full control over layout
        c = canvas.Canvas(filepath, pagesize=landscape(A4))
        width, height = landscape(A4)

        # ── Background ───────────────────────────────────────────────────────
        c.setFillColor(colors.HexColor('#0F172A'))
        c.rect(0, 0, width, height, fill=True, stroke=False)

        # ── Decorative border ────────────────────────────────────────────────
        border_color = colors.HexColor('#6366F1')
        c.setStrokeColor(border_color)
        c.setLineWidth(4)
        c.rect(20, 20, width - 40, height - 40, fill=False, stroke=True)
        c.setLineWidth(1)
        c.rect(28, 28, width - 56, height - 56, fill=False, stroke=True)

        # ── Corner decorations ────────────────────────────────────────────────
        corner_size = 30
        for x, y in [(30, 30), (width-30, 30), (30, height-30), (width-30, height-30)]:
            c.setFillColor(colors.HexColor('#6366F1'))
            c.circle(x, y, 8, fill=True, stroke=False)

        # ── Header band ──────────────────────────────────────────────────────
        c.setFillColor(colors.HexColor('#1E293B'))
        c.rect(0, height - 110, width, 110, fill=True, stroke=False)

        # ── Logo / App name ──────────────────────────────────────────────────
        c.setFont('Helvetica-Bold', 14)
        c.setFillColor(colors.HexColor('#6366F1'))
        c.drawCentredString(width / 2, height - 45, '● PATHWISE LEARNING PLATFORM ●')

        # ── Certificate title ────────────────────────────────────────────────
        c.setFont('Helvetica-Bold', 11)
        c.setFillColor(colors.HexColor('#94A3B8'))
        c.drawCentredString(width / 2, height - 75, 'CERTIFICATE OF COMPLETION')

        # ── Star decorations ─────────────────────────────────────────────────
        c.setFont('Helvetica', 16)
        c.setFillColor(colors.HexColor('#6366F1'))
        c.drawString(width / 2 - 180, height - 78, '✦')
        c.drawString(width / 2 + 165, height - 78, '✦')

        # ── "This certifies that" ─────────────────────────────────────────────
        c.setFont('Helvetica', 13)
        c.setFillColor(colors.HexColor('#94A3B8'))
        c.drawCentredString(width / 2, height - 155, 'This is to certify that')

        # ── Learner Name ─────────────────────────────────────────────────────
        c.setFont('Helvetica-Bold', 36)
        c.setFillColor(colors.HexColor('#FFFFFF'))
        c.drawCentredString(width / 2, height - 210, user_name)

        # Underline for name
        name_width = c.stringWidth(user_name, 'Helvetica-Bold', 36)
        underline_y = height - 215
        c.setStrokeColor(colors.HexColor('#6366F1'))
        c.setLineWidth(2)
        c.line(width / 2 - name_width / 2, underline_y,
               width / 2 + name_width / 2, underline_y)

        # ── "has successfully completed" ─────────────────────────────────────
        c.setFont('Helvetica', 13)
        c.setFillColor(colors.HexColor('#94A3B8'))
        c.drawCentredString(width / 2, height - 250, 'has successfully completed the learning path')

        # ── Course Title ─────────────────────────────────────────────────────
        # Wrap long titles
        font_size = 22 if len(course_title) <= 50 else 18 if len(course_title) <= 80 else 15
        c.setFont('Helvetica-Bold', font_size)
        c.setFillColor(colors.HexColor('#6366F1'))
        c.drawCentredString(width / 2, height - 295, course_title[:80])

        # ── Completion date ──────────────────────────────────────────────────
        date_str = completion_date.strftime('%B %d, %Y')
        c.setFont('Helvetica', 12)
        c.setFillColor(colors.HexColor('#94A3B8'))
        c.drawCentredString(width / 2, height - 340, f'Completed on  {date_str}')

        # ── Divider line ─────────────────────────────────────────────────────
        c.setStrokeColor(colors.HexColor('#334155'))
        c.setLineWidth(1)
        c.line(80, height - 375, width - 80, height - 375)

        # ── Footer: Certificate ID + signature area ──────────────────────────
        footer_y = height - 415

        # Left: Certificate ID
        c.setFont('Helvetica', 9)
        c.setFillColor(colors.HexColor('#64748B'))
        c.drawString(80, footer_y, f'Certificate ID: {certificate_id}')
        c.drawString(80, footer_y - 15, f'Issued: {date_str}')
        c.drawString(80, footer_y - 30, 'Verify at: pathwise.learning/verify')

        # Center: Seal
        c.setFont('Helvetica-Bold', 9)
        c.setFillColor(colors.HexColor('#6366F1'))
        c.drawCentredString(width / 2, footer_y - 10, '★ VERIFIED COMPLETION ★')
        c.setFont('Helvetica', 8)
        c.setFillColor(colors.HexColor('#64748B'))
        c.drawCentredString(width / 2, footer_y - 24, 'PathWise Learning Platform')
        c.drawCentredString(width / 2, footer_y - 36, 'Powered by AI + CBR Technology')

        # Right: Signature
        c.setFont('Helvetica', 9)
        c.setFillColor(colors.HexColor('#64748B'))
        c.drawRightString(width - 80, footer_y - 5, 'PathWise Learning')
        c.setStrokeColor(colors.HexColor('#334155'))
        c.setLineWidth(1)
        c.line(width - 200, footer_y - 10, width - 80, footer_y - 10)
        c.drawRightString(width - 80, footer_y - 22, 'Director, Learning Systems')

        c.save()
        logger.info(f"Certificate generated: {filepath}")
        return filepath

    except ImportError:
        logger.error("reportlab not installed. Cannot generate certificate.")
        return None
    except Exception as e:
        logger.error(f"Certificate generation failed: {e}")
        return None
