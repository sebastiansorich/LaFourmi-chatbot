# src/models/sale.py
from .. import db

class Sale(db.Model):
    __tablename__ = 'sales'

    id_sale = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id_order'), nullable=False)
    payment_type = db.Column(db.String(50))
    total = db.Column(db.Numeric(10, 2))
    sale_date = db.Column(db.Date)
    user_register = db.Column(db.Integer)
    user_process = db.Column(db.Integer)
    process_date = db.Column(db.Date)
    registration_date = db.Column(db.Date)
    drop_mark = db.Column(db.Boolean)

    order = db.relationship('Order', backref='sales')
    sale_details = db.relationship('SaleDetail', backref='sale', cascade='all, delete-orphan')

    def __init__(self, id_order, payment_type, total, sale_date, user_register=None, user_process=None,
                 process_date=None, registration_date=None, drop_mark=False):
        self.id_order = id_order
        self.payment_type = payment_type
        self.total = total
        self.sale_date = sale_date
        self.user_register = user_register
        self.user_process = user_process
        self.process_date = process_date
        self.registration_date = registration_date
        self.drop_mark = drop_mark
