import json
import logging
import openai
import os
import re
from flask import jsonify, request
from src.controllers.branch_controllers import get_branch_by_cellphone, update_branch_by_model, get_context
from src.controllers.product_controllers import get_context_menu_route
from src.controllers.storage_controllers import get_storage_by_branch
from src.controllers.concept_controllers import get_concept_by_value
from src.controllers.client_controller import get_client_by_cellphone, create_client_by_cellphone
from src.helper.vauchers import  handle_file_message
from src.services.order_service import create_order
from src.controllers.order_controllers import delete_order
from src.helper.utils import is_null_or_whitespace
from src.models.conversation import Conversation
from src.services.order_service import create_order, get_order_summary
from src.services.whatsapp_service import send_whatsapp_message
from src.services.stock_service import send_daily_sales_report_whatsapp
from src.config import Config

conversations = {}

def webhook():
    try:
        data = request.get_json()
        if not data:
            logging.error(f"Error: No data received")
            return jsonify({"error":"No data received"}), 400
       
        #logging.info(data)
        for entry in data['entry']:
            for change in entry['changes']:
                branch_cellphone = ""
                if 'metadata' in change['value']:
                    branch_cellphone = change['value']['metadata']['display_phone_number']

                result = get_branch_by_cellphone(branch_cellphone)
                if result is None:
                    logging.error(f"Error: Branch not found: {branch_cellphone}")
                    return jsonify({"error":f"Branch not found: {branch_cellphone}"}), 400
                
                branch = result
                company = result.company

                storage = get_storage_by_branch(branch.id)
                if storage is None:
                    logging.error(f"Error: storage not found: {branch.id} {branch.name}")
                    return jsonify({"error":f"Storage not found: {branch.id} {branch.name}"}), 400

                status_business = branch.status
                #context = get_context_menu(company, storage, get_context(company, branch))
                context = get_context_menu_route(company, storage, get_context(company, branch))
                gpt_model = get_concept_by_value(50, company.model) #50 tipo de modelo chatgpt de concepto

                if gpt_model is None:
                    logging.error(f"Model GPT not found: {company.id} {company.name}")
                    return jsonify({"error:":f"Model GPT not found {company.id} {company.name}"}), 400
                
                if 'messages' in change['value']:
                    for message in change['value']['messages']:
                        if 'text' in message:
                            phone_number = message['from']
                            message_text = message['text']['body']

                            if is_null_or_whitespace(message_text):
                                logging.info(f"Status: empty message")
                                return jsonify({'status' : 'empty message'}), 204
                            message_text = message_text.strip()

                            # verifica que sea un cliente el que envia un mensaje y comprueba si el negocio esta cerrado
                            if phone_number != branch_cellphone and status_business == False:
                                send_whatsapp_message(branch.whatsapp_number_id, branch.whatsapp_token, phone_number, company.close_message)
                                logging.info(f"Status: bussines close")
                                return jsonify({'status': 'business close'}), 200

                            # si es el administrador del negocio, recibe comandos
                            if phone_number == branch_cellphone:
                                message_text = message_text.upper()
                                if message_text == "<ABRIR>" or message_text == "<CERRAR>":
                                    branch.status = message_text == "<ABRIR>"
                                    update_branch_by_model(branch)
                                    logging.info(f"Status: modifyng business state")
                                    return jsonify({"status": "modifyng business state"}), 200
                                if message_text == "<DIARIO>":
                                    response = send_daily_sales_report_whatsapp(branch.company_id, branch.id, branch.phone, branch.whatsapp_number_id, branch.whatsapp_token)
                                    if isinstance(response, tuple):
                                        response_data, status_code = response
                                        if status_code == 500:
                                            logging.error(f"Error al procesar reporte diario")
                                            return jsonify({"error": f"{response_data.json['error']}"}), 500
                                        elif status_code == 200:
                                            logging.info(f"Status: daily report was sent")
                                            return jsonify({"status": f"{response_data.json['status']}"}), 200
                                        else:
                                            logging.error(f"Error no identificado")
                                            return jsonify({"error": "Error no identificado"}), 500
                            
                            # verifica si la empresa ya está en el diccionario
                            if company.id not in conversations:
                                conversations[company.id] = {}
                            
                            # verifica si el número de teléfono ya está en el diccionario de la empresa
                            if phone_number not in conversations[company.id]:
                                conversations[company.id][phone_number] = Conversation()

                            # obtiene la conversación específica
                            conversation = conversations[company.id][phone_number]

                            # Agrega la pregunta actual al historial
                            conversation.add_interaction(ask=message_text, answer="")

                            # Genera los mensajes para el modelo de OpenAI
                            openai.api_key = branch.apikey
                            generated_message = conversation.generate_message_for_model(context)
                            response = openai.chat.completions.create(
                                        model=gpt_model.description, 
                                        messages=generated_message,
                                        temperature=0.5)

                            response_content = response.choices[0].message.content
                            
                            client = get_client_by_cellphone(phone_number)
                            if client is None:
                                logging.info(f"Info: insert new client: {phone_number}")
                                response = create_client_by_cellphone(phone_number)
                                if isinstance(response, tuple) and response[1] == 500:
                                    return jsonify({"error": f"{response[0].json['error']}"}), 500
                                client = response
                                logging.info(f"Info: new client registered {phone_number}")

                            id_pedido = 0
                            # Lista de patrones para buscar, junto con las funciones y sus parámetros
                            actions = [
                                {
                                    'tag': 'PEDIDO',
                                    'handler': create_order,
                                    'params': (company, branch, client)
                                },
                                {
                                    'tag': 'CANCELAR',
                                    'handler': delete_order,
                                    'params': ()  # Ejemplo con parámetros diferentes
                                }
                            ]
                            # Iterar sobre los patrones y procesar
                            for action in actions:
                                patron = rf'<{action["tag"]}>(.*?)</{action["tag"]}>'
                                coincidencia = re.search(patron, response_content, re.DOTALL)
                                if coincidencia:
                                    json_texto = coincidencia.group(1).strip()
                                    datos = json.loads(json_texto.lower())
                                    # Desempaquetar los parámetros específicos para cada función
                                    branch_id = branch.id
                                    response_action = action['handler'](*action['params'], datos)
                                    if isinstance(response, tuple) and response[1] == 500:
                                        return jsonify({"error": f"{response[0].json['error']}"}), 400
                                    if isinstance(response, tuple) and response[1] == 409:
                                        response_content = f"{response[0].json['error']}, elige otro producto o retira de tu lista para proseguir con tu pedido."
                                        break
                                    
                                    # Llamar a la función correspondiente con los parámetros
                                    response_action = action['handler'](*action['params'], data)

                                    # Manejo unificado de respuestas
                                    if isinstance(response_action, tuple):
                                        response_data, status_code = response_action
                                        if status_code == 409: #InsuficcientStockError
                                            response_content = f"{response_data.json['error']}, elige otro producto o cambia tu orden para proseguir con tu pedido."
                                            break
                                        if status_code == 432: #UnauthorizedError
                                            response_content = f"{response_data.json['error']}, elige otro codigo de pedido para cancelar."
                                            break
                                        if status_code == 433: #DataProccesedError
                                            response_content = f"{response_data.json['error']}"
                                            break
                                        if status_code == 500: #InternalServerError
                                            return jsonify({"error": response_data.json['error']}), 500
                                   
                                    # Procesar el mensaje según el tipo de acción
                                    if action["tag"] == "PEDIDO":
                                            id_order = response_action.json['id_order']
                                            logging.info(f"id_{action['tag'].lower()}: {id_order}")
                                            summary = get_order_summary(id_order, client)
                                            send_whatsapp_message(branch.whatsapp_number_id, branch.whatsapp_token, branch.phone, summary)
                                            mensaje = f"Su pedido ha sido registrado con código: *{id_order}*"
                                    elif action["tag"] ==  "CANCELAR":
                                            id_order = response_action.json['id_order']
                                            mensaje = f"Su pedido con código: *{id_order}* ha sido cancelado."
                                    else:
                                            mensaje = ""

                                    # Si se generó un mensaje, agregarlo a la respuesta
                                    if mensaje:
                                        response_content = f"{response_content}{os.linesep}{mensaje}"
                                    # Eliminar el contenido del tag procesado
                                    response_content = re.sub(patron, '', response_content, flags=re.DOTALL).strip()
                            
                            assist_human = False
                            if (response.choices[0].message.content.__contains__(Config.ASSIST_HUMAN_TAG)):
                                assist_human = True
                                response.choices[0].message.content = response.choices[0].message.content.replace(Config.ASSIST_HUMAN_TAG, "")

                            # Actualiza la última interacción con la respuesta generada
                            conversation.historial[-1]['respuesta'] = response_content

                            # Envía la respuesta por WhatsApp
                            send_whatsapp_message(branch.whatsappPhoneNumberId, branch.whatsapp_token, phone_number, response_content)

                            # assist human - sistema de colas, fase inicial
                            if (assist_human):
                                message_human = f"El número +{phone_number} solicita asistencia humana"
                                send_whatsapp_message(branch.assist_human_number, message_human)
                        #manejo de documentos
                        # 
                        #        
                        elif 'document' or 'image' in message:
                            response = handle_file_message(message, branch, branch_cellphone)                        
                            return response
                        #
                        #
                elif 'statuses' in change['value']:
                    for status in change['value']['statuses']:
                        print(f"Message status update: {status}")
                
        return jsonify({'status': 'success'}), 200
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def verify_webhook():
    try:
        verify_token = Config.VERIFY_TOKEN_WEBHOOK
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == verify_token:
            return challenge, 200
        else:
            return "Verification token mismatch", 403
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500
