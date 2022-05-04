from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection

# in django-rest-framework.org/api-guide/fields/ trovo tutte le informazioni per costruire un serializer
# Serializer converte un modello in un dizionario, però non tutte i vari campi devono essere convertiti perchè alcuni sono privati, quindi li specifichiamo per ogni modello

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255) # specifichiamo la lunghezza perchè così quando accetteremo un oggetto tramite post possiamo filtrare
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price') # avendo cambiato nome da unit_price a price devo specificare la sorgente
    price_with_tax = serializers.SerializerMethodField(method_name = 'calculate_tax') # significa che è un metodo che da il valroe a questo campo
    # collection_id = serializers.PrimaryKeyRelatedField( # prendo l'id della collezione
    #    queryset = Collection.objects.all
    # )

    # collection_title = serializers.StringRelatedField()
    
    # collection = CollectionSerializer() # passo direttamente un dizionario serializzato di Collection

    collection = serializers.HyperlinkedRelatedField( # usato per generare hyperlink all'effettiva collezione
        queryset = Collection.objects.all(),
        view_name = 'collection-detail'
    )



    def calculate_tax (self, product: Product):
        return product.unit_price * Decimal(1.1)

