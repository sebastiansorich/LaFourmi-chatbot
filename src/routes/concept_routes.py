# src/routes/concept_routes.py
from flask import Blueprint
from src.controllers.concept_controllers import create_concept, get_concepts, get_concept, update_concept, delete_concept

concept_bp = Blueprint('concept_bp', __name__)

#concept_bp.route('/concepts', methods=['POST'])(create_concept)
#concept_bp.route('/concepts', methods=['GET'])(get_concepts)
#concept_bp.route('/concepts/<id>', methods=['GET'])(get_concept)
#concept_bp.route('/concepts/<id>', methods=['PUT'])(update_concept)
#concept_bp.route('/concepts/<id>', methods=['DELETE'])(delete_concept)
