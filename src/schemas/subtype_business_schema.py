# src/schemas/subtype_business_schema.py

from .. import ma
from ..models.type_business import SubtypeBusiness

class SubtypeBusinessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubtypeBusiness
        load_instance = True

subtype_business_schema = SubtypeBusinessSchema()
subtypes_business_schema = SubtypeBusinessSchema(many=True)
