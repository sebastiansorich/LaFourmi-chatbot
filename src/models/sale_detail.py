# src/models/sale_detail.py
from .. import db

class SaleDetail(db.Model):
    __tablename__ = 'sale_details'

    id_detail = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_sale = db.Column(db.Integer, db.ForeignKey('sales.id_sale'), nullable=False)
    id_product = db.Column(db.Integer, db.ForeignKey('products.id_product'), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))
    drop_mark = db.Column(db.Boolean)

    product = db.relationship('Product', backref='sale_details')

    def __init__(self, id_sale, id_product, quantity, price, drop_mark=False):
        self.id_sale = id_sale
        self.id_product = id_product
        self.quantity = quantity
        self.price = price
        self.drop_mark = drop_mark
