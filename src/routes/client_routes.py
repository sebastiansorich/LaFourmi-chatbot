# src/routes/client_routes.py
from flask import Blueprint
from ..controllers.client_controller import create_client, get_clients, get_client, update_client, delete_client

client_bp = Blueprint('clients', __name__)

#client_bp.route('/clients', methods=['POST'])(create_client)
#client_bp.route('/clients', methods=['GET'])(get_clients)
#client_bp.route('/clients/<int:id>', methods=['GET'])(get_client)
#client_bp.route('/clients/<int:id>', methods=['PUT'])(update_client)
#client_bp.route('/clients/<int:id>', methods=['DELETE'])(delete_client)
