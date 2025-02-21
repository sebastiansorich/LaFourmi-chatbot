from .. import ma
from ..models.storage import Storage

class StorageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Storage
        fields = ('id_storage', 'id_branch', 'name', 'description', 
                  'user_register', 'user_process', 'process_date', 
                  'registration_date', 'drop_mark')

storage_schema = StorageSchema()
storages_schema = StorageSchema(many=True)
