from django.db import models

# Create your models here.


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField()

    def __str__(self):
        return self.name


class Code(models.Model):
    name = models.CharField(max_length=255)
    code = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    execution_time = models.DurationField()

    language = models.ForeignKey(to=ProgrammingLanguage, on_delete=models.RESTRICT)
