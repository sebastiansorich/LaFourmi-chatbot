from flask import request, jsonify
from datetime import datetime
from ..models.client import Client
from .. import db
from ..schemas.client_schema import client_schema, clients_schema
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_

def create_client():
    try:
        data = request.get_json()
        cellphone = data.get('cellphone')
        address = data.get('address')
        url_maps = data.get('url_maps')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        status = data.get('status')
        name_client = data.get('name_client')
        user_register = data.get('user_register')
        user_process = data.get('user_process')
        process_date = data.get('process_date')
        registration_date = data.get('registration_date')
        drop_mark = data.get('drop_mark', False)

        # Verificar si el cliente ya existe por número de celular
        existing_client = Client.query.filter_by(cellphone=cellphone).first()
        if existing_client:
            return jsonify({"error": "Client with this cellphone already exists"}), 400

        new_client = Client(
            cellphone=cellphone,
            address=address,
            url_maps=url_maps,
            latitude=latitude,
            longitude=longitude,
            status=status,
            name_client=name_client,
            user_register=user_register,
            user_process=user_process,
            process_date=process_date,
            registration_date=registration_date,
            drop_mark=drop_mark
        )

        db.session.add(new_client)
        db.session.commit()
        return client_schema.jsonify(new_client)
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

def create_client_by_cellphone(cellphone):
    try:
        # Verificar si el cliente ya existe por número de celular
        existing_client = Client.query.filter_by(cellphone=cellphone).first()
        if existing_client:
            return jsonify({"info": "Client with this cellphone already exists"}), 400

        today = datetime.now()
        new_client = Client(
            cellphone=cellphone,
            address="",
            url_maps="",
            latitude=0,
            longitude=0,
            status=0,
            name_client="",
            user_register=1,
            user_process=1,
            process_date=today,
            registration_date=today,
            drop_mark=0
        )

        db.session.add(new_client)
        db.session.commit()
        return new_client
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

def get_clients():
    try:
        all_clients = Client.query.all()
        result = clients_schema.dump(all_clients)
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_client(id):
    try:
        client = Client.query.get(id)
        if not client:
            return jsonify({"error": "Client not found"}), 404
        return client_schema.jsonify(client)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500
    
def get_client_by_cellphone(cellphone, dropMark = False):
    try:
        client = Client.query.filter(and_(Client.cellphone == cellphone, Client.drop_mark == dropMark)).first()
        return client
    except Exception as e:
        logging.error(f"An unexpected error ocurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def update_client(id):
    try:
        client = Client.query.get(id)
        if not client:
            return jsonify({"error": "Client not found"}), 404

        data = request.get_json()
        client.cellphone = data.get('cellphone', client.cellphone)
        client.address = data.get('address', client.address)
        client.url_maps = data.get('url_maps', client.url_maps)
        client.latitude = data.get('latitude', client.latitude)
        client.longitude = data.get('longitude', client.longitude)
        client.status = data.get('status', client.status)
        client.name_client = data.get('name_client', client.name_client)
        client.user_register = data.get('user_register', client.user_register)
        client.user_process = data.get('user_process', client.user_process)
        client.process_date = data.get('process_date', client.process_date)
        client.registration_date = data.get('registration_date', client.registration_date)
        client.drop_mark = data.get('drop_mark', client.drop_mark)

        db.session.commit()
        return client_schema.jsonify(client)
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

def delete_client(id):
    try:
        client = Client.query.get(id)
        if not client:
            return jsonify({"error": "Client not found"}), 404

        client.drop_mark = True
        db.session.commit()
        return client_schema.jsonify(client), 200
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
