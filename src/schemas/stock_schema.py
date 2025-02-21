from .. import ma
from ..models.stock import Stock
from .product_schema import ProductSchema
from .storage_schema import StorageSchema

class StockSchema(ma.SQLAlchemyAutoSchema):
    product = ma.Nested(ProductSchema)
    storage = ma.Nested(StorageSchema)

    class Meta:
        model = Stock
        fields = ('id_stock', 'id_product', 'id_storage', 'stock', 'reserved_stock','entry_date', 
                  'user_register', 'user_process', 'process_date', 'registration_date', 
                  'drop_mark', 'product', 'storage')

stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)
