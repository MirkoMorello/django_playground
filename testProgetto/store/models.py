from dis import disco
from itertools import product
from unittest.util import _MAX_LENGTH
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from uuid import uuid4

# Create your models here.




class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete = models.CASCADE, related_name='+', null=True) # è una dipendenza circolare, ci serve per il prodotto de featurare, related_name + dice di non creare la relazione inversa nell'altro modello
    
    def __str__(self) -> str: #override del metodo tostring, così da poter visualizzarle nell'admin panel
        return self.title #super().__str__()
    
    class Meta:
        ordering = ['title']



class Product(models.Model):
    # sku = models.CharField(max_length=10, primary_key=True) In caso volessimo specificare una nostra PK, dato che django di default ne crea una per ogni modello
    title = models.CharField(max_length=255) #varchar 255
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True) # blank permette di non inserire niente nella creazione di un nuovo oggetto
    unit_price = models.DecimalField(max_digits=6,
                                     decimal_places=2,
                                     validators = [MinLengthValidator(1)]) # validatore da il numero minimo durante la creazione di un nuovo oggetto
    inventory = models.IntegerField()
    last_update = models.DateTimeField
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now = True)
    collection = models.ForeignKey(Collection, on_delete = models.PROTECT, related_name='products') # essendo ambivalente qui sto dicendo anche che il campo di collection non sarà product ma products
    promotions = models.ManyToManyField(Promotion, blank = True)

    def __str__(self) -> str: #override del metodo tostring, così da poter visualizzarle nell'admin panel
        return self.title #super().__str__()
    
    class Meta:
        ordering = ['title']



class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 255)
    birth_date = models.DateField(null = True)
    membership = models.CharField(max_length=1, choices = MEMBERSHP_CHOICES, default = MEMBERSHIP_BRONZE)

    def __str__(self) -> str: #override del metodo tostring, così da poter visualizzarle nell'admin panel
        return self.title #super().__str__()
    
    class Meta:
        ordering = ['first_name', 'last_name']
    
    def __str__(self) -> str: #override del metodo tostring, così da poter visualizzarle nell'admin panel
        return f'{self.first_name} {self.last_name}' #super().__str__()
    


class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'

    PAYMENT_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add = True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)



class Address(models.Model): #relazione uno a molti
    street = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    zip = models.PositiveSmallIntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems') # nome cambiato
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)



class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4) # permette di cambiare la pk da un numero integer sequenziale ad una stringa alfanumerica, questo perchè perlomeno un hacker non può accedere a random tramite api a carrelli di altre persone, non è una funzione perchè se no hardcodava un singolo uuid per ogni cart
    created_at = models.DateTimeField(auto_now_add = True)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(validators = [MinValueValidator(1)]) # valore minimo accettato = 1

    class Meta:
        unique_together = [['cart', 'product']] # così ho una singola istanza di un prodotto in un carrello



class Review (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description =  models.TextField(null=True)
    date = models.DateField(auto_now_add=True)