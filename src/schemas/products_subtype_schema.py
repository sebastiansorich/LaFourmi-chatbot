# src/schemas/product_subtype_schema.py

from .. import ma
from ..models.product_type import ProductSubtype  # Ensure correct import

class ProductSubtypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductSubtype  # Updated model reference
        load_instance = True

product_subtype_schema = ProductSubtypeSchema()
product_subtypes_schema = ProductSubtypeSchema(many=True)
