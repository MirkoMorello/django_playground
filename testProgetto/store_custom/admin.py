from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models import Product

# Register your models here.

#questa app è letteralmente l'app per il mio store, che è custom e mette in comunione le altre applicazioni che ho, quella store e quella tag, permettendo di mantenerle stagne

class TagInline(GenericTabularInline): # ho aggiunto un modello di un altra app che implementa relazioni generiche ed agnostiche
    autocomplete_fields = ['tag']
    model = TaggedItem

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)