# src/schemas/sale_schema.py
from .. import ma
from ..models.sale import Sale
from ..models.sale_detail import SaleDetail

class SaleDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SaleDetail
        include_fk = True

class SaleSchema(ma.SQLAlchemyAutoSchema):
    sale_details = ma.Nested(SaleDetailSchema, many=True)

    class Meta:
        model = Sale
        include_fk = True

sale_schema = SaleSchema()
sales_schema = SaleSchema(many=True)
