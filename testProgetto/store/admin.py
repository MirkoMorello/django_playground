from django.db.models.aggregates import Count
from django.contrib import admin, messages
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode

#from testProgetto.tags.models import TaggedItem
from . import models

# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)



@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering = 'products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist') # è il link alla pagina changelist di prodotto, con ?collection__id=numero_collezione
        + '?'
        + urlencode({
            'collection__id': str(collection.id)
        })) 
        return format_html ('<a href = "{}">{}</a>', url, collection.products_count)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate( # override della classe oggetto originaria (ModelAdmin ha questo metodo) per poter aggiungere products_count a variabile dell'oggetto
            products_count = Count('products')
        )



@admin.register(models.Product) # modello admin per la classe prodotto
class ProductAdmin(admin.ModelAdmin):
    # fields = ['title', 'slug'] # campi che si possono visualizzare durante l'aggiunta di un nuovo prodotto, con exclude puoi escludere
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug' : ['title'] # viene usato il titolo per popolare automaticamente lo slug durante la creazione di un nuovo oggetto
    }
    actions = ['clear_inventory']
    search_fields = ['title']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = ['collection', 'last_update', InventoryFilter] # c'è il nostro filtro custom
    list_select_related = ['collection']


    def collection_title(self, product):
        return product.collection.title


    @admin.display(ordering = 'inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'


    @admin.action(description='Clear inventory') # azione custom
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were succesfully updated',
            messages.INFO
        )
 


@admin.register(models.Customer) # modello admin per la classe prodotto
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'ilast_name__starts_with'] # è per dire che vuoi che inizi con quello che stai cercando, non case sensitive

    def orders_count(self, customer):
        url = (reverse('admin:store_order_changelist') # è il link alla pagina changelist di prodotto, con ?collection__id=numero_collezione
        + '?'
        + urlencode({
            'customer__id': str(customer.id)
        })) 
        return format_html ('<a href = "{}">{}</a>', url, customer.orders_count)
    
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            orders_count = Count('order')
        )


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem


@admin.register(models.Order) # modello admin per la classe prodotto
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline] # permette di inserire un oggetto di tipo product, come specificato sopra
    autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', 'customer']

