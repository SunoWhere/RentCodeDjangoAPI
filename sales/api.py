from django.shortcuts import get_object_or_404
from django.db.models import Sum
from ninja_extra import ControllerBase, api_controller, route

from rentcode.models import Code
from rentcode.schemas import CodeToCartSchema, CodeMinSchema
from sales.models import Client, Purchase
from sales.schemas import ClientSchema, ClientInSchema, ClientLoginSchema, PurchaseSchema

@api_controller("/client")
class ClientController(ControllerBase):
    @route.get("", response=list[ClientSchema])
    def get_all_clients(self):
        return Client.objects.prefetch_related("codes", "codes__language")
    
    @route.get("/{client_id}", response=ClientSchema)
    def get_client(self, client_id: int):
        client = get_object_or_404(Client, id=client_id)
        return client
    
    @route.put("/{client_id}", response=ClientSchema)
    def update_client(self, client_id: int, payload: ClientInSchema):
        client = get_object_or_404(Client, id=client_id)
        client.email = payload.email
        client.firstname = payload.firstname
        client.lastname = payload.lastname
        client.birthday = payload.birthday
        client.save()
        return client
    
    @route.post("/login/", response=ClientSchema)
    def login(self, payload: ClientLoginSchema):
        client = get_object_or_404(Client, email=payload.email)
        return client

    @route.post("", response=ClientSchema)
    def create_client(self, payload: ClientInSchema):
        client = Client.objects.create(**payload.dict())
        return client
    
    @route.get("/{client_id}/cart", response=list[CodeMinSchema])
    def get_client_cart(self, client_id: int):
        client = get_object_or_404(Client, id=client_id)
        return client.codes
    
    @route.post("/{client_id}/cart", response=list[CodeMinSchema])
    def add_to_client_cart(self, payload: CodeToCartSchema, client_id: int):
        client = get_object_or_404(Client, id=client_id)
        code = get_object_or_404(Code, id=payload.id)
        client.codes.add(code)
        return client.codes
    
    @route.delete("/{client_id}/cart/{code_id}", response=list[CodeMinSchema])
    def remove_from_client_cart(self, client_id: int, code_id: int):
        client = get_object_or_404(Client, id=client_id)
        code = get_object_or_404(Code, id=code_id)
        client.codes.remove(code)
        return client.codes
    
    @route.get("/{client_id}/purchases", response=list[PurchaseSchema])
    def get_client_all_purchases(self, client_id: int):
        client = get_object_or_404(Client, id=client_id)
        return client.purchase_set.all()

    @route.post("/{client_id}/purchases", response=PurchaseSchema)
    def create_client_purchase(self, client_id: int):
        client = get_object_or_404(Client, id=client_id)
        total_price = client.codes.aggregate(Sum('price'))['price__sum']
        purchase = Purchase(client=client, total_price=total_price)
        purchase.save()
        for code in client.codes.all():
            purchase.codes.add(code)
        client.codes.clear()
        return purchase


@api_controller("/purchase")
class PurchaseController(ControllerBase):
    @route.get("/{purchase_id}", response=PurchaseSchema)
    def get_client_purchase(self, purchase_id: int):
        purchase = get_object_or_404(Purchase, id=purchase_id)
        return purchase