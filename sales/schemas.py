from ninja import ModelSchema

from rentcode.schemas import CodeSchema
from sales.models import Client, Purchase


class ClientSchema(ModelSchema):
    class Meta:
        model = Client
        fields = ["id", "firstname", "lastname", "email", "birthday"]
    
    codes: list[CodeSchema]


class ClientPurchaseSchema(ModelSchema):
    class Meta:
        model = Client
        fields = ["id", "firstname", "lastname", "email", "birthday"]
    

class ClientInSchema(ModelSchema):
    class Meta:
        model = Client
        fields = ["firstname", "lastname", "email", "birthday"]
    

class ClientLoginSchema(ModelSchema):
    class Meta:
        model = Client
        fields = ["email"]


class PurchaseSchema(ModelSchema):
    class Meta:
        model = Purchase
        fields = ["id", "total_price", "created_at"]

    client: ClientPurchaseSchema
    codes: list[CodeSchema]