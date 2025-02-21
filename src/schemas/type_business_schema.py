# src/schemas/type_business_schema.py

from .. import ma
from ..models.type_business import TypeBusiness

class TypeBusinessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TypeBusiness
        load_instance = True

type_business_schema = TypeBusinessSchema()
types_business_schema = TypeBusinessSchema(many=True)
