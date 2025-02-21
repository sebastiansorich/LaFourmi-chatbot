# src/routes/sale_routes.py
from flask import Blueprint
from src.controllers.sale_controllers import create_sale, get_sales, get_sale, update_sale, delete_sale

sale_bp = Blueprint('sale_bp', __name__)

#sale_bp.route('/sales', methods=['POST'])(create_sale)
#sale_bp.route('/sales', methods=['GET'])(get_sales)
#sale_bp.route('/sales/<id>', methods=['GET'])(get_sale)
#sale_bp.route('/sales/<id>', methods=['PUT'])(update_sale)
#sale_bp.route('/sales/<id>', methods=['DELETE'])(delete_sale)
