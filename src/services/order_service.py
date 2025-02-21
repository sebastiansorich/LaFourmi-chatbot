import os
from flask import request, jsonify
from src.controllers.order_controllers import create_order_by_controller, get_order
from src.controllers.client_controller import get_client
from src.controllers.product_controllers import get_product
from src.models.order import Order
from src.models.order_detail import OrderDetail
from datetime import datetime

def create_order(company, branch, client, data):
        now = datetime.now()
        order = Order(
            id_company=company.id,
            branch_id=branch.id,
            id_client=client.id_client,
            status=1,
            total=0,
            order_date=now,
            user_register=1,
            user_process=1,
            process_date=now,
            registration_date=now,
            drop_mark=False
        )
        order_detail = [OrderDetail(order.id_order,p['id_product'],p['quantity'],p['price']) for p in data['productos']]
        order.order_details = order_detail

        #order_json = json.dumps(order.to_dic(), indent=4) #esto cuando funcione las rutas y se consuma los metodos del controlador.
        return create_order_by_controller(order)

def get_order_summary(id_order, client):
        message = ""
        order_response = get_order(id_order)

        if order_response.status_code == 200:
            order_data = order_response.get_json()
            message = (
            f"**Pedido: {order_data['id_order']}**{os.linesep}"
            f"**Cliente: {client.cellphone}**{os.linesep}"
            f"Pedido:{os.linesep}código  |   producto   | cantidad{os.linesep}"
            )

            for detail in order_data['order_details']:
                # Intentar obtener el producto de una caché local o similar para evitar múltiples solicitudes
                product_response = get_product(detail['id_product'])
                if product_response.status_code == 200:
                    product_data = product_response.get_json()
                    message += f"{detail['id_product']} {product_data['description']} {detail['quantity']}{os.linesep}"
                else:
                    message += f"{detail['id_product']} Producto no encontrado {detail['quantity']}{os.linesep}"

        return message