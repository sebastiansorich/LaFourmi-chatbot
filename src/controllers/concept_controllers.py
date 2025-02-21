# src/controllers/concept_controllers.py
from flask import request, jsonify
from ..models.concept import Concept
from .. import db
from ..schemas.concept_schema import concept_schema, concepts_schema
from sqlalchemy import and_
import logging
from sqlalchemy.exc import SQLAlchemyError

def create_concept():
    try:
        description = request.json['description']
        concepts_type = request.json.get('concepts_type', None)
        value = request.json.get('value', None)

        new_concept = Concept(description=description, concepts_type=concepts_type, value=value)

        db.session.add(new_concept)
        db.session.commit()

        return concept_schema.jsonify(new_concept)
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

def get_concepts():
    try:
        all_concepts = Concept.query.all()
        result = concepts_schema.dump(all_concepts)
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_concept(id):
    try:
        concept = Concept.query.get(id)
        return concept_schema.jsonify(concept)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_concept_by_value(type, value):
    try:
        concept = Concept.query.filter(and_(Concept.concepts_type == type, Concept.value == value )).first()
        return concept
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def update_concept(id):
    try:
        concept = Concept.query.get(id)

        concept.description = request.json.get('description', concept.description)
        concept.concepts_type = request.json.get('concepts_type', concept.concepts_type)
        concept.value = request.json.get('value', concept.value)

        db.session.commit()

        return concept_schema.jsonify(concept)
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

def delete_concept(id):
    try:
        concept = Concept.query.get(id)
        db.session.delete(concept)
        db.session.commit()
        return concept_schema.jsonify(concept)
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
