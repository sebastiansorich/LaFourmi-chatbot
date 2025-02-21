# src/controllers/order_controller.py
from flask import request, jsonify
from src.helper.exceptions import InsufficientStockError, UnauthorizedError, DataProcessedError
from src.models.product import Product
from ..models.order import Order
from ..models.order_detail import OrderDetail
from .. import db
from ..schemas.order_schema import order_schema, orders_schema
from ..models.stock import Stock
from ..models.client import Client
from ..models.branch import Branch  # Importar el modelo Branch
import logging
from sqlalchemy.exc import SQLAlchemyError

def create_order():
    try:
        data = request.get_json()

        id_company = data['id_company']
        branch_id = data['branch_id']
        id_client = data['id_client']
        status = data.get('status')
        order_date = data['order_date']
        user_register = data.get('user_register')
        user_process = data.get('user_process')
        process_date = data.get('process_date')
        registration_date = data.get('registration_date')
        drop_mark = data.get('drop_mark', False)
        order_details = data.get('order_details', [])

        # Obtener los datos del cliente
        client = Client.query.get(id_client)
        if not client:
            return jsonify({"error": f"Client with id {id_client} not found"}), 404

        # Inicializar el total
        total = 0

        # Verificar si el branch existe
        branch = Branch.query.get(branch_id)
        if not branch:
            return jsonify({"error": f"Branch with id {branch_id} not found"}), 404

        # Iniciar la transacción
        new_order = Order(
            id_company=id_company,
            branch_id=branch_id,
            id_client=id_client,
            status=status,
            total=total,
            order_date=order_date,
            user_register=user_register,
            user_process=user_process,
            process_date=process_date,
            registration_date=registration_date,
            drop_mark=drop_mark
        )

        for detail in order_details:
            id_product = detail['id_product']
            quantity = detail['quantity']
            drop_mark_detail = detail.get('drop_mark', False)

            # Obtener el precio del producto
            product = Product.query.get(id_product)
            if not product:
                return jsonify({"error": f"Product with id {id_product} not found"}), 404

            price = product.price

            # Validar stock disponible
            stock_record = Stock.query.filter_by(id_product=id_product).first()
            if not stock_record or stock_record.stock < quantity:
                return jsonify({"error": f"Insufficient stock for product id {id_product}"}), 400

            # Descontar stock
            stock_record.stock -= quantity
            stock_record.reserved_stock += quantity

            # Calcular el total acumulado
            total += price * quantity

            new_order_detail = OrderDetail(
                id_order=new_order.id_order,
                id_product=id_product,
                quantity=quantity,
                price=price,
                drop_mark=drop_mark_detail
            )
            new_order.order_details.append(new_order_detail)

        # Actualizar el total del pedido
        new_order.total = total

        db.session.add(new_order)
        db.session.commit()

        # Aquí es donde podrías devolver la información del cliente si es necesario
        return jsonify({
            "order": order_schema.dump(new_order),
            "client": {
                "name": client.name_client,
                "cellphone": client.cellphone
            }
        })

    except Exception as e:
        db.session.rollback()
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500

