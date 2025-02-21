# src/controllers/product_subtype_controller.py

from flask import request, jsonify
from ..models.product_type import ProductSubtype  # Updated import
from .. import db
from ..schemas.products_subtype_schema import product_subtype_schema, product_subtypes_schema  # Updated imports
import logging
from sqlalchemy.exc import SQLAlchemyError

def create_product_subtype():
    try:
        name = request.json['name']
        product_type_id = request.json['product_type_id']

        new_product_subtype = ProductSubtype(name=name, product_type_id=product_type_id)  # Updated class name

        db.session.add(new_product_subtype)
        db.session.commit()
        return product_subtype_schema.jsonify(new_product_subtype), 201  # Updated schema
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

def get_product_subtypes():
    try:
        all_product_subtypes = ProductSubtype.query.all()  # Updated query
        result = product_subtypes_schema.dump(all_product_subtypes)  # Updated schema
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_product_subtype(id):
    try:
        product_subtype = ProductSubtype.query.get(id)  # Updated query
        if product_subtype is None:
            return jsonify({"error": "Product Subtype not found"}), 404
        return product_subtype_schema.jsonify(product_subtype)  # Updated schema
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def update_product_subtype(id):
    try:
        product_subtype = ProductSubtype.query.get(id)  # Updated query
        if product_subtype is None:
            return jsonify({"error": "Product Subtype not found"}), 404

        data = request.get_json()
        product_subtype.name = data.get('name', product_subtype.name)
        product_subtype.product_type_id = data.get('product_type_id', product_subtype.product_type_id)
    
        db.session.commit()
        return product_subtype_schema.jsonify(product_subtype)  # Updated schema
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

def delete_product_subtype(id):
    try:
        product_subtype = ProductSubtype.query.get(id)  # Updated query
        if product_subtype is None:
            return jsonify({"error": "Product Subtype not found"}), 404

        db.session.delete(product_subtype)
        db.session.commit()
        return product_subtype_schema.jsonify(product_subtype)  # Updated schema
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
