from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from ..models.branch import Branch

class BranchSchema(SQLAlchemyAutoSchema):
    qr_code_image = fields.Method("get_qr_code_image", dump_only=True)

    class Meta:
        model = Branch
        load_instance = True
        exclude = ("qr_code_image",)  # Excluir campo binario por defecto

    def get_qr_code_image(self, obj):
        # Método para manejar el campo binario
        if obj.qr_code_image:
            return "QR code image data"
        return None

branch_schema = BranchSchema()
branches_schema = BranchSchema(many=True)
