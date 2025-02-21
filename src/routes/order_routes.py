# src/routes/order_routes.py
from flask import Blueprint
from src.controllers.order_controllers import create_order, get_orders, get_order, update_order, delete_order

order_bp = Blueprint('order_bp', __name__)

#order_bp.route('/orders', methods=['POST'])(create_order)
#order_bp.route('/orders', methods=['GET'])(get_orders)
#order_bp.route('/orders/<id>', methods=['GET'])(get_order)
#order_bp.route('/orders/<id>', methods=['PUT'])(update_order)
#order_bp.route('/orders/<id>', methods=['DELETE'])(delete_order)
