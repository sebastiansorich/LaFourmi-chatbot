from .. import db

class Storage(db.Model):
    __tablename__ = 'storages'

    id_storage = db.Column(db.Integer, primary_key=True)
    id_branch = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    user_register = db.Column(db.Integer)
    user_process = db.Column(db.Integer)
    process_date = db.Column(db.Date)
    registration_date = db.Column(db.Date)
    drop_mark = db.Column(db.Boolean)

    branch = db.relationship('Branch', back_populates='storages')
    stocks = db.relationship('Stock', back_populates='storage')

    def __init__(self, id_branch, name, description, user_register, user_process, process_date, registration_date, drop_mark):
        self.id_branch = id_branch
        self.name = name
        self.description = description
        self.user_register = user_register
        self.user_process = user_process
        self.process_date = process_date
        self.registration_date = registration_date
        self.drop_mark = drop_mark
