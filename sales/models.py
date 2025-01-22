from django.db import models

from rentcode.models import Code

# Create your models here.
class Client(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    birthday = models.DateField()

    codes = models.ManyToManyField(to=Code, related_name="clients")

class Purchase(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.RESTRICT)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    codes = models.ManyToManyField(to=Code)