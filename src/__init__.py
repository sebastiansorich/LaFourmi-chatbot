# src/__init__.py

import os
from flask import jsonify, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from logging_config import setup_logging

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

#UPLOAD_FOLDER = 'uploads/' #declaramos un nombre para la carpeta de archivos subidos

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config.Config')
    
 #   app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

#    if not os.path.exists(UPLOAD_FOLDER): #creamos uploads si no existe
#        os.makedirs(UPLOAD_FOLDER)
  # configurar logging
    setup_logging()
    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Importar modelos dentro del contexto de la aplicación
    with app.app_context():
        from src.models.client import Client 
        from src.models.company import Company
        from src.models.branch import Branch
        from src.models.storage import Storage
        from src.models.product import Product
        from src.models.stock import Stock
        from src.models.concept import Concept
        from src.models.order import Order
        from src.models.order_detail import OrderDetail
        from src.models.sale import Sale
        from src.models.sale_detail import SaleDetail
        from src.models.type_business import TypeBusiness
        from .models.product_type import ProductType, ProductSubtype
        #db.create_all()
        
        # Nota: Elimina la línea `db.create_all()` si estás utilizando migraciones

    # Importar y registrar blueprints
    from src.routes.branch_routes import branch_bp
    from src.routes.company_routes import company_bp
    from src.routes.storage_routes import storage_bp 
    from src.routes.product_routes import product_bp 
    from src.routes.stock_routes import stock_bp
    from src.routes.concept_routes import concept_bp
    from src.routes.order_routes import order_bp
    from src.routes.sales_routes import sale_bp
    from src.routes.client_routes import client_bp
    from src.routes.webhook_route import webhook_bp
    from src.routes.type_business_routes import type_business_bp
    from src.routes.subtype_business_routes import subtype_business_bp
    from src.routes.product_type_routes import product_type_bp
    from src.routes.product_subtype_routes import product_subtype_bp
    

    app.register_blueprint(client_bp)
    app.register_blueprint(branch_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(storage_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(concept_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(sale_bp)
    app.register_blueprint(webhook_bp)
    app.register_blueprint(type_business_bp)
    app.register_blueprint(subtype_business_bp)
    app.register_blueprint(product_type_bp)
    app.register_blueprint(product_subtype_bp)

    return app
