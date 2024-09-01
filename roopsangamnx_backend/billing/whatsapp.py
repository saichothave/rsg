from decimal import Decimal
from dotenv import load_dotenv
from os import getenv
import json
import requests

load_dotenv()

# Custom JSON encoder for Decimal objects
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        return super(DecimalEncoder, self).default(obj)


def send_message_sync(data):
    url = "https://graph.facebook.com/" + f"/{getenv('VERSION')}/{getenv('PHONE_NUMBER_ID')}/messages"

    headers = {
        "Authorization": f"Bearer {getenv('APP_SECRET')}",
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=data)

    print(response.text)

def sendInvoiceImage(img, recipient):
    url = f"https://graph.facebook.com/{getenv('VERSION')}/{getenv('PHONE_NUMBER_ID')}/media"
    headers = {
        "Authorization": f"Bearer {getenv('APP_SECRET')}"
    }
    files = {
        'file': ('invoice.png', img, 'image/png', {'Expires': '0'}),
    }
    upload_media = requests.post(
        url, 
        data={
            "messaging_product": "whatsapp", 
            "recipient_type": "individual",
            'type': 'image/png',
        },
        files=files,
        headers=headers
    )

    media_id = upload_media.json()['id']

    url = "https://graph.facebook.com/" + f"/{getenv('VERSION')}/{getenv('PHONE_NUMBER_ID')}/messages"

    headers = {
        "Authorization": f"Bearer {getenv('APP_SECRET')}",
        'Content-Type': 'application/json'
    }

    data = json.dumps({
        "messaging_product": "whatsapp",
        "preview_url": False,
        "recipient_type": "individual",
        "to": recipient,
        "type": "IMAGE",
        "image": {
            "id":media_id
        }
    })

    response = requests.request("POST", url, headers=headers, data=data)
    print(response.text)

def get_text_message_input(recipient, text):
  return json.dumps({
    "messaging_product": "whatsapp",
    "preview_url": False,
    "recipient_type": "individual",
    "to": recipient,
    "type": "IMAGE",
    "image": {
      "id":523737826841000
    }
  })

def sendInvoiceTemplateMsg(img, recipient, cust_name, amount, inv_no, inv_date):

    url = f"https://graph.facebook.com/{getenv('VERSION')}/{getenv('PHONE_NUMBER_ID')}/media"
    headers = {
        "Authorization": f"Bearer {getenv('APP_SECRET')}"
    }
    files = {
        'file': ('invoice.png', img, 'image/png', {'Expires': '0'}),
    }
    upload_media = requests.post(
        url, 
        data={
            "messaging_product": "whatsapp", 
            "recipient_type": "individual",
            'type': 'image/png',
        },
        files=files,
        headers=headers
    )

    if upload_media.status_code == 200:

        media_id = upload_media.json()['id']

        url = "https://graph.facebook.com/" + f"/{getenv('VERSION')}/{getenv('PHONE_NUMBER_ID')}/messages"

        headers = {
            "Authorization": f"Bearer {getenv('APP_SECRET')}",
            'Content-Type': 'application/json'
        }

        data = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "template",
            "template": {
                "name": "rsg_invoice",
                "language": {
                    "code": "en_US"
                },
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "image",
                                "image": {
                                    "id":media_id
                                }
                            }
                        ]
                    },
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": cust_name
                            },
                            {
                                "type": "text",
                                "text": inv_no
                            },
                            {
                                "type": "text",
                                "text": f"{inv_date.strftime("%b")} {inv_date.strftime("%d")}"
                            },
                            {
                                "type": "currency",
                                "currency": {
                                "fallback_value": "VALUE",
                                "code": "INR",
                                "amount_1000": Decimal(amount*1000)
                                }
                            },
                            {
                                "type": "text",
                                "text": "Roopsangam Dresses NX, Shirdi"
                            }
                        ]
                    }
                ]
            }
        }, cls=DecimalEncoder)

        response = requests.request("POST", url, headers=headers, data=data)
        return response
    else:
        return upload_media