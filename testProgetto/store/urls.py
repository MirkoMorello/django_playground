from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.ProductList.as_view()), # asview permette di convertire la classe in una classica function-based view
    path('products/<int:id>/', views.ProductDetail.as_view()), # tra le <> obbligo ad essere intero, l'oggetto sarà id
    path('collections/', views.collection_list),
    path('collections/<int:pk>', views.collection_detail, name ='collection-detail') # dandogli il nome posso poi referenziarlo in un altro campo api, come fatto in ProductSerializer
]