from PIL import Image, ImageDraw, ImageFont
import io
import os

from authentication.models import BillingDesk

# def generate_invoice_image(billing):

#     # Create an image with white background
#     width, height = 400, 600  # Example dimensions
#     image = Image.new('RGB', (width, height), 'white')
#     draw = ImageDraw.Draw(image)

#     # Set font (adjust the path to a valid font file on your system)
#     # Use a default font
#     try:
#         font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
#         font = ImageFont.truetype(font_path, 20)
#     except IOError:
#         font = ImageFont.load_default()


#     # Draw text (adjust coordinates and content as needed)
#     draw.text((10, 10), f"Invoice #{billing.id}", fill='black', font=font)
#     draw.text((10, 50), f"Customer: {billing.customer_details.name}", fill='black', font=font)
#     draw.text((10, 90), f"Total Amount: {billing.total_amount}", fill='black', font=font)
#     draw.text((10, 130), f"Date: {billing.date}", fill='black', font=font)

#     y = 170
#     for item in billing.items.all():
#         draw.text((10, y), f"{item.product.name} x {item.quantity} - {item.total_price}", fill='black', font=font)
#         y += 40

#     # Save the image to a BytesIO object
#     image_io = io.BytesIO()
#     image.save(image_io, 'PNG')
#     image_io.seek(0)
#     return image_io


def generate_invoice_image(billing, request):
    # Create an image with white background
    width, height = 400, 600  # Example dimensions
    DASH_NUM = 150
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Load font
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'Times New Roman.ttf')
    try:
        title_font = ImageFont.truetype(font_path, 24)
        content_font = ImageFont.truetype(font_path, 16)
        dash_font = ImageFont.truetype(font_path, 10)
        table_font = ImageFont.truetype(font_path, 14)
    except IOError:
        title_font = ImageFont.load_default(size=30)
        content_font = ImageFont.load_default()

    y = 10

    def centerText(text, font):
        text_width = draw.textlength(text, font)
        x = (width - text_width) // 2
        draw.text((x,y), text, fill='black', font=font)


    if request.user.user_type == "billingdesk":
        shop = BillingDesk.objects.filter(user_id=request.data['billing_desk_id'])[0].assigned_shop
        
        centerText(shop.shop_name,title_font)
        y += title_font.size + 10
        centerText(shop.address_line_1,content_font)
        y += content_font.size + 5
        if shop.address_line_2:
            centerText(shop.address_line_2,content_font)
            y += content_font.size + 5
        centerText(f"{shop.city} - {shop.zip_code}",content_font)
        y += content_font.size + 10

    # Add invoice name under 2 horizontal lines
    centerText("-"*DASH_NUM,dash_font)
    y += dash_font.size + 2

    centerText("INVOICE",content_font)
    y += content_font.size +2

    centerText("-"*DASH_NUM,dash_font)
    y += content_font.size + 10


    # Draw other invoice details
    draw.text((10, y), f"Invoice #{billing.id}", fill='black', font=content_font)
    y += content_font.size + 8
    draw.text((10, y), f"Customer: {billing.customer_details.name}", fill='black', font=content_font)
    y += content_font.size + 8
    draw.text((10, y), f"Date: {billing.date.strftime('%d/%m/%Y')}", fill='black', font=content_font)
    y += content_font.size + 10

    centerText("-"*DASH_NUM,dash_font)
    y += content_font.size

    # Draw billing items
    x=10

    # Draw the table headers
    headers = ["Description", "Qty", "Disc", "Unit Price", "Total Price"]
    column_widths = [130, 50, 50 ,80, 80]

    for i, header in enumerate(headers):
        draw.text((x + sum(column_widths[:i]), y), header, fill='black', font=table_font)

    y += content_font.size + 5  # Move to the next line
    centerText("-"*DASH_NUM,dash_font)
    y += content_font.size + 5

    # Draw the items
    for item in billing.items.all():
        row = [
            f"{item.product.brand} - {item.product.name}",
            str(item.quantity),
            str(item.discount),
            f"{item.unit_price:.2f}",
            f"{item.quantity * item.unit_price:.2f}"
        ] 
        for i, text in enumerate(row):
            draw.text((x + sum(column_widths[:i]), y), text, fill='black', font=table_font)
        y += table_font.size + 5  # Move to the next lin


    centerText("-"*DASH_NUM,dash_font)
    y += content_font.size + 5

    draw.text((10, y), f"Total Amount: {billing.total_amount}", fill='black', font=content_font)
    y += content_font.size + 8

    # Save the image to a BytesIO object
    image_io = io.BytesIO()
    image.save(image_io, 'PNG')
    image_io.seek(0)
    return image_io