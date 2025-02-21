# src/controllers/subtype_business_controller.py

from flask import request, jsonify
from ..models.type_business import SubtypeBusiness
from .. import db
from ..schemas.subtype_business_schema import subtype_business_schema, subtypes_business_schema
import logging
from sqlalchemy.exc import SQLAlchemyError

def create_subtype_business():
    try:
        name = request.json['name']
        type_business_id = request.json['type_business_id']

        new_subtype_business = SubtypeBusiness(name=name, type_business_id=type_business_id)

        db.session.add(new_subtype_business)
        db.session.commit()
        return subtype_business_schema.jsonify(new_subtype_business), 201
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

def get_subtypes_business():
    try:
        all_subtypes_business = SubtypeBusiness.query.all()
        result = subtypes_business_schema.dump(all_subtypes_business)
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_subtype_business(id):
    try:
        subtype_business = SubtypeBusiness.query.get(id)
        if subtype_business is None:
            return jsonify({"error": "Subtype Business not found"}), 404
        return subtype_business_schema.jsonify(subtype_business)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def update_subtype_business(id):
    try:
        subtype_business = SubtypeBusiness.query.get(id)
        if subtype_business is None:
            return jsonify({"error": "Subtype Business not found"}), 404

        data = request.get_json()
        subtype_business.name = data.get('name', subtype_business.name)
        subtype_business.type_business_id = data.get('type_business_id', subtype_business.type_business_id)

        db.session.commit()
        return subtype_business_schema.jsonify(subtype_business)
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

def delete_subtype_business(id):
    try:
        subtype_business = SubtypeBusiness.query.get(id)
        if subtype_business is None:
            return jsonify({"error": "Subtype Business not found"}), 404

        db.session.delete(subtype_business)
        db.session.commit()
        return subtype_business_schema.jsonify(subtype_business)
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