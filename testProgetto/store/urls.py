from cgitb import lookup
from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter # default router mette di default anche il supporto a http://127.0.0.1:8000/store/, inoltre, se uso http://127.0.0.1:8000/store/products.json ottengo il json
from rest_framework_nested import routers # libreria esterna, installata con drf nested routers, permette di fare rotte innestate
from . import views
from pprint import pprint # per printare carino

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename  = 'products') # stiamo dicendo che il nostro products endpoint dovrebbe essere gestito da productviewset. Ho specificato esplicitamente basename perchè ho modificato get_queryset e non capisce più nulla essendo che ha anche le review
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
# pprint(router.urls) se vuoi vedere le regexp e come sono gestiti i paths appena creati

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename ='product-reviews') # aggiungo child a products, che sarebbero le reviews, sto creando innestamento

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart') # carts è il parent, il lookup è il figlio ed è il parametro che estraiamo in get_queryset nella view di cartitem (cercherà cart_pk)
carts_router.register('items', views.CartItemViewSet, basename='cart-items')


# URLConf
urlpatterns = router.urls + products_router.urls + carts_router.urls

# urlpatterns = [
#     # path('products/', views.ProductList.as_view()), # asview permette di convertire la classe in una classica function-based view
#     # path('products/<int:pk>/', views.ProductDetail.as_view()), # tra le <> obbligo ad essere intero, l'oggetto sarà id
#     # path('collections/', views.collection_list),
#     # path('collections/<int:pk>', views.collection_detail, name ='collection-detail') # dandogli il nome posso poi referenziarlo in un altro campo api, come fatto in ProductSerializer
# ]