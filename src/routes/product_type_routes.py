# src/routes/product_type_routes.py

from flask import Blueprint
from src.controllers.product_type_controller import create_product_type, get_product_types, get_product_type, update_product_type, delete_product_type

product_type_bp = Blueprint('product_type_bp', __name__)

#product_type_bp.route('/product_types', methods=['POST'])(create_product_type)
#product_type_bp.route('/product_types', methods=['GET'])(get_product_types)
#product_type_bp.route('/product_types/<id>', methods=['GET'])(get_product_type)
#product_type_bp.route('/product_types/<id>', methods=['PUT'])(update_product_type)
#product_type_bp.route('/product_types/<id>', methods=['DELETE'])(delete_product_type)
