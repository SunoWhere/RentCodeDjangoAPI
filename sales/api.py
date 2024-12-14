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
    
    @route.post("")
    def create_client(self, payload: ClientInSchema):
        client = Client.objects.create(**payload.dict())
        return {"id": client.id}

    @route.post("/login")
    def login(self, payload: ClientLoginSchema):
        client = Client.objects.create(**payload.dict())
        return {"id": client.id}
    
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
    
    @route.delete("/{client_id}/cart", response=list[CodeMinSchema])
    def remove_from_client_cart(self, payload: CodeToCartSchema, client_id: int):
        client = get_object_or_404(Client, id=client_id)
        code = get_object_or_404(Code, id=payload.id)
        client.codes.remove(code)
        return client.codes
    
    @route.get("/{client_id}/purchases", response=list[PurchaseSchema])
    def get_client_purchases(self, client_id: int):
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
    @route.post("")
    def create_purchase(self):
        pass