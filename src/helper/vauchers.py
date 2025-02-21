import logging
import fitz  # PyMuPDF
from flask import jsonify
from PyPDF2 import PdfReader
import pandas as pd
import pytesseract
from PIL import Image
import io
from src.config import Config
import requests
from src.controllers.stock_controllers import update_stock_from_excel
from src.services.whatsapp_service import send_whatsapp_message_with_file, upload_file_to_whatsapp

BANK_KEYWORDS = ["Banco Economico", "Banco sol", "Banco Mercantil Santa Cruz", "Transferencia", "Comprobante", "Pago recibido", "BNB", "QR"]


def is_single_page_pdf(file_content):
    try:
        # Leer el archivo en memoria
        pdf_reader = PdfReader(io.BytesIO(file_content))
        return len(pdf_reader.pages) == 1
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
        return False

def extract_text_from_pdf(pdf_stream):
    try:
        if not pdf_stream or not hasattr(pdf_stream, "read"):
            raise ValueError("Invalid PDF stream provided")

        pdf_stream.seek(0)  # Asegúrate de que el cursor esté al inicio
        header = pdf_stream.read(10)  # Leer los primeros bytes del archivo
        logging.debug(f"PDF Header: {header}")

        if not header.startswith(b"%PDF"):
            raise ValueError("Invalid PDF format")
        pdf_stream.seek(0)  # Volver al inicio para procesar

        doc = fitz.open(stream=pdf_stream, filetype="pdf")  # Abrir PDF desde flujo
        text = ""

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            page_text = page.get_text("text")

            if page_text.strip():
                text += page_text
            else:
                pix = page.get_pixmap(dpi=300)
                image = Image.open(io.BytesIO(pix.tobytes(output="png")))
                text += pytesseract.image_to_string(image, lang="eng", config="--psm 6")

            logging.debug(f"Texto extraído de la página {page_num + 1}: {page_text}")

        return text.strip()

    except fitz.FileDataError:
        logging.error("PyMuPDF failed to open the PDF stream. File might be corrupt.")
        return None
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}", exc_info=True)
        return None



def extract_text_from_image(image_stream):
    try:
        img = Image.open(image_stream)  # Abrir imagen desde el flujo en memoria
        text = pytesseract.image_to_string(img)  # Usar OCR para extraer texto
        return text.strip()
    except Exception as e:
        logging.error(f"Error extracting text from image: {e}")
        return None

    

def contains_bank_keywords(text, keywords):
    for keyword in keywords:
        if keyword.lower() in text.lower():  # Ignora mayúsculas/minúsculas
            return True
    return False

def process_pdf(file_content, branch):
    try:
        # Reiniciar el puntero del archivo por si ya se leyó antes
        file_content.seek(0)

        # Extraer texto del PDF
        extracted_text = extract_text_from_pdf(file_content)
        if not extracted_text:
            logging.info("No text extracted from PDF")
            return jsonify({"message": "PDF does not contain readable text"}), 200

        logging.info(f"Text extracted from PDF: {extracted_text}")

        if contains_bank_keywords(extracted_text, BANK_KEYWORDS):
            # Subir el archivo a WhatsApp
            try:
                # Reiniciar el flujo para la subida
                file_content.seek(0)
                media_id = upload_file_to_whatsapp(
                    output=file_content,  # Archivo en memoria
                    fileName="processed_document.pdf",
                    mimeType="application/pdf",
                    whatsappPhoneNumberId=branch.whatsapp_number_id,
                    whatsappToken=branch.whatsapp_token
                )
                logging.info(f"Archivo subido exitosamente a WhatsApp, media_id: {media_id}")

            except Exception as e:
                logging.error(f"Error uploading PDF to WhatsApp: {e}", exc_info=True)
                return jsonify({"message": "Error uploading PDF"}), 500

            # Enviar el mensaje con el archivo procesado
            try:
                send_whatsapp_message_with_file(
                    mediaId=media_id,
                    typeDocument="document",
                    caption=f"Comprobante PDF recibido y procesado. Texto extraído: {extracted_text}",
                    fileName="processed_document.pdf",
                    #whatsappPhoneDestination=branch.phone,
                    whatsappPhoneDestination="59168682046",
                    whatsappPhoneNumberId=branch.whatsapp_number_id,
                    whatsappToken=branch.whatsapp_token
                )
                logging.info("Mensaje enviado exitosamente con el PDF procesado")

                return jsonify({"message": "PDF processed successfully", "extracted_text": extracted_text}), 200

            except Exception as e:
                logging.error(f"Error sending WhatsApp message: {e}", exc_info=True)
                return jsonify({"message": "Error sending PDF"}), 500

        else:
            logging.info("No bank keywords found in PDF")
            return jsonify({"message": "PDF does not contain bank keywords"}), 200

    except Exception as e:
        logging.error(f"Error processing PDF: {e}", exc_info=True)
        return jsonify({"message": "Error processing PDF"}), 500


