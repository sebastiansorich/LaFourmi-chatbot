# src/schemas/product_schema.py

from .. import ma
from ..models.product import Product

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        fields = ('id_product', 'id_company', 'product_type_id', 'producto_subtype_id', 'description', 
                  'unit_of_measure', 'price', 'status', 'user_register', 
                  'user_process', 'process_date', 'registration_date', 
                  'negative_stock', 'drop_mark')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
