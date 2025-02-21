from flask import Blueprint
from src.controllers.storage_controllers import create_storage, get_storages, get_storage, update_storage, delete_storage

storage_bp = Blueprint('storage_bp', __name__)

#storage_bp.route('/storages', methods=['POST'])(create_storage)
#storage_bp.route('/storages', methods=['GET'])(get_storages)
#storage_bp.route('/storages/<id_storage>', methods=['GET'])(get_storage)
#storage_bp.route('/storages/<id_storage>', methods=['PUT'])(update_storage)
#storage_bp.route('/storages/<id_storage>', methods=['DELETE'])(delete_storage)
