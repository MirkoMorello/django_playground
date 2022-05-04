from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# Create your views here.
# queste permettono di effettuare endpoint RESTful API

@api_view() # di rest_frameork, più performante, installato tramite pipenv e abbiamo aggiunto alle installed apps
def product_list(request):
    queryset = Product.objects.select_related('collection').all() # mi permette anche di prendere le relative collezioni
    serializer = ProductSerializer(queryset, many = True, context = {'request' : request}) # essendo una queryset, avverto che deve iterare su più oggetti per castarli a dizionario
    return Response(serializer.data) # anche questo è di rest_framework

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

@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id) # ottengo l'oggetto se c'è, se non c'è ottengo risposta 404 da passare
    serializer = ProductSerializer(product)
    return Response(serializer.data) # serializer.data l'effettivo dizionario, successivamente django creerà un oggetto json da questo dizionario

@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)