from logging import raiseExceptions
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# Create your views here.
# queste permettono di effettuare endpoint RESTful API

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

@api_view(['GET', 'PUT'])
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

@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)