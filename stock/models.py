from datetime import date

from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    sku = models.CharField(max_length=15, unique=True, help_text='Stock Keeping Unit')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # TODO add Category for product

    def __str__(self):
        return self.name

    @property
    def quantity(self):
        qty_in = Movement.objects.filter(product=self, kind=Movement.IN).aggregate(models.Sum('quantity'))
        qty_out = Movement.objects.filter(product=self, kind=Movement.OUT).aggregate(models.Sum('quantity'))
        return (qty_in['quantity__sum'] or 0) - (qty_out['quantity__sum'] or 0)


class Movement(models.Model):
    IN, OUT = 'IN', 'OUT'
    KIND = [(IN, 'Inlet'), (OUT, 'Outlet')]

    kind = models.CharField(max_length=5, choices=KIND, default=OUT)
    data = models.DateField(default=date.today)
    quantity = models.PositiveIntegerField()  # TODO dynamic accordingly with a unit measurement (Integer ou Decimal)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    partner = models.ForeignKey('Partner', null=True,  on_delete=models.SET_NULL)
    location = models.ForeignKey('Location', null=True, on_delete=models.SET_NULL)
    # TODO add control product for Lot
    # TODO add logistic LIFO e FIFO for product

    def __str__(self):
        return f'{self.product} - {self.data}'
    
    def save(self, *args, **kwargs):
        if self.kind == Movement.OUT and self.quantity > self.product.quantity:
            raise ValidationError('Stock out')
        super().save(*args, **kwargs)
    

class Partner(models.Model):
    name = models.CharField(max_length=50)
    cp = models.CharField(max_length=14, unique=True, help_text='CNPJ or CPF')
    client = models.BooleanField(help_text='Is a Client')
    supplier = models.BooleanField(help_text='Is a Supplier')
    # TODO add Partner default location
    # TODO add address


class Location(models.Model):
    CLIENT, INTERNAL = 'CLIENT', 'INTERNAL'
    KIND = [(CLIENT, 'Client'), (INTERNAL, 'Internal')]

    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=10, choices=KIND)
