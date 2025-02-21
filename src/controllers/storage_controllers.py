from flask import request, jsonify
from ..models.storage import Storage
from .. import db
from ..schemas.storage_schema import storage_schema, storages_schema
import logging
from sqlalchemy.exc import SQLAlchemyError

def create_storage():
    try:
        id_branch = request.json['id_branch']
        name = request.json['name']
        description = request.json.get('description')
        user_register = request.json.get('user_register')
        user_process = request.json.get('user_process')
        process_date = request.json.get('process_date')
        registration_date = request.json.get('registration_date')
        drop_mark = request.json.get('drop_mark')

        new_storage = Storage(id_branch, name, description, user_register, user_process, process_date, registration_date, drop_mark)

        db.session.add(new_storage)
        db.session.commit()

        return storage_schema.jsonify(new_storage)
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

def get_storages():
    try:
        all_storages = Storage.query.all()
        result = storages_schema.dump(all_storages)
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_storage(id_storage):
    try:
        storage = Storage.query.get(id_storage)
        return storage_schema.jsonify(storage)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_storage_by_branch(idBranch):
    try:
        storage = Storage.query.filter_by(id_branch = idBranch).order_by(Storage.id_storage).all()
        return storage
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def update_storage(id_storage):
    try:
        storage = Storage.query.get(id_storage)

        storage.id_branch = request.json['id_branch']
        storage.name = request.json['name']
        storage.description = request.json.get('description')
        storage.user_register = request.json.get('user_register')
        storage.user_process = request.json.get('user_process')
        storage.process_date = request.json.get('process_date')
        storage.registration_date = request.json.get('registration_date')
        storage.drop_mark = request.json.get('drop_mark')

        db.session.commit()

        return storage_schema.jsonify(storage)
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

def delete_storage(id_storage):
    try:
        storage = Storage.query.get(id_storage)
        if not storage:
            return jsonify({"error": "Storage not found"}), 404
    
        storage.drop_mark = True
        db.session.commit()
        return storage_schema.jsonify(storage), 200
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
