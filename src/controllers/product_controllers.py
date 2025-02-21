from flask import request, jsonify
from ..models.product import Product
from .. import db
from ..schemas.product_schema import product_schema, products_schema
from src.models.company import Company
from src.models.storage import Storage
from src.models.product_type import ProductSubtype
from src.models.stock import Stock
from sqlalchemy import and_
import logging
from sqlalchemy.exc import SQLAlchemyError
import os

def create_product():
    try:
        id_company = request.json['id_company']
        product_type_id = request.json['product_type_id']  # Updated key
        product_subtype_id = request.json['product_subtype_id']  # Updated key
        description = request.json['description']
        unit_of_measure = request.json['unit_of_measure']
        price = request.json['price']
        status = request.json['status']
        user_register = request.json.get('user_register')
        user_process = request.json.get('user_process')
        process_date = request.json.get('process_date')
        registration_date = request.json.get('registration_date')
        negative_stock = request.json.get('negative_stock')
        drop_mark = request.json.get('drop_mark')

        new_product = Product(id_company, product_type_id, product_subtype_id, description, unit_of_measure, price, status, user_register, user_process, process_date, registration_date, negative_stock, drop_mark)

        db.session.add(new_product)
        db.session.commit()

        return product_schema.jsonify(new_product)
    except ValueError as e:
        db.session.rollback()
        logging.error(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"SQLAlchemyError: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

def get_products():
    try:
        all_products = Product.query.all()
        result = products_schema.dump(all_products)
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_product(id_product):
    try:
        product = Product.query.get(id_product)
        if product is None:
            return jsonify({"error": "Product not found"}), 404
        return product_schema.jsonify(product)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_product_by_company(idCompany):
    try:
        products = Product.query.filter(Product.id_company == idCompany
                                        ).order_by(Product.product_type_id, Product.id_product
                                        ).all()
        return products
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def update_product(id_product):
    try:
        product = Product.query.get(id_product)

        product.id_company = request.json['id_company']
        product.product_type_id = request.json['product_type_id']  # Updated key
        product.product_subtype_id = request.json['product_subtype_id']  # Updated key
        product.description = request.json['description']
        product.unit_of_measure = request.json['unit_of_measure']
        product.price = request.json['price']
        product.status = request.json['status']
        product.user_register = request.json.get('user_register')
        product.user_process = request.json.get('user_process')
        product.process_date = request.json.get('process_date')
        product.registration_date = request.json.get('registration_date')
        product.negative_stock = request.json.get('negative_stock')
        product.drop_mark = request.json.get('drop_mark')

        db.session.commit()

        return product_schema.jsonify(product)
    except ValueError as e:
        db.session.rollback()
        logging.error(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"SQLAlchemyError: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

def delete_product(id_product):
    try:
        product = Product.query.get(id_product)
        if not product:
            return jsonify({"message": "Product not found"}), 404
        
        product.drop_mark = True
        db.session.commit()
        result = product_schema.dump(product),200
        return jsonify(result),200
    except ValueError as e:
        db.session.rollback()
        logging.error(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"SQLAlchemyError: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

def get_context_menu(company, storage, context):
    try:
        products = Product.query.filter(and_(Product.id_company == company.id, 
                                            Product.drop_mark == False, 
                                            Product.status == True, 
                                            Product.product_type_id.in_([1,2]))
                                        ).order_by(Product.product_type_id, Product.id_product
                                        ).all() #definir el tipo de producto 1:comida, 2:bebda
        
        stocks = Stock.query.filter(and_(Stock.id_storage == storage.id_storage, 
                                        Stock.drop_mark == False,
                                        Stock.stock > 0,
                                        Stock.id_product.in_([product.id_product for product in products]))
                                    ).all()
        # Crear un diccionario para mapear los productos con sus existencias
        stock_dict = {stock.id_product: stock for stock in stocks}

        menu_items = []
        drink_items = []

        context_menu = "Menu"
        context_drinks = "Bebidas"

        for product in products:
            stock = stock_dict.get(product.id_product, None) # Obtener el stock del producto o None si no existe
            if stock:
                if product.product_type_id == 1:  # Comida
                    menu_items.append(f"{product.description} - {product.price}")
                elif product.product_type_id == 2:  #Bebida
                    drink_items.append(f"{product.description} - {product.price}")
        
        context_menu = f"Menú: {os.linesep} {os.linesep.join(menu_items)}"
        context_drinks = f"Bebidas: {os.linesep} {os.linesep.join(drink_items)}"

        return f"""{context} {os.linesep} {os.linesep}
                {context_menu} {os.linesep} {os.linesep} 
                {context_drinks}"""
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_context_menu_route(company, storage, context):
    try:
        # Filtrar productos por compañía, estado y tipo de producto
        products = Product.query.filter(
            and_(
                Product.id_company == company.id, 
                Product.drop_mark == False, 
                Product.status == True
            )
        ).order_by(Product.product_type_id, Product.id_product).all()

        # Filtrar stocks por almacenamiento, estado y existencia
        stocks = Stock.query.filter(
            and_(
                Stock.id_storage == storage.id_storage, 
                Stock.drop_mark == False,
                Stock.stock > 0,
                Stock.id_product.in_([product.id_product for product in products])
            )
        ).all()

        # Crear un diccionario para mapear los productos con sus existencias
        stock_dict = {stock.id_product: stock for stock in stocks}

        # Obtener todos los subtipos de productos
        subtypes = ProductSubtype.query.all()
        subtype_dict = {subtype.id: subtype.name for subtype in subtypes}

        # Crear diccionarios para organizar los productos por subtipo
        subtype_items = {subtype.name: [] for subtype in subtypes}
        subtype_items_stock = {subtype.name: [] for subtype in subtypes}

        for product in products:
            stock = stock_dict.get(product.id_product, None)  # Obtener el stock del producto o None si no existe
            if stock:
                subtype_name = subtype_dict.get(product.product_subtype_id, "Otros")
                subtype_items[subtype_name].append(f"{product.id_product}, {product.description}, {product.price:.2f} Bs")
                subtype_items_stock[subtype_name].append(f"{product.id_product}, {product.description}, {stock.stock} disponibles")

        # Construir el contexto del menú
        context_menu_parts = []
        context_menu_parts_stock = []
        for subtype, items in subtype_items.items():
            if items:
                context_menu_parts.append(f"{subtype}: {os.linesep}  - {os.linesep.join(items)}")
        for subtype, items in subtype_items_stock.items():
            if items:
                context_menu_parts_stock.append(f"{subtype}: {os.linesep}  - {os.linesep.join(items)}")
        
        context_menu = f"Menú: {os.linesep}{os.linesep.join(context_menu_parts)}"
        context_stock = f"Stock disponible: {os.linesep}{os.linesep.join(context_menu_parts_stock)}"

        if "<MENU>" in context:
            context = context.replace("<MENU>", context_menu)
        else:
            context = f"""{context}{os.linesep}{os.linesep}{context_menu}"""

        if "<STOCK>" in context:
            context = context.replace("<STOCK>", context_stock)

        return context
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500