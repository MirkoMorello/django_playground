from decimal import Decimal
from itertools import product
from venv import create
from rest_framework import serializers
from .models import Cart, Product, Collection, Review, CartItem


# in django-rest-framework.org/api-guide/fields/ trovo tutte le informazioni per costruire un serializer
# Serializer converte un modello in un dizionario, però non tutte i vari campi devono essere convertiti perchè alcuni sono privati, quindi li specifichiamo per ogni modello

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    
    products_count = serializers.IntegerField(read_only = True) # non devo metterlo in post e non voglio che dia errore se non lo metto, quindi metto read_only

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'price', 'price_with_tax', 'collection'] # per default, questo creatore di serializer mette la pk, se non la voglio basta scommentare una collection sotto che andrà a sovrascrivere

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255) # specifichiamo la lunghezza perchè così quando accetteremo un oggetto tramite post possiamo filtrare
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price') # avendo cambiato nome da unit_price a price devo specificare la sorgente, se voglio averlo anche con Meta va scommentato perchè Product non ha price ma unit_price, quindi la classe meta se non trova cerca qui
    price_with_tax = serializers.SerializerMethodField(method_name = 'calculate_tax') # significa che è un metodo che da il valroe a questo campo, va inserito perchè non ce l'ho nell'oggetto Product
    ##### Modi differenti per ottenere la collezione del prodotto:
    # collection_id = serializers.PrimaryKeyRelatedField( # prendo l'id della collezione
    #    queryset = Collection.objects.all
    # )
    # collection_title = serializers.StringRelatedField()
    # collection = CollectionSerializer() # passo direttamente un dizionario serializzato di Collection
    # collection = serializers.HyperlinkedRelatedField( # usato per generare hyperlink all'effettiva collezione
    #     queryset = Collection.objects.all(),
    #     view_name = 'collection-detail'
    # )
    def calculate_tax (self, product: Product):
        return product.unit_price * Decimal(1.1)



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description'] # abbiamo rimosso product perchè viene preso dall'url, sovrascrivendo context in views viene passato forzatamente product_id
    
    def create(self, validated_data): # override della creazione del dizionario, così posso andare a pescare product_id che ho passato forzatamente dall'url nella view
        product_id = self.context['product_id'] # prendo dal context overridato in views
        return Review.objects.create(product_id = product_id, **validated_data) # creo l'oggetto con i validated_data che sono quelli dentro fields, e aggiungo product_id preso dal context che in views.py ho preso dall'url


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']



class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField() # significa che deve andare a cercarsi la funzione con questo nome

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True) # readonly fa si che non compaia nel form della post
    items = CartItemSerializer(many=True, read_only=True) # uso l'id per prendermi il serializer di cartitem
    total_price = serializers.SerializerMethodField()
    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value): # se passo in post un product id che non esiste
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('No product with the given ID was found.')
        return value

    def save(self, **kwargs):  # override per poter aggiornare la quantità di un elemento che è già presente in carrello
        cart_id = self.context['cart_id'] # persa dal context di view
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id = cart_id, product_id = product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id = cart_id, **self.validated_data)
        
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
    





    # def create(self, validated_data): # override, in caso io voglia customizzazioni nella creazione di un oggetto dopo POST, non è necessario
    #     product = Product(**validated_data)
    #     product.other = 1 # field speciale che volevo settare
    #     product.save()
    #     return product
    

    # def update(self, instance, validated_data): # override, in caso io voglia customizzazioni nella modifica di un oggetto dopo PUT, non è necessario
    #     instance.unit_price = validated_data.get('unit_price') # field da modificare
    #     instance.save()
    #     return instance



    # def validate(self, data) # normalmente non mi serve fare un override, ma se devo fare delle validazioni particolari, come i due campi della password medesime, allora devo farlo qui
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Password do not match')
    #     return data
