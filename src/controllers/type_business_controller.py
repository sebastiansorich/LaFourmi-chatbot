# src/controllers/type_business_controller.py

from flask import request, jsonify
from ..models.type_business import TypeBusiness
from .. import db
from ..schemas.type_business_schema import type_business_schema, types_business_schema
import logging
from sqlalchemy.exc import SQLAlchemyError

def create_type_business():
    try:
        name = request.json['name']
        new_type_business = TypeBusiness(name=name)

        db.session.add(new_type_business)
        db.session.commit()
        return type_business_schema.jsonify(new_type_business), 201
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

def get_types_business():
    try:
        all_types_business = TypeBusiness.query.all()
        result = types_business_schema.dump(all_types_business)
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_type_business(id):
    try:
        type_business = TypeBusiness.query.get(id)
        if type_business is None:
            return jsonify({"error": "Type Business not found"}), 404
        return type_business_schema.jsonify(type_business)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def update_type_business(id):
    try:
        type_business = TypeBusiness.query.get(id)
        if type_business is None:
            return jsonify({"error": "Type Business not found"}), 404

        data = request.get_json()
        type_business.name = data.get('name', type_business.name)

        db.session.commit()
        return type_business_schema.jsonify(type_business)
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

def delete_type_business(id):
    try:
        type_business = TypeBusiness.query.get(id)
        if type_business is None:
            return jsonify({"error": "Type Business not found"}), 404
    
        db.session.delete(type_business)
        db.session.commit()
        return type_business_schema.jsonify(type_business)
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
