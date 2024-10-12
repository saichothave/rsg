import json
from PIL import Image, ImageDraw, ImageFont
import io
import os

import requests
from escpos.printer import Usb
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import base64

from authentication.models import BillingDesk
from billing.printer import p
from .whatsapp import sendInvoiceTemplateMsg
from os import getenv


def add_newline_every_n_chars(text, n=15):
    # Split the text into chunks of size n
    chunks = [text[i:i+n] for i in range(0, len(text), n)]
    # Join the chunks with newline characters
    return '\n'.join(chunks)


def printBill(billing, request):
    # p = Usb()
    if request.user.user_type == "billingdesk":
        shop = BillingDesk.objects.filter(user_id=request.data['billing_desk_id'])[0].assigned_shop
        
        p.line_spacing(100,180)
        p.set(align='center', bold=True, font="a", custom_size=True, width=2, height=2, smooth=True)
        p.textln(shop.shop_name)

        p.line_spacing(85,180)
        p.ln()

        p.set(align='center', bold=False, font="b", underline=0, custom_size=True, width=2, height=2, smooth=True)
        p.textln(shop.address_line_1)

        if shop.address_line_2:
            p.textln(shop.address_line_2)

        p.textln(f"{shop.city} - {shop.zip_code}")

        p.set(align='center', bold=False, font="b", underline=0, normal_textsize=True)
        p.ln()
        p.text("_"*64)

        p.set(align='center', bold=False, font="b", underline=0, custom_size=True, width=2, height=2, smooth=True)
        p.text("INVOICE")

        p.set(align='center', bold=False, font="b", underline=0, normal_textsize=True)
        p.ln()
        p.textln("_"*64)

        p.cut()
    

    # p.printer.image(image)
    # p.cut("FULL")



def printImage(image):
    # p = Usb(dVendor=0x0483, idProduct=0x5743)
    p.image(image,impl="bitImageRaster")
    p.cut("FULL")

    
