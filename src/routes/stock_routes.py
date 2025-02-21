# src/routes/stock_routes.py
from flask import Blueprint
from src.controllers.stock_controllers import create_stock, get_stocks, get_stock, update_stock, delete_stock

stock_bp = Blueprint('stock_bp', __name__)

#stock_bp.route('/stocks', methods=['POST'])(create_stock)
#stock_bp.route('/stocks', methods=['GET'])(get_stocks)
#stock_bp.route('/stocks/<id>', methods=['GET'])(get_stock)
#stock_bp.route('/stocks/<id>', methods=['PUT'])(update_stock)
#stock_bp.route('/stocks/<id>', methods=['DELETE'])(delete_stock)

