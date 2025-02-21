from .. import ma
from ..models.company import Company
from ..schemas.branch_schema import BranchSchema

class CompanySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        include_fk = True

    branches = ma.Nested(BranchSchema, many=True)

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)