def generate_invoice_image(billing, request, printOnly=False, imageOnly=False):
    # Create an image with white background
    width, height = 600, 900  # Example dimensions
    DASH_NUM = 200
    bottom_margin = 200
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Load font
    base_dir = settings.BASE_DIR
    font_path = os.path.join(base_dir, 'fonts', 'times.ttf')
    emoji_font = os.path.join(base_dir, 'fonts', 'DejaVuSans.ttf')
    print('font path', font_path)
    try:
        title_font = ImageFont.truetype(font_path, 48)
        content_font = ImageFont.truetype(font_path, 32)
        dash_font = ImageFont.truetype(font_path, 20)
        table_font = ImageFont.truetype(font_path, 22)
    except IOError:
        print('ioerror')
        title_font = ImageFont.load_default()
        content_font = ImageFont.load_default()
        dash_font = ImageFont.load_default()
        table_font = ImageFont.load_default()

    y = 10

    def centerText(text, font):
        text_width = draw.textlength(text, font)
        x = (width - text_width) // 2
        draw.text((x,y), text, fill='black', font=font)


    shop = None
    if request.user.user_type == "billingdesk":
        shop = BillingDesk.objects.filter(user_id=request.user.id)[0].assigned_shop
        
        centerText(shop.shop_name,title_font)
        y += title_font.size + 10
        centerText("RoopsangamNX",content_font)
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
    if shop is not None:
        print(content_font.size*18)
        draw.text((300,y), align="right", text=f"SHP#-{shop.pk} BD#-{request.user.id}", fill='black', font=content_font)
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
    column_widths = [200, 80, 80 ,110, 110]

    for i, header in enumerate(headers):
        draw.text((x + sum(column_widths[:i]), y), header, fill='black', font=table_font)

    y += content_font.size + 5  # Move to the next line
    centerText("-"*DASH_NUM,dash_font)
    y += content_font.size + 5

    # Draw the items
    for item in billing.items.all():
        product_detail = str(item.product.article_no.article) + " " + str(item.product.brand) + " - " + str(item.product.name)
        formatted_product_detail = add_newline_every_n_chars(product_detail, 15)
       
        row = [
            # f"{item.product.brand} - {item.product.name}",
            formatted_product_detail,
            str(item.quantity),
            str(item.discount),
            f"{item.unit_price:.2f}",
            f"{item.total_price:.2f}"
        ] 
        for i, text in enumerate(row):
            draw.text((x + sum(column_widths[:i]), y), text, fill='black', font=table_font)
        y += table_font.size + 5  # Move to the next lin

        lines = (len(product_detail) // 15)
        y = y +(lines*table_font.size)
        draw.text((x,y),"[" + str(item.product_variant.size.size) + " - " + str(item.product_variant.color.color) + "]", fill='black', font=table_font)
        y += content_font.size + 5

        if y+bottom_margin >= height:
            new_height = y + table_font.size + bottom_margin  # Add some padding
            new_image = Image.new('RGB', (width, new_height), 'white')
            new_draw = ImageDraw.Draw(new_image)
            
            # Copy existing content to the new image
            new_image.paste(image, (0, 0))
            image = new_image
            draw = new_draw


    centerText("-"*DASH_NUM,dash_font)
    y += content_font.size + 5

    draw.text((10, y), f"Total Amount: {billing.total_amount}", fill='black', font=content_font)
    y += content_font.size + 8

    centerText("-"*DASH_NUM,dash_font)

    y += content_font.size + 8
    text = "Thank You Visit Again!!"

    centerText(text, font=content_font)


    y += content_font.size + 20


    # Save the image to a BytesIO object
    image_io = io.BytesIO()
    image.save(image_io, 'PNG')
    image_io.seek(0)

    image_base64 = base64.b64encode(image_io.getvalue()).decode('utf-8')

    # response = HttpResponse(image_io, content_type='image/png')

    send_whatsapp_msg_response = None
    printer_response = None

    response_data = {
        'image': image_base64,
        'invoiceNumber' : billing.id,
        'metadata': {

        }
    }

    if imageOnly:
        return JsonResponse(response_data)

    # [print invoice]  - backend to print-server communication 
    try:
        if getenv('ISHOSTED') == "False" :
            printer_response = requests.post(getenv('LOCALPRINTERURL'), data= json.dumps(
                    {
                        "imageBase64" : image_base64,
                        "filename":"invoice.png"
                    }
                ), headers={"Content-Type": "application/json"})
            
            # Check the response
            if printer_response is not None and printer_response.status_code == 200:
                response_data['metadata']['PrintStatus'] = 200
                response_data['metadata']['printMsg'] = "Bill generated and Printed successfully."
            elif printer_response is not None:
                response_data['metadata']['PrintStatus'] = printer_response.status_code
                response_data['metadata']['printMsg'] = "Bill generated and but not able to print.\n ERROR :: " + printer_response.text
        else:
            response_data['metadata']['PrintStatus'] = 300
            response_data['metadata']['printMsg'] = "Backend is hosted on other domain"
    except Exception as e:
        response_data['metadata']['PrintStatus'] = 500
        response_data['metadata']['printMsg'] = repr(e)

    #[whatsapp] -  send invoice on whatsapp
    try:
        if getenv('HASWPINTEGRATION') == "True":
            send_whatsapp_msg_response = sendInvoiceTemplateMsg(image_io.getvalue(), f"+91{billing.customer_details.phone_number}",billing.customer_details.name, billing.total_amount, billing.id, billing.date)
       
            if printOnly:
                response_data['metadata']['wpMsgSts'] = 201
                response_data['metadata']["wpMsgReason"] = 'Print Only Request'
            elif send_whatsapp_msg_response is not None and send_whatsapp_msg_response.status_code == 200:
                response_data['metadata']['wpMsgSts'] = send_whatsapp_msg_response.status_code
                response_data['metadata']["wpMsgReason"] = send_whatsapp_msg_response.text
        else:
            response_data['metadata']['wpMsgSts'] = 300
            response_data['metadata']["wpMsgReason"] = 'Whatsapp integration not available'
 
    except Exception as e:
        response_data['metadata']['wpMsgSts'] = 500
        response_data['metadata']["wpMsgReason"] = repr(e)


    response = JsonResponse(response_data)

    return response