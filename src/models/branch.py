from .. import db


class Branch(db.Model):
    __tablename__ = 'branches'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    manager = db.Column(db.String(100))
    status = db.Column(db.Boolean)
    operating_hours = db.Column(db.String(100))
    name_contact = db.Column(db.String(100))
    position_link = db.Column(db.String(255))
    user_register = db.Column(db.Integer)
    user_process = db.Column(db.Integer)
    process_date = db.Column(db.Date)
    registration_date = db.Column(db.Date)
    drop_mark = db.Column(db.Boolean)
    apikey = db.Column(db.String(255))
    whatsapp_token = db.Column(db.String(255))
    whatsapp_number_id = db.Column(db.String(255))
    assist_human_number = db.Column(db.String(20))
    qr_code_image = db.Column(db.LargeBinary)  # Nueva columna para la imagen del código QR

    company = db.relationship('Company', back_populates='branches')
    storages = db.relationship('Storage', back_populates='branch')
    orders = db.relationship('Order', back_populates='branch')

    def __init__(self, name, company_id, address=None, phone=None, manager=None,
                 status=None, operating_hours=None, name_contact=None, position_link=None,
                 user_register=None, user_process=None, process_date=None,
                 registration_date=None, drop_mark=False, apikey=None,
                 whatsapp_token=None, whatsapp_number_id=None, assist_human_number=None):
        self.name = name
        self.company_id = company_id
        self.address = address
        self.phone = phone
        self.manager = manager
        self.status = status
        self.operating_hours = operating_hours
        self.name_contact = name_contact
        self.position_link = position_link
        self.user_register = user_register
        self.user_process = user_process
        self.process_date = process_date
        self.registration_date = registration_date
        self.drop_mark = drop_mark
        self.apikey = apikey
        self.whatsapp_token = whatsapp_token
        self.whatsapp_number_id = whatsapp_number_id
        self.assist_human_number = assist_human_number