# src/controllers/stock_controllers.py
import os
from datetime import date
import pandas as pd
import requests
import requests
from werkzeug.utils import secure_filename
from flask import request, jsonify
from ..models.stock import Stock
from .. import db
from ..schemas.stock_schema import stock_schema, stocks_schema
import logging
from sqlalchemy.exc import SQLAlchemyError

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_stock():
    try:
        id_product = request.json['id_product']
        id_storage = request.json['id_storage']
        stock = request.json['stock']
        reserved_stock = request.json['reserved_stock']
        entry_date = request.json['entry_date']
        user_register = request.json.get('user_register', None)
        user_process = request.json.get('user_process', None)
        process_date = request.json.get('process_date', None)
        registration_date = request.json.get('registration_date', None)
        drop_mark = request.json.get('drop_mark', False)

        new_stock = Stock(
            id_product=id_product,
            id_storage=id_storage,
            stock=stock,
            reserved_stock=reserved_stock,
            entry_date = entry_date,
            user_register=user_register,
            user_process=user_process,
            process_date=process_date,
            registration_date=registration_date,
            drop_mark=drop_mark
        )

        db.session.add(new_stock)
        db.session.commit()

        return stock_schema.jsonify(new_stock)
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

def get_stocks():
    try:
        all_stocks = Stock.query.all()
        result = stocks_schema.dump(all_stocks)
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_stock(id):
    try:
        stock = Stock.query.get(id)
        return stock_schema.jsonify(stock)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def update_stock(id):
    try:
        stock = Stock.query.get(id)

        stock.id_product = request.json['id_product']
        stock.id_storage = request.json['id_storage']
        stock.stock = request.json['stock']
        stock.reserved_stock = request.json['reserved_stock']
        stock.entry_date = request.json['entry_date']
        stock.user_register = request.json.get('user_register', stock.user_register)
        stock.user_process = request.json.get('user_process', stock.user_process)
        stock.process_date = request.json.get('process_date', stock.process_date)
        stock.registration_date = request.json.get('registration_date', stock.registration_date)
        stock.drop_mark = request.json.get('drop_mark', stock.drop_mark)

        db.session.commit()

        return stock_schema.jsonify(stock)
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

def delete_stock(id):
    try:
        stock = Stock.query.get(id)
        if not stock:
            return jsonify({"error": "Stock not found"}), 404
        
        stock.drop_mark = True
        db.session.commit()
        return stock_schema.jsonify(stock), 200
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

def update_stock_from_excel(file_path):
    try:
        logging.info("INTENTANDO LEER FILE_PATH")
        df = pd.read_excel(file_path, engine='openpyxl')
        update_database(df)
        logging.info("STOCK UPDATED")
        return jsonify({"message": "Stock updated successfully"}), 200
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500

def update_database(df):
    try:
        for index, row in df.iterrows():
            today = date.today()
            stock = Stock.query.filter_by(id_product=row['id_product']).first()
            if stock:
                stock.stock = row['stock']
                stock.reserved_stock = row['reserved_stock']
                stock.entry_date = today
                db.session.commit()
            else:
                new_stock = Stock(
                    id_product = row['id_product'],
                    id_storage = row.get('id_storage', 1),  # Assuming id_storage is provided or default to 1
                    stock = row['stock'],
                    reserved_stock = row.get('reserved_stock', 0),
                    entry_date = today,
                    user_register = row.get('user_register', None),
                    user_process = row.get('user_process', None),
                    process_date = row.get('process_date', None),
                    registration_date = row.get('registration_date', None),
                    drop_mark = row.get('drop_mark', False)
                )
                db.session.add(new_stock)
                db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def download_file(access_token, media_id, file_path):
    url = f'https://graph.facebook.com/v13.0/{media_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_info = response.json()
        download_url = file_info.get('url')

        if download_url:
            file_response = requests.get(download_url, headers=headers)
            if file_response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(file_response.content)
                logging.info("El archivo se ha descargado exitosamente.")
                return True
            else:
                logging.error(f"No se pudo descargar el archivo. Código de estado: {file_response.status_code}")
                logging.error(f"Detalles del error: {file_response.text}")
                return False
        else:
            logging.error("No se pudo obtener la URL de descarga del archivo.")
            return False
    else:
        logging.error(f"No se pudo obtener la información del archivo. Código de estado: {response.status_code}")
        logging.error(f"Detalles del error: {response.text}")
        return False

def get_daily_stock(storages):
    storage_ids = [storage.id_storage for storage in storages]
    stocks = (
        db.session.query(Stock)
        .filter(Stock.stock > 0)
        .filter(Stock.id_storage.in_(storage_ids))
        .all()
    )
    return stocks