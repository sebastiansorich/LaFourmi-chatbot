# src/models/type_products.py

from .. import db

class ProductType(db.Model):
    __tablename__ = 'product_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    product_subtypes = db.relationship('ProductSubtype', back_populates='product_type')
    products = db.relationship('Product', back_populates='product_type')

class ProductSubtype(db.Model):
    __tablename__ = 'product_subtypes'  # Updated table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'), nullable=False)
    product_type = db.relationship('ProductType', back_populates='product_subtypes')
    products = db.relationship('Product', back_populates='product_subtype')
