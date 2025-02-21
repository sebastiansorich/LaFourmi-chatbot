# src/models/stock.py
from .. import db

class Stock(db.Model):
    __tablename__ = 'stock'

    id_stock = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_product = db.Column(db.Integer, db.ForeignKey('products.id_product'), nullable=False)
    id_storage = db.Column(db.Integer, db.ForeignKey('storages.id_storage'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    reserved_stock = db.Column(db.Integer, nullable=False)
    entry_date = db.Column(db.Date)  
    user_register = db.Column(db.Integer)
    user_process = db.Column(db.Integer)
    process_date = db.Column(db.Date)
    registration_date = db.Column(db.Date)
    drop_mark = db.Column(db.Boolean)

    product = db.relationship('Product', back_populates='stocks')
    storage = db.relationship('Storage', back_populates='stocks')

    def __init__(self, id_product, id_storage, stock, reserved_stock,entry_date, user_register=None,
                 user_process=None, process_date=None, registration_date=None, drop_mark=False):
        self.id_product = id_product
        self.id_storage = id_storage
        self.stock = stock
        self.reserved_stock = reserved_stock
        self.entry_date = entry_date
        self.user_register = user_register
        self.user_process = user_process
        self.process_date = process_date
        self.registration_date = registration_date
        self.drop_mark = drop_mark
