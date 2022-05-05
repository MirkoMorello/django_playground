from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter # default router mette di default anche il supporto a http://127.0.0.1:8000/store/, inoltre, se uso http://127.0.0.1:8000/store/products.json ottengo il json
from . import views
from pprint import pprint # per printare carino

router = DefaultRouter()
router.register('products', views.ProductViewSet) # stiamo dicendo che il nostro products endpoint dovrebbe essere gestito da productviewset
router.register('collections', views.CollectionViewSet)
# pprint(router.urls) se vuoi vedere le regexp e come sono gestiti i paths appena creati


# URLConf

urlpatterns = router.urls

# urlpatterns = [
#     # path('products/', views.ProductList.as_view()), # asview permette di convertire la classe in una classica function-based view
#     # path('products/<int:pk>/', views.ProductDetail.as_view()), # tra le <> obbligo ad essere intero, l'oggetto sarà id
#     # path('collections/', views.collection_list),
#     # path('collections/<int:pk>', views.collection_detail, name ='collection-detail') # dandogli il nome posso poi referenziarlo in un altro campo api, come fatto in ProductSerializer
# ]