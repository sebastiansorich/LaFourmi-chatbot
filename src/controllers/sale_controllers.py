# src/controllers/sale_controller.py
from flask import request, jsonify
from ..models.sale import Sale
from ..models.sale_detail import SaleDetail
from ..models.product import Product
from ..models.order_detail import OrderDetail
from ..models.stock import Stock
from .. import db
from ..schemas.sale_schema import sale_schema, sales_schema
import logging
from sqlalchemy.exc import SQLAlchemyError

def create_sale():
    try:
        data = request.get_json()

        id_order = data['id_order']
        payment_type = data.get('payment_type')
        sale_date = data['sale_date']
        user_register = data.get('user_register')
        user_process = data.get('user_process')
        process_date = data.get('process_date')
        registration_date = data.get('registration_date')
        drop_mark = data.get('drop_mark', False)
        sale_details = data.get('sale_details', [])

        total = 0
        
        new_sale = Sale(
            id_order=id_order,
            payment_type=payment_type,
            total=total,
            sale_date=sale_date,
            user_register=user_register,
            user_process=user_process,
            process_date=process_date,
            registration_date=registration_date,
            drop_mark=drop_mark
        )


        for detail in sale_details:
                id_product=detail['id_product'],
                drop_mark=detail.get('drop_mark', False)

                order_detail = OrderDetail.query.filter_by(id_order=id_order, id_product=id_product).first()
                if not order_detail:
                    return jsonify({"error":f"Order detail for product id {id_product} not found"}), 404

                quantity = order_detail.quantity

                product = Product.query.get(id_product)
                if not product:
                    return jsonify({"error": f"Not Product with id {id_product} not found"}), 404

                stock_record = Stock.query.filter_by(id_product=id_product).first()
                if not stock_record:
                    return jsonify({"error": f"Stock record for product id {id_product} not found"}), 404             
                
                if stock_record.reserved_stock < quantity:
                    return jsonify({"error": f"Not enough reserved stock for product id {id_product}"}), 400

                stock_record.reserved_stock -= quantity
                
                price = product.price
                
                subtotal = price * quantity
                total += subtotal

                new_sale_detail = SaleDetail(
                    id_sale= new_sale.id_sale,
                    id_product=id_product,
                    quantity=quantity,
                    price=price,
                )
        new_sale.sale_details.append(new_sale_detail)

        new_sale.total = total

        db.session.add(new_sale)
        db.session.commit()

        return sale_schema.jsonify(new_sale)
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

def get_sales():
    try:
        all_sales = Sale.query.all()
        result = sales_schema.dump(all_sales)
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_sale(id):
    try:
        sale = Sale.query.get(id)
        return sale_schema.jsonify(sale)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def update_sale(id):
    try:
        sale = Sale.query.get(id)

        data = request.get_json()
        sale.payment_type = data.get('payment_type', sale.payment_type)
        sale.total = data.get('total', sale.total)
        sale.sale_date = data.get('sale_date', sale.sale_date)
        sale.user_register = data.get('user_register', sale.user_register)
        sale.user_process = data.get('user_process', sale.user_process)
        sale.process_date = data.get('process_date', sale.process_date)
        sale.registration_date = data.get('registration_date', sale.registration_date)
        sale.drop_mark = data.get('drop_mark', sale.drop_mark)

        # Update sale details
        for detail_data in data.get('sale_details', []):
            detail = SaleDetail.query.get(detail_data['id_detail'])
            if detail:
                detail.id_product = detail_data.get('id_product', detail.id_product)
                detail.quantity = detail_data.get('quantity', detail.quantity)
                detail.price = detail_data.get('price', detail.price)
                detail.drop_mark = detail_data.get('drop_mark', detail.drop_mark)

        db.session.commit()

        return sale_schema.jsonify(sale)
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

def delete_sale(id):
    try:
        sale = Sale.query.get(id)
        if not sale:
            return jsonify({"error": "Sale not found"}), 404
    
        sale.drop_mark = True
        db.session.commit()
        return sale_schema.jsonfy(sale), 200
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
