from flask import Blueprint
from src.controllers.webhook_controllers import webhook, verify_webhook

webhook_bp = Blueprint('webhook_bp', __name__)

webhook_bp.route('/webhook', methods=['POST'])(webhook)
webhook_bp.route('/webhook', methods=['GET'])(verify_webhook)