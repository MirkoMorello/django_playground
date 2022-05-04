from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
# queste permettono di effettuare endpoint RESTful API

@api_view() # di rest_frameork, più performante, installato tramite pipenv e abbiamo aggiunto alle installed apps
def product_list(request):
    return Response('ok') # anche questo è di rest_framework


@api_view()
def product_detail(request, id):
    return Response(id)