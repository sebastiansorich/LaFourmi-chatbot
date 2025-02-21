# src/models/client.py
from .. import db

class Client(db.Model):
    __tablename__ = 'clients'

    id_client = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cellphone = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    url_maps = db.Column(db.String(500))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.Integer)
    name_client = db.Column(db.String(100))
    user_register = db.Column(db.Integer)
    user_process = db.Column(db.Integer)
    process_date = db.Column(db.Date)
    registration_date = db.Column(db.Date)
    drop_mark = db.Column(db.Boolean)

    orders = db.relationship('Order', back_populates='client')

    def __init__(self, cellphone, address, url_maps, latitude, longitude, status, name_client, user_register=None, user_process=None, process_date=None, registration_date=None, drop_mark=False):
        self.cellphone = cellphone
        self.address = address
        self.url_maps = url_maps
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
        self.name_client = name_client
        self.user_register = user_register
        self.user_process = user_process
        self.process_date = process_date
        self.registration_date = registration_date
        self.drop_mark = drop_mark
