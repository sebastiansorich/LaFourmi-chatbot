from .. import db
from .type_business import TypeBusiness, SubtypeBusiness

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type_business_id = db.Column(db.Integer, db.ForeignKey('type_business.id'), nullable=False)
    subtype_business_id = db.Column(db.Integer, db.ForeignKey('subtype_business.id'), nullable=False)
    cellphone_master = db.Column(db.String(20))
    nit = db.Column(db.String(50))
    name_receipt = db.Column(db.String(100))
    user_register = db.Column(db.Integer)
    user_process = db.Column(db.Integer)
    process_date = db.Column(db.Date)
    registration_date = db.Column(db.Date)
    drop_mark = db.Column(db.Boolean)
    context = db.Column(db.Text)
    close_message = db.Column(db.String(300), nullable=False)
    model = db.Column(db.Integer, nullable=False, default=50)  # Cambiado de String a Integer

    type_business = db.relationship('TypeBusiness')
    subtype_business = db.relationship('SubtypeBusiness')

    branches = db.relationship('Branch', back_populates='company')
    products = db.relationship('Product', back_populates='company')

    def __init__(self, name, type_business_id, subtype_business_id, cellphone_master=None, nit=None, name_receipt=None, user_register=None, user_process=None, process_date=None, registration_date=None, drop_mark=False, context=None, close_message=None, model=None):
        self.name = name
        self.type_business_id = type_business_id
        self.subtype_business_id = subtype_business_id
        self.cellphone_master = cellphone_master
        self.nit = nit
        self.name_receipt = name_receipt
        self.user_register = user_register
        self.user_process = user_process
        self.process_date = process_date
        self.registration_date = registration_date
        self.drop_mark = drop_mark
        self.context = context
        self.close_message = close_message
        self.model = model  # Inicialización de la nueva columna
