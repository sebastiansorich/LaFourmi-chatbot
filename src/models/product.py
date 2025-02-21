# src/models/product.py

from .. import db
from .product_type import ProductType, ProductSubtype  # Ensure correct imports

class Product(db.Model):
    __tablename__ = 'products'

    id_product = db.Column(db.Integer, primary_key=True)
    id_company = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'), nullable=False)
    product_subtype_id = db.Column(db.Integer, db.ForeignKey('product_subtypes.id'), nullable=False)  # Updated ForeignKey
    description = db.Column(db.String(255), nullable=False)
    unit_of_measure = db.Column(db.Integer, nullable=False)  # value concept
    price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    user_register = db.Column(db.Integer)
    user_process = db.Column(db.Integer)
    process_date = db.Column(db.Date)
    registration_date = db.Column(db.Date)
    negative_stock = db.Column(db.Boolean)
    drop_mark = db.Column(db.Boolean)

    company = db.relationship('Company', back_populates='products')
    stocks = db.relationship('Stock', back_populates='product')
    product_type = db.relationship('ProductType', back_populates='products')
    product_subtype = db.relationship('ProductSubtype', back_populates='products')

    def __init__(self, id_company, product_type_id, product_subtype_id, description, unit_of_measure, price, status, user_register, user_process, process_date, registration_date, negative_stock, drop_mark):
        self.id_company = id_company
        self.product_type_id = product_type_id
        self.product_subtype_id = product_subtype_id
        self.description = description
        self.unit_of_measure = unit_of_measure
        self.price = price
        self.status = status
        self.user_register = user_register
        self.user_process = user_process
        self.process_date = process_date
        self.registration_date = registration_date
        self.negative_stock = negative_stock
        self.drop_mark = drop_mark
