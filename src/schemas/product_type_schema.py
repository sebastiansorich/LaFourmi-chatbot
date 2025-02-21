# src/schemas/product_type_schema.py

from .. import ma
from ..models.product_type import ProductType

class ProductTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductType
        load_instance = True

product_type_schema = ProductTypeSchema()
product_types_schema = ProductTypeSchema(many=True)
