from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, HRFlowable
from reportlab.platypus.flowables import KeepTogether
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.units import inch
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Billing, BillingItem
import io

def generate_daily_billing_summary():
    # Get today's date range
    today = timezone.now().date()
    # today = datetime.utcnow() + timedelta(hours=5, minutes=30)
    start_date = timezone.datetime.combine(today, timezone.datetime.min.time())
    end_date = timezone.datetime.combine(today, timezone.datetime.max.time())

    # Filter billings for today
    billings = Billing.objects.filter(date__range=(start_date, end_date))
    total_revenue = sum(billing.total_amount for billing in billings)
    total_gst = sum(billing.gst_amount or 0 for billing in billings)
    total_paid = sum(billing.total_amount for billing in billings if billing.isPaid)
    total_paid_card = sum(billing.total_amount for billing in billings if billing.payment_mode=="Card")
    total_paid_cash = sum(billing.total_amount for billing in billings if billing.payment_mode=="Cash")
    total_paid_online = sum(billing.total_amount for billing in billings if billing.payment_mode=="Online")
    total_unpaid = sum(billing.total_amount for billing in billings if billing.isPaid==False)

    # Set up PDF file
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20, bottomMargin=20, leftMargin=40, rightMargin=40)
    elements = []

    # Set up styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='Title',
        fontSize=20,
        spaceAfter=18,
        textColor=colors.HexColor('#2A3F54'),
        alignment=1,  # Center align
        fontName='Helvetica-Bold'
    )
    header_style = ParagraphStyle(
        name='Header',
        fontSize=14,
        textColor=colors.HexColor('#0E5A8A'),
        spaceAfter=10,
        bold=True
    )
    normal_style = ParagraphStyle(
        name='Normal',
        fontSize=12,
        spaceAfter=6,
        textColor=colors.HexColor('#4F4F4F'),
        fontName='Helvetica'
    )
    bold_style = ParagraphStyle(
        name='Bold',
        fontSize=12,
        spaceAfter=6,
        textColor=colors.HexColor('#333333'),
        fontName='Helvetica-Bold'
    )

    # Add title and summary with a horizontal line
    title = Paragraph("Daily Billing Summary", title_style)
    elements.append(title)
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0E5A8A'), spaceAfter=14))
    elements.append(Paragraph(f"Date: {today.strftime('%B %d, %Y %I:%M %p')}", normal_style))
    elements.append(Paragraph(f"Total Revenue: Rs. {total_revenue}", bold_style))
    # elements.append(Paragraph(f"Total GST: Rs. {total_gst}", bold_style))
    elements.append(Paragraph(f"Total Paid Amount: Rs. {total_paid}", bold_style))
    elements.append(Paragraph(f"Total Unpaid Amount: Rs. {total_unpaid}", bold_style))
    elements.append(Spacer(1, 8))

    payment_table = Table(
        [
            ["Cash", "Online", "Card"],
            [total_paid_cash, total_paid_online, total_paid_card]
        ],
        hAlign='LEFT',
        colWidths=[2 * inch, 2 * inch, 2 * inch],
    )

    payment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0E5A8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FAFAFA')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3F3F3')]),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
        ]))
    elements.append(payment_table)
    elements.append(Spacer(1, 16))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0E5A8A'), spaceAfter=14))


    # Generate details for each billing/customer with a card-like design
    for billing in billings:
        customer_name = billing.customer_details.name

        # Create a table for customer and billing details in two columns
        customer_billing_table = Table(
            [
                [Paragraph(f"<b>Invoice ID:</b> {billing.id}"), Paragraph(f"<b>Time :</b> {(billing.date + timedelta(hours=5, minutes=30)).strftime('%I:%M %p')}")],
                [Paragraph(f"<b>Customer:</b> {customer_name}"), Paragraph(f"<b>Total Amount:</b> Rs. {billing.total_amount}")],
                [Paragraph(f"<b>Contact:</b> {billing.customer_details.phone_number}"), Paragraph(f"<b>Payment Mode:</b> {billing.payment_mode}")],
                [Paragraph(f"<b>Desk :</b> {billing.billing_desk.location}"), Paragraph(f"<b>Status:</b> {'Paid' if billing.isPaid else 'Pending'}")]
            ],
            hAlign='LEFT'
        )
        customer_billing_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9F9F9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#4F4F4F')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        # Add the table to elements with some spacing
        elements.append(customer_billing_table)
        elements.append(Spacer(1, 8))

        # Table data for purchased items
        item_data = [["Brand", "Article" ,"Product",  "Quantity", "Unit Price", "Discount", "Total Price"]]
        for item in billing.items.all():
            item_data.append([
                item.product.brand,
                item.product.article_no,
                f"{item.product.name} [ {item.product_variant.size} - {item.product_variant.color.color} ]",
                item.quantity,
                f"Rs. {item.unit_price}",
                f"{item.discount} %",
                f"Rs. {item.total_price}"
            ])

        # Add table to elements for purchased items with a modern design
        item_table = Table(item_data, hAlign='LEFT')
        item_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0E5A8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FAFAFA')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F3F3F3')]),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
        ]))
        elements.append(item_table)
        elements.append(Spacer(1, 16))  # Add space between customers
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0E5A8A'), spaceAfter=14))
        elements.append(Spacer(1, 16))  # Add space between customers


    # Build the PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
