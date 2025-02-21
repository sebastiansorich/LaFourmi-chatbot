#src/routes/type_business_routes.py

from flask import Blueprint
from src.controllers.type_business_controller import create_type_business, get_types_business, get_type_business, update_type_business, delete_type_business

type_business_bp = Blueprint('type_business_bp', __name__)

#type_business_bp.route('/type_business', methods=['POST'])(create_type_business)
#type_business_bp.route('/type_business', methods=['GET'])(get_types_business)
#type_business_bp.route('/type_business/<id>', methods=['GET'])(get_type_business)
#type_business_bp.route('/type_business/<id>', methods=['PUT'])(update_type_business)
#type_business_bp.route('/type_business/<id>', methods=['DELETE'])(delete_type_business)
