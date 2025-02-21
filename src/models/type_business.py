# src/models/type_business.py

from .. import db

class TypeBusiness(db.Model):
    __tablename__ = 'type_business'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    subtypes = db.relationship('SubtypeBusiness', back_populates='type_business')

class SubtypeBusiness(db.Model):
    __tablename__ = 'subtype_business'
    id = db.Column(db.Integer, primary_key=True)
    type_business_id = db.Column(db.Integer, db.ForeignKey('type_business.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    type_business = db.relationship('TypeBusiness', back_populates='subtypes')
