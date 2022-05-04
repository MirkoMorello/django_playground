from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail) # tra le <> obbligo ad essere intero, l'oggetto sarà id
]