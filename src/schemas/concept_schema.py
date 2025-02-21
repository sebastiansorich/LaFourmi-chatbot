# src/schemas/concept_schema.py
from .. import ma
from ..models.concept import Concept

class ConceptSchema(ma.Schema):
    class Meta:
        model = Concept
        fields = ('id_concept', 'description', 'concepts_type', 'value')

concept_schema = ConceptSchema()
concepts_schema = ConceptSchema(many=True)
