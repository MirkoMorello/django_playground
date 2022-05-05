from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection

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