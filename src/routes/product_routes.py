from flask import Blueprint
from src.controllers.product_controllers import get_context_menu_route, create_product, get_products, get_product, update_product, delete_product, get_context_menu

product_bp = Blueprint('product_bp', __name__)

#product_bp.route('/products', methods=['POST'])(create_product)
#product_bp.route('/products', methods=['GET'])(get_products)
#product_bp.route('/products/<id_product>', methods=['GET'])(get_product)
#product_bp.route('/products/<id_product>', methods=['PUT'])(update_product)
#product_bp.route('/products/<id_product>', methods=['DELETE'])(delete_product)
#product_bp.route('/context-menuE', methods=['GET'])(get_context_menu)
#product_bp.route('/context-menu', methods=['GET'])(get_context_menu_route)