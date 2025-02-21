# src/routes/product_subtype_routes.py

from flask import Blueprint
from src.controllers.product_subtype_controller import create_product_subtype, get_product_subtypes, get_product_subtype, update_product_subtype, delete_product_subtype

product_subtype_bp = Blueprint('product_subtype_bp', __name__)

#product_subtype_bp.route('/product_subtypes', methods=['POST'])(create_product_subtype)
#product_subtype_bp.route('/product_subtypes', methods=['GET'])(get_product_subtypes)
#product_subtype_bp.route('/product_subtypes/<id>', methods=['GET'])(get_product_subtype)
#product_subtype_bp.route('/product_subtypes/<id>', methods=['PUT'])(update_product_subtype)
#product_subtype_bp.route('/product_subtypes/<id>', methods=['DELETE'])(delete_product_subtype)
