from flask import request, jsonify
from ..models.company import Company
from .. import db
from ..schemas.company_schema import company_schema, companies_schema
from sqlalchemy import and_
import logging
from sqlalchemy.exc import SQLAlchemyError

def create_company():
    try:
        name = request.json['name']
        type_business_id = request.json['type_business_id']
        subtype_business_id = request.json['subtype_business_id']
        cellphone_master = request.json.get('cellphone_master', None)
        nit = request.json.get('nit', None)
        name_receipt = request.json.get('name_receipt', None)
        user_register = request.json.get('user_register', None)
        user_process = request.json.get('user_process', None)
        process_date = request.json.get('process_date', None)
        registration_date = request.json.get('registration_date', None)
        drop_mark = request.json.get('drop_mark', False)
        context = request.json.get('context', None)
        close_message = request.json.get('close_message', None)
        model = request.json.get('model', None)  # Agregado aquí

        new_company = Company(
            name=name,
            type_business_id=type_business_id,
            subtype_business_id=subtype_business_id,
            cellphone_master=cellphone_master,
            nit=nit,
            name_receipt=name_receipt,
            user_register=user_register,
            user_process=user_process,
            process_date=process_date,
            registration_date=registration_date,
            drop_mark=drop_mark,
            context=context,
            close_message=close_message,
            model=model  # Inicialización de la nueva columna
        )

        db.session.add(new_company)
        db.session.commit()
        return company_schema.jsonify(new_company), 201
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
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

def update_company(id):
    try:
        company = Company.query.get(id)
        if company is None:
            return jsonify({"error": "Company not found"}), 404

        data = request.get_json()

        company.name = data.get('name', company.name)
        company.type_business_id = data.get('type_business_id', company.type_business_id)
        company.subtype_business_id = data.get('subtype_business_id', company.subtype_business_id)
        company.cellphone_master = data.get('cellphone_master', company.cellphone_master)
        company.nit = data.get('nit', company.nit)
        company.name_receipt = data.get('name_receipt', company.name_receipt)
        company.user_register = data.get('user_register', company.user_register)
        company.user_process = data.get('user_process', company.user_process)
        company.process_date = data.get('process_date', company.process_date)
        company.registration_date = data.get('registration_date', company.registration_date)
        company.drop_mark = data.get('drop_mark', company.drop_mark)
        company.context = data.get('context', company.context)
        company.close_message = data.get('close_message', company.close_message)
        company.model = data.get('model', company.model)  # Actualización de la nueva columna

        db.session.commit()
        return company_schema.jsonify(company)
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
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

def get_companies():
    try:
        all_companies = Company.query.all()
        result = companies_schema.dump(all_companies)
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_company(id):
    try:
        company = Company.query.get(id)
        if company is None:
            return jsonify({"error": "Company not found"}), 404
        return company_schema.jsonify(company)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_company_by_cellphone(cellphone, dropMark = False):
    try:
        company = Company.query.filter(and_(Company.cellphone_master == cellphone, Company.drop_mark == dropMark)).first()
        if company is None:
            return jsonify({"error": "Company not found"}), 404
        return company_schema.jsonify(company)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def delete_company(id):
    try:
        company = Company.query.get(id)
        if company is None:
            return jsonify({"error": "Company not found"}), 404

        company.drop_mark = True
        db.session.commit()
        return company_schema.jsonify(company), 200
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