# src/models/order.py
from .. import db

class Order(db.Model):
    __tablename__ = 'orders'

    id_order = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_company = db.Column(db.Integer, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    id_client = db.Column(db.Integer, db.ForeignKey('clients.id_client'), nullable=True)
    status = db.Column(db.String(50))
    total = db.Column(db.Numeric(10, 2))
    order_date = db.Column(db.Date)
    user_register = db.Column(db.Integer)
    user_process = db.Column(db.Integer)
    process_date = db.Column(db.Date)
    registration_date = db.Column(db.Date)
    drop_mark = db.Column(db.Boolean)

    branch = db.relationship('Branch', back_populates='orders')
    client = db.relationship('Client', back_populates='orders')
    order_details = db.relationship('OrderDetail', backref='order', lazy=True)

    def __init__(self, id_company, branch_id, id_client=None, cellphone=None, status=None, total=0,
                 order_date=None, user_register=None, user_process=None, process_date=None,
                 registration_date=None, drop_mark=False):
        self.id_company = id_company
        self.branch_id = branch_id
        self.id_client = id_client
        self.cellphone = cellphone
        self.status = status
        self.total = total
        self.order_date = order_date
        self.user_register = user_register
        self.user_process = user_process
        self.process_date = process_date
        self.registration_date = registration_date
        self.drop_mark = drop_mark
