from flask import Blueprint
from src.controllers.company_controllers import create_company, get_companies, get_company, update_company, delete_company, get_company_by_cellphone

company_bp = Blueprint('company_bp', __name__)

#company_bp.route('/companies', methods=['POST'])(create_company)
#company_bp.route('/companies', methods=['GET'])(get_companies)
#company_bp.route('/companies/<id>', methods=['GET'])(get_company)
#company_bp.route('/companies/<id>', methods=['PUT'])(update_company)
#company_bp.route('/companies/<id>', methods=['DELETE'])(delete_company)
#company_bp.route('/companies/<cellphone>', methods=['GET'])(get_company_by_cellphone)
