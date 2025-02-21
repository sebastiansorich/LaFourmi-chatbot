# src/schemas/order_schema.py
from .. import ma
from ..models.order import Order
from ..models.order_detail import OrderDetail

class OrderDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderDetail
        include_fk = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    order_details = ma.Nested(OrderDetailSchema, many=True)

    class Meta:
        model = Order
        include_fk = True

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