def create_order_by_controller(order):
    try:
        # Inicializar el total
        total = 0

        # Verificar si el branch existe
        branch = Branch.query.get(order.branch_id)  # Se agregó para verificar la existencia del branch
        if not branch:
            raise Exception(f"error: Branch with id {order.branch_id} not found")

        if not order.order_details or len(order.order_details) == 0:
            raise Exception(f"error: Details is empty, order: {order.branch_id}")

        new_order = Order(
            id_company=order.id_company,
            branch_id=order.branch_id,  # Se agregó para asignar el branch_id
            id_client=order.id_client,
            status=order.status,
            total=order.total,
            order_date=order.order_date,
            user_register=order.user_register,
            user_process=order.user_process,
            process_date=order.process_date,
            registration_date=order.registration_date,
            drop_mark=order.drop_mark
        )

        for detail in order.order_details:
            id_product = detail.id_product
            quantity = detail.quantity
            drop_mark_detail = detail.drop_mark

            # Obtener el precio del producto si no se proporciona
            product = Product.query.get(id_product)
            if not product:
                raise Exception(f"error: Product with id {id_product} not found")

            # Utilizar el precio del producto si no se proporciona
            price = product.price

            # Validar stock disponible
            stock_record = Stock.query.filter_by(id_product=id_product).first()
            if not stock_record or stock_record.stock < quantity:
                raise InsufficientStockError(id_product, product.description)

            # Descontar stock y actualizar stock reservado
            stock_record.stock -= quantity
            stock_record.reserved_stock += quantity

            # Calcular el total acumulado
            total += price * quantity

            new_order_detail = OrderDetail(
                id_order=new_order.id_order,
                id_product=id_product,
                quantity=quantity,
                price=price,
                drop_mark=drop_mark_detail
            )
            new_order.order_details.append(new_order_detail)

        # Actualizar el total del pedido
        new_order.total = total

        db.session.add(new_order)
        db.session.commit()

        return order_schema.jsonify(new_order)

    except ValueError as e:
        db.session.rollback()
        logging.error(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 404
    except InsufficientStockError as e:
        db.session.rollback()
        logging.error(f"InsufficientStockError: {e}")
        return jsonify({"error": str(e)}), 409  # 409 Conflict, ya que es un problema de estado de recursos
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"SQLAlchemyError: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500

def get_orders():
    try:
        all_orders = Order.query.all()
        result = orders_schema.dump(all_orders)
        return jsonify(result)
    except Exception as e:
        logging.error(f"An unexpected error occurred:: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def get_order(id):
    try:
        order = Order.query.get(id)
        if order is None:
            return jsonify({"error": "Order not found"}), 404
        return order_schema.jsonify(order)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error" : f"An unexpected error occurred:, {str(e)}"}), 500

def update_order(id):
    try:
        order = Order.query.get(id)

        data = request.get_json()
        order.branch_id = data.get('branch_id', order.branch_id)
        order.id_client = data.get('id_client', order.id_client)
        order.cellphone = data.get('cellphone', order.cellphone)
        order.status = data.get('status', order.status)
        order.total = data.get('total', order.total)
        order.order_date = data.get('order_date', order.order_date)
        order.user_register = data.get('user_register', order.user_register)
        order.user_process = data.get('user_process', order.user_process)
        order.process_date = data.get('process_date', order.process_date)
        order.registration_date = data.get('registration_date', order.registration_date)
        order.drop_mark = data.get('drop_mark', order.drop_mark)

        # Update order details
        for detail_data in data.get('order_details', []):
            detail = OrderDetail.query.get(detail_data['id_detail'])
            if detail:
                detail.id_product = detail_data.get('id_product', detail.id_product)
                detail.quantity = detail_data.get('quantity', detail.quantity)
                detail.price = detail_data.get('price', detail.price)
                detail.drop_mark = detail_data.get('drop_mark', detail.drop_mark)

        db.session.commit()

        return order_schema.jsonify(order)
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
    #finally:
    #    db.session.close()

def delete_order(id):
    try:
        order = Order.query.get(id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
    
        order.drop_mark = True
        db.session.commit()
        return order_schema.jsonify(order), 200
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
    #finally:
    #    db.session.close()
def delete_order_by_controller(client, id):
    try:
        order = Order.query.get(id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        
        if client.id_client != order.id_client:
            raise UnauthorizedError(order.id_client, client.cellphone, "")
        
        if order.status > 1:
            raise DataProcessedError(id, order.status)

        order.status = 3
        db.session.commit()
        return order_schema.jsonify(order)
    
    except ValueError as e:
        db.session.rollback()
        logging.error(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 404
    except UnauthorizedError as e:
        db.session.rollback()
        logging.error(f"UnauthorizedError: {e}")
        return jsonify({"error": str(e)}), 432  # Custom error unnasigned
    except DataProcessedError as e:
        db.session.rollback()
        logging.error(f"DataProccesedError: {e}")
        return jsonify({"error": str(e)}), 433  # Custom error unnasigned
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"SQLAlchemyError: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500
    #finally:
        #db.session.close()
