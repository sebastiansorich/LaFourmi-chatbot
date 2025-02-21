# src/routes/subtype_business_routes.py

from flask import Blueprint
from src.controllers.subtype_business_controller import create_subtype_business, get_subtypes_business, get_subtype_business, update_subtype_business, delete_subtype_business

subtype_business_bp = Blueprint('subtype_business_bp', __name__)

#subtype_business_bp.route('/subtype_business', methods=['POST'])(create_subtype_business)
#subtype_business_bp.route('/subtype_business', methods=['GET'])(get_subtypes_business)
#subtype_business_bp.route('/subtype_business/<id>', methods=['GET'])(get_subtype_business)
#subtype_business_bp.route('/subtype_business/<id>', methods=['PUT'])(update_subtype_business)
#subtype_business_bp.route('/subtype_business/<id>', methods=['DELETE'])(delete_subtype_business)
