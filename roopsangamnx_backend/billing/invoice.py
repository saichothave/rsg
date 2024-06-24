from PIL import Image, ImageDraw, ImageFont
import io
import os

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


def generate_invoice_image(billing):
    # Create an image with white background
    width, height = 400, 600  # Example dimensions
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Load font
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'Times New Roman.ttf')
    try:
        title_font = ImageFont.truetype(font_path, 24)
        content_font = ImageFont.truetype(font_path, 18)
    except IOError:
        title_font = ImageFont.load_default(size=30)
        content_font = ImageFont.load_default()

    y = 10

    def centerText(text, font):
        text_width = draw.textlength(text, font)
        x = (width - text_width) // 2
        draw.text((x,y), text, fill='black', font=font)


    centerText(f"Roopsangam Dresses",title_font)
    y += title_font.size + 10
    centerText(f"Khandoba Complex",content_font)
    y += content_font.size + 5
    centerText(f"Shirdi",content_font)
    y += content_font.size + 5

    # Draw other invoice details
    y += 20
    draw.text((10, y), f"Invoice #{billing.id}", fill='black', font=content_font)
    y += 30
    draw.text((10, y), f"Customer: {billing.customer_details.name}", fill='black', font=content_font)
    y += 30
    draw.text((10, y), f"Total Amount: {billing.total_amount}", fill='black', font=content_font)
    y += 30
    draw.text((10, y), f"Date: {billing.date}", fill='black', font=content_font)
    y += 40

    # Draw billing items
    for item in billing.items.all():
        draw.text((10, y), f"{item.product.name} x {item.quantity} - {item.total_price}", fill='black', font=content_font)
        y += 30

    # Save the image to a BytesIO object
    image_io = io.BytesIO()
    image.save(image_io, 'PNG')
    image_io.seek(0)
    return image_io