def process_image(file_content, branch):
    file_content.seek(0)  # Asegúrate de que el cursor esté al inicio
    extracted_text = extract_text_from_image(file_content)
    if not extracted_text:
        logging.info("No text extracted from image")
        return jsonify({"message": "Image does not contain readable text"}), 200

    logging.info(f"Text extracted from image: {extracted_text}")

    if contains_bank_keywords(extracted_text, BANK_KEYWORDS):
        try:
            # Subir la imagen a WhatsApp
            file_content.seek(0)  # Asegúrate de que el cursor esté al inicio antes de subir
            media_id = upload_file_to_whatsapp(
                output=file_content,
                fileName="processed_image.jpg",
                mimeType="image/jpeg",
                whatsappPhoneNumberId=branch.whatsapp_number_id,
                whatsappToken=branch.whatsapp_token
            )

            # Enviar el mensaje con la imagen procesada
            send_whatsapp_message_with_file(
                mediaId=media_id,
                typeDocument="image",
                caption=f"Comprobante de imagen recibido y procesado. Texto extraído: {extracted_text}",
                fileName="processed_image.jpg",
                whatsappPhoneDestination="59168682046",
                whatsappPhoneNumberId=branch.whatsapp_number_id,
                whatsappToken=branch.whatsapp_token
            )

            return jsonify({"message": "Image processed successfully", "extracted_text": extracted_text}), 200

        except Exception as e:
            logging.error(f"Error processing and sending image: {e}")
            return jsonify({"message": "Error processing image"}), 500
    else:
        logging.info("No bank keywords found in image")
        return jsonify({"message": "Image does not contain bank keywords"}), 200



def handle_file_message(message, branch, branch_cellphone):
    
    # Extraer el número de teléfono desde el mensaje
    phone_number = message.get('from')
    if not phone_number:
        logging.error("Error: Missing phone number in document message")
        return jsonify({'error': 'Missing phone number'}), 400

    # Verificar si el remitente es el administrador
    if phone_number == branch_cellphone:
        logging.error(f"Error: {phone_number} is not authorized to send documents")
        return jsonify({'error': 'Unauthorized sender'}), 401

    # Validar la información del archivo
    document = message.get('document')
    if not document:
        logging.error("Error: No document provided in message")
        return jsonify({'error': 'No document provided'}), 400

    mime_type = document.get('mime_type')
    if not mime_type:
        logging.error("Error: MIME type not provided in document message")
        return jsonify({'error': 'Missing MIME type'}), 400

    file_id = document.get('id')
    filename = document.get('filename')
    if not file_id or not filename:
        logging.error("Error: Missing file ID or filename in document message")
        return jsonify({'error': 'Missing file information'}), 400

  # Descargar el archivo en memoria
    file_url = f"https://graph.facebook.com/{Config.WHATSAPP_VERSION}/{file_id}/"
    headers = {"Authorization": f"Bearer {branch.whatsapp_token}"}
    response = requests.get(file_url, headers=headers, stream=True)

    if response.status_code != 200:
        logging.error("Error downloading the file")
        return jsonify({'error': 'File download failed'}), 500

    file_content = io.BytesIO(response.content)  # Cargar el contenido del archivo en memoria

    # Procesar según el tipo de archivo
    if mime_type == 'application/pdf':
        return process_pdf(file_content, branch)
    elif mime_type.startswith('image/'):
        return process_image(file_content, branch)
    elif mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        if update_stock_from_excel(file_content):
            logging.info("Stock updated successfully")
            return jsonify({"message": "Stock updated successfully"}), 200
        else:
            logging.error("Failed to update stock")
            return jsonify({"error": "Failed to update stock"}), 500
    else:
        logging.info("Unsupported file type")
        return jsonify({"error": "Unsupported file type"}), 400
    
    
def handle_file_message(message, branch, branch_cellphone):
    phone_number = message.get('from')
    if not phone_number:
        logging.error("Error: Missing phone number in message")
        return jsonify({'error': 'Missing phone number'}), 400

    if phone_number == branch_cellphone:
        logging.error(f"Error: {phone_number} is not authorized to send files")
        return jsonify({'error': 'Unauthorized sender'}), 401

    # Identificar si es un mensaje de documento o imagen
    document = message.get('document')
    image = message.get('image')
    
    # Validar que haya contenido
    if not document and not image:
        logging.error("Error: No document or image provided in message")
        return jsonify({'error': 'No document or image provided'}), 400

    # Extraer datos comunes
    file_data = document if document else image
    mime_type = file_data.get('mime_type')
    file_id = file_data.get('id')
    filename = file_data.get('filename', 'received_file')

    if not file_id or not mime_type:
        logging.error("Error: Missing file ID or MIME type in message")
        return jsonify({'error': 'Missing file information'}), 400

    # Descargar el archivo desde la API de Facebook
    file_url = f"https://graph.facebook.com/{Config.WHATSAPP_VERSION}/{file_id}"
    headers = {"Authorization": f"Bearer {branch.whatsapp_token}"}

    response = requests.get(file_url, headers=headers)
    if response.status_code != 200:
        logging.error(f"Error downloading the file: {response.status_code}")
        return jsonify({'error': 'File download failed'}), 500

    media_url = response.json().get("url")
    file_response = requests.get(media_url, headers=headers)
    media_content = file_response.content

    logging.info(f"Tipo de archivo recibido: {mime_type}")

    # Procesar según el tipo MIME
    if mime_type == 'application/pdf':
        if is_single_page_pdf(media_content):
            logging.info(f"Received a valid PDF: {filename}")
            return process_pdf(io.BytesIO(media_content), branch)
        else:
            logging.warning(f"PDF has more than one page: {filename}")
            return jsonify({"error": "PDF must contain only one page"}), 400

    elif mime_type.startswith('image/'):
        logging.info(f"Received an image: {filename}")
        return process_image(io.BytesIO(media_content), branch)

    elif mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        if update_stock_from_excel(media_content):
            logging.info("Stock updated successfully")
            return jsonify({"message": "Stock updated successfully"}), 200
        else:
            logging.error("Failed to update stock")
            return jsonify({"error": "Failed to update stock"}), 500

    else:
        logging.warning(f"Unsupported MIME type: {mime_type}")
        return jsonify({"error": "Unsupported file type"}), 400



