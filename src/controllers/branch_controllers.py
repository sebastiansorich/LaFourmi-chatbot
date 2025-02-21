from flask import request, jsonify, send_file
import io
from ..models.branch import Branch
from .. import db
from ..schemas.branch_schema import branch_schema, branches_schema
from sqlalchemy import and_
import logging
from sqlalchemy.exc import SQLAlchemyError

def create_branch():
    try:
        company_id = request.json['company_id']
        name = request.json['name']
        address = request.json['address']
        phone = request.json['phone']
        manager = request.json['manager']
        status = request.json['status']
        operating_hours = request.json['operating_hours']
        name_contact = request.json['name_contact']
        position_link = request.json['position_link']
        user_register = request.json['user_register']
        user_process = request.json['user_process']
        process_date = request.json['process_date']
        registration_date = request.json['registration_date']
        drop_mark = request.json['drop_mark']
        apikey = request.json.get('apikey')
        whatsapp_token = request.json.get('whatsapp_token')
        whatsapp_number_id = request.json.get('whatsapp_number_id')
        assist_human_number = request.json.get('assist_human_number')

        new_branch = Branch(company_id=company_id, name=name, address=address, phone=phone,
                            manager=manager, status=status, operating_hours=operating_hours,
                            name_contact=name_contact, position_link=position_link,
                            user_register=user_register, user_process=user_process,
                            process_date=process_date, registration_date=registration_date,
                            drop_mark=drop_mark,apikey=apikey, whatsapp_token=whatsapp_token, 
                            whatsapp_number_id=whatsapp_number_id,assist_human_number=assist_human_number)

        db.session.add(new_branch)
        db.session.commit()

        result = branch_schema.dump(new_branch)
        return jsonify(result)
    except ValueError as e:
        db.session.rollback()
        logging.error(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"SQLAlchemyError: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred, {str(e)}"}), 500
    finally:
        db.session.close()

def get_branches():
    try:
        all_branches = Branch.query.all()
        result = branches_schema.dump(all_branches)
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500
        
def get_branch(id):
    try:
        branch = Branch.query.get(id)
        result = branch_schema.dump(branch)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error no esperado al crear el branch: {e}")
        return jsonify({"error" : f"An unexpected error ocurred:, {str(e)}"}), 500

def get_branch_by_cellphone(cellphone, dropMark = False):
    try:
        branch = Branch.query.filter(and_(Branch.phone == cellphone, Branch.drop_mark == dropMark)).first()
        return branch
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def update_branch(id):
    try:        
        branch = Branch.query.get(id)

        branch.name = request.json['name']
        branch.address = request.json['address']
        branch.phone = request.json['phone']
        branch.manager = request.json['manager']
        branch.status = request.json['status']
        branch.operating_hours = request.json['operating_hours']
        branch.name_contact = request.json['name_contact']
        branch.position_link = request.json['position_link']
        branch.user_register = request.json['user_register']
        branch.user_process = request.json['user_process']
        branch.process_date = request.json['process_date']
        branch.registration_date = request.json['registration_date']
        branch.drop_mark = request.json['drop_mark']
        branch.apikey = request.json.get('apikey')
        branch.whatsapp_token = request.json.get('whatsapp_token')
        branch.whatsapp_number_id = request.json.get('whatsapp_number_id')
        branch.assist_human_number = request.json.get('assist_human_number')

        db.session.commit()

        result = branch_schema.dump(branch)
        return jsonify(result)
    
    except ValueError as e:
        db.session.rollback()
        logging.error(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"SQLAlchemyError: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred, {str(e)}"}), 500
    finally:
        db.session.close()

def update_branch_by_model(data):
    try:
        branch = Branch.query.get(data.id)#hola jaja, #ehhh que hora te conectaste??

        branch.name = data.name
        branch.address = data.address
        branch.phone = data.phone
        branch.manager = data.manager
        branch.status = data.status
        branch.operating_hours = data.operating_hours
        branch.name_contact = data.name_contact
        branch.position_link = data.position_link
        branch.user_register = data.user_register
        branch.user_process = data.user_process
        branch.process_date = data.process_date
        branch.registration_date = data.registration_date
        branch.drop_mark = data.drop_mark
        branch.apikey = data.apikey
        branch.whatsapp_token = data.whatsapp_token
        branch.whatsapp_number_id = data.whatsapp_number_id
        branch.assist_human_number = data.assist_human_number

        db.session.commit()

        result = branch_schema.dump(branch)
        return jsonify(result)
    except ValueError as e:
        db.session.rollback()
        logging.error(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"SQLAlchemyError: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred, {str(e)}"}), 500
    finally:
        db.session.close()

def delete_branch(id):
    branch = Branch.query.get(id)
    if not branch: 
        return jsonify({"message": "Branch not found"}), 404
    
    try:
        branch.drop_mark = True
        db.session.commit()
        result = branch_schema.dump(branch)
        return jsonify(result), 200
    except ValueError as e:
        db.session.rollback()
        logging.error(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"SQLAlchemyError: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred, {str(e)}"}), 500
    finally:
        db.session.close()

def get_context(company, branch):
    try:
        context = company.context
        context = f"""{context} 
                Horario de atención: 
                {branch.operating_hours}
                Dirección:
                {branch.address}
                Posición geográfica en google maps:
                {branch.position_link}"""
        return context
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred, {str(e)}"}), 500
    
def update_branch_qr_code(id):
    try:
        branch = Branch.query.get(id)
        if not branch:
            return jsonify({"error": "Branch not found"}), 404

        # Obtener la imagen del request
        qr_code_image = request.files.get('qr_code_image')
        if not qr_code_image:
            return jsonify({"error": "QR Code image is required"}), 400

        # Guardar la imagen como binario en la base de datos
        branch.qr_code_image = qr_code_image.read()

        db.session.commit()

        result = branch_schema.dump(branch)
        return jsonify({"message": "QR Code updated successfully", "branch": result}), 200

    except ValueError as e:
        db.session.rollback()
        logging.error(f"ValueError: {e}")
        return jsonify({"error": "Invalid data provided"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"SQLAlchemyError: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": f"An unexpected error occurred, {str(e)}"}), 500
    finally:
        db.session.close()

def get_branch_qr_code(id):
    try:
        branch = Branch.query.get(id)
        if not branch or not branch.qr_code_image:
            return jsonify({"error": "QR Code image not found"}), 404

        # Decodificar la imagen binaria desde la base de datos
        qr_code_image = io.BytesIO(branch.qr_code_image)

        # Enviar la imagen como respuesta
        return send_file(qr_code_image, mimetype='image/png', as_attachment=False)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": f"An unexpected error occurred, {str(e)}"}), 500
