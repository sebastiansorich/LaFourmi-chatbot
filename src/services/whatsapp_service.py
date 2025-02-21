from datetime import date
from src.config import Config
import requests
import logging
import io


def send_whatsapp_message(whatsappPhoneNumberId, whatsappToken, to, message):
    url = f"https://graph.facebook.com/{Config.WHATSAPP_VERSION}/{whatsappPhoneNumberId}/messages"
    headers = {
        "Authorization": f"Bearer {whatsappToken}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def upload_file_to_whatsapp(output, fileName, mimeType, whatsappPhoneNumberId, whatsappToken):
    url = f"https://graph.facebook.com/{Config.WHATSAPP_VERSION}/{whatsappPhoneNumberId}/media"
    headers = {
        "Authorization": f"Bearer {whatsappToken}"
    }

    # El archivo debe ser leído en formato binario
    files = {
        'file': (fileName, output, mimeType)
    }

    data = {
        'messaging_product': 'whatsapp'
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    
    # Verificar el código de respuesta
    if response.status_code == 200:
        response_json = response.json()
        media_id = response_json.get('id')

        if media_id:
            return media_id
        else:
            raise Exception("La respuesta no contiene el 'id' del medio")
    else:
        raise Exception(f"Error al subir archivo: {response.status_code} - {response.text}")

def send_whatsapp_message_with_file(mediaId, typeDocument, caption, fileName, whatsappPhoneDestination, whatsappPhoneNumberId, whatsappToken):
    url = f"https://graph.facebook.com/{Config.WHATSAPP_VERSION}/{whatsappPhoneNumberId}/messages"
    headers = {
        "Authorization": f"Bearer {whatsappToken}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": whatsappPhoneDestination,
        "type": typeDocument,
        typeDocument: {
            "id": mediaId,
            "caption": caption,
        }
    }

    if typeDocument == "document":
        payload["document"]["filename"] = fileName

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        logging.info(f"Mensaje enviado exitosamente a {whatsappPhoneDestination}")
    else:
        raise Exception(f"Error al enviar mensaje: {response.text}")
