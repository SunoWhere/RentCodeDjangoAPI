from django.contrib import admin

from sales.models import Client

# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin): ...
