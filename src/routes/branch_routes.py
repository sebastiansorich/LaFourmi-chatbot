from flask import Blueprint
from src.controllers.branch_controllers import create_branch, get_branches, get_branch, update_branch, delete_branch, get_branch_by_cellphone, update_branch_qr_code, get_branch_qr_code

branch_bp = Blueprint('branch_bp', __name__)

#branch_bp.route('/branches', methods=['POST'])(create_branch)
branch_bp.route('/branches', methods=['GET'])(get_branches)
#branch_bp.route('/branches/<id>', methods=['GET'])(get_branch)
#branch_bp.route('/branches/<id>', methods=['PUT'])(update_branch)
#branch_bp.route('/branches/<id>', methods=['DELETE'])(delete_branch)
#branch_bp.route('/branches/<cellphone>', methods=['GET'])(get_branch_by_cellphone)
#branch_bp.route('/branches/<id>/qrimage', methods=['POST'])(update_branch_qr_code)
#branch_bp.route('/branches/<id>/qrimage', methods=['GET'])(get_branch_qr_code)
