from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail), # tra le <> obbligo ad essere intero, l'oggetto sarà id
    path('collections/', views.collection_list),
    path('collections/<int:pk>', views.collection_detail, name ='collection-detail') # dandogli il nome posso poi referenziarlo in un altro campo api, come fatto in ProductSerializer
]