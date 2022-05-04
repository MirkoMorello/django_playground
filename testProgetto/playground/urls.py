from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('hello/', views.say_hello),
    path('hello2/', views.say_hello2),
    path('hello3/', views.say_hello3),
    path('hello4/', views.say_hello4),
    path('hello5/', views.say_hello5),
    path('hello6/', views.say_hello6),
    path('hello7/', views.say_hello7)
]