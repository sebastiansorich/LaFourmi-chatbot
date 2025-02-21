# src/models/concept.py
from .. import db

class Concept(db.Model):
    __tablename__ = 'concepts'

    id_concept = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)
    concepts_type = db.Column(db.Integer)  # Podría referirse a una tabla de tipos de conceptos
    value = db.Column(db.Integer)

    def __init__(self, description, concepts_type=None, value=None):
        self.description = description
        self.concepts_type = concepts_type
        self.value = value
