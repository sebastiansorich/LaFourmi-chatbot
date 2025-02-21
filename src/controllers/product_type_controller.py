# src/controllers/product_type_controller.py

from flask import request, jsonify
from ..models.product_type import ProductType
from .. import db
from ..schemas.product_type_schema import product_type_schema, product_types_schema
import logging
from sqlalchemy.exc import SQLAlchemyError

def create_product_type():
    try:
        name = request.json['name']
        new_product_type = ProductType(name=name)

        db.session.add(new_product_type)
        db.session.commit()
        return product_type_schema.jsonify(new_product_type), 201
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

def get_product_types():
    try:
        all_product_types = ProductType.query.all()
        result = product_types_schema.dump(all_product_types)
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_product_type(id):
    try:
        product_type = ProductType.query.get(id)
        if product_type is None:
            return jsonify({"error": "Product Type not found"}), 404
        return product_type_schema.jsonify(product_type)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def update_product_type(id):
    try:
        product_type = ProductType.query.get(id)
        if product_type is None:
            return jsonify({"error": "Product Type not found"}), 404

        data = request.get_json()
        product_type.name = data.get('name', product_type.name)

        db.session.commit()
        return product_type_schema.jsonify(product_type)
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

def delete_product_type(id):
    try:
        product_type = ProductType.query.get(id)
        if product_type is None:
            return jsonify({"error": "Product Type not found"}), 404

        db.session.delete(product_type)
        db.session.commit()
        return product_type_schema.jsonify(product_type)
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
