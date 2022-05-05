from ast import Delete
from logging import raiseExceptions
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import OrderItem, Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# Create your views here.
# queste permettono di effettuare endpoint RESTful API

# quelle fatte fino ad ora sono function-based views, esistono anche class-based views, rendono il codice più pulito


class ProductViewSet(ModelViewSet): # abbiamo una singola classe che implementa tutte le views per il prodotto, grazie a ModelViewSet
    queryset = Product.objects.all() # mi permette anche di prendere le relative collezioni
    serializer_class = ProductSerializer
    
    def get_serializer_context(self): #override
            return {'request' : self.request} # essendo una queryset, avverto che deve iterare su più oggetti per castarli a dizionario

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0: # abbiamo cambiato la logica di distruzione per non pingare ancora il db, lezione 2_26, ricontrolla
            return Response({'error': "product can't be deleted because there is an associated order item"}, status = status.HTTP_405_METHOD_NOT_ALLOWED) # in caso l'oggetto sia referenziato in un order, non lo elimino e ritorno 405
        return super().destroy(request, *args, **kwargs)
        
class CollectionViewSet(ModelViewSet): # volendo esiste anche ReadOnlyModelViewSet che permette di non avere put/delete/patch
    queryset = Collection.objects.annotate(products_count = Count('products')).all() # conto i prodotti che lo hanno referenziato
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id = kwargs['pk']).count() > 0: # abbiamo cambiato la logica di distruzione per non pingare ancora il db, lezione 2_26, ricontrolla
            return Response({'error': "collection can't be deleted because there are products referencing it"}, status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    









############## NOT USED ANYMORE



@api_view(['GET', 'POST']) # di rest_frameork, più performante, installato tramite pipenv e abbiamo aggiunto alle installed apps
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all() # mi permette anche di prendere le relative collezioni
        serializer = ProductSerializer(queryset, many = True, context = {'request' : request}) # essendo una queryset, avverto che deve iterare su più oggetti per castarli a dizionario
        return Response(serializer.data) # anche questo è di rest_framework
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data) # se data è specificato, il serializer effettuerà deserealizzazione in modo tale che da un dizionario ottengo un oggetto
        serializer.is_valid(raise_exception = True) # con raise exception = True non c'è bisogno di fare un if else in cui restituire status 400
        serializer.save() # viene salvato in DB
        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""
@api_view()
def product_detail(request, id):
    try:
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data) # serializer.data l'effettivo dizionario, successivamente django creerà un oggetto json da questo dizionario
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
"""

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id) # ottengo l'oggetto se c'è, se non c'è ottengo risposta 404 da passare
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data) # serializer.data l'effettivo dizionario, successivamente django creerà un oggetto json da questo dizionario
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({'error': "product can't be deleted because there is an associated order item"}, status = status.HTTP_405_METHOD_NOT_ALLOWED) # in caso l'oggetto sia referenziato in un order, non lo elimino e ritorno 405
        product.delete()
        return Response(status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.annotate(products_count = Count('products')).all() # conto i prodotti che lo hanno referenziato
        serializer = CollectionSerializer(queryset, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET', 'DELETE', 'PUT'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')), pk=pk)
    if request.method == 'GET':
        serilizer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    elif request.method == 'DELETE':
        if collection.product.count()>0:
            return Response({'error': "collection can't be deleted because there are products referencing it"}, status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    
