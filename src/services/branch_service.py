import logging
from flask import jsonify
from src.models.branch import Branch
import io

from src.services.whatsapp_service import send_whatsapp_message_with_file, upload_file_to_whatsapp

def send_branch_qr_whatsapp(branch_id, whatsappPhoneDestination):
    try:
        # Obtener los datos de la sucursal
        branch = Branch.query.get(branch_id)
        if not branch:
            return jsonify({"error": "Branch not found"}), 404

        if not branch.qr_code_image:
            return jsonify({"error": "QR Code not found for this branch"}), 404

        # Obtener datos necesarios para WhatsApp desde la sucursal
        whatsappToken = branch.whatsapp_token
        whatsappPhoneNumberId = branch.whatsapp_number_id

        if not whatsappToken or not whatsappPhoneNumberId:
            return jsonify({"error": "WhatsApp configuration missing for this branch"}), 400

        # Preparar archivo del QR en memoria
        qr_code_image = io.BytesIO(branch.qr_code_image)
        qr_code_image.seek(0)  # Asegurarse de que el archivo se lea desde el inicio

        # Subir el archivo a WhatsApp
        mimeType = "image/png"
        fileName = f"QR_Branch_{branch_id}.png"
        mediaId = upload_file_to_whatsapp(
            output=qr_code_image,
            fileName=fileName,
            mimeType=mimeType,
            whatsappPhoneNumberId=whatsappPhoneNumberId,
            whatsappToken=whatsappToken
        )

        # Enviar el mensaje con el archivo
        caption = f"Este es el código QR de la sucursal: {branch.name}. 📍 Dirección: {branch.address}"
        send_whatsapp_message_with_file(
            mediaId=mediaId,
            typeDocument="image",
            caption=caption,
            fileName=fileName,
            whatsappPhoneDestination=whatsappPhoneDestination,
            whatsappPhoneNumberId=whatsappPhoneNumberId,
            whatsappToken=whatsappToken
        )

        return jsonify({"message": "QR Code sent successfully via WhatsApp"}), 200

    except Exception as e:
        logging.error(f"Error al enviar el QR por WhatsApp: {e}")
        return jsonify({"error": str(e)}), 500
