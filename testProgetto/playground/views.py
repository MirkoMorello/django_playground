from itertools import product
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, connection
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.contrib.contenttypes.models import ContentType
from store.models import Product, OrderItem, Customer, Order, Collection
from tags.models import TaggedItem


def say_hello(request):
    query_set = Product.objects.all() # ci da tutti gli oggetti
    try:
        product = Product.objects.get(pk=1) # è una where
    except ObjectDoesNotExist:
        pass

    # alternativamente, si usa filter e si prende il primo elemento ritornato, che se non esiste è None, invece di generare una eccezione come sopra
    product = Product.objects.filter(pk=1).first()
    # questo invece ci dice se esiste
    product = Product.objects.filter(pk=1).exists()

    query_set[0:5]

    for product in query_set:
        print(product)
    return render(request, 'hello.html', {'name': 'Mosh'})

def say_hello2(request):
    result = Product.objects.filter(unit_price__gt = 20) # __gt è greater than, è la keyword per filtrare, cerca queryset api per le altre (fields lookups)
    queryset = Product.objects.filter(unit_price__range = (20,30))
    return render(request, 'hello.html', {'name': 'Mirko', 'products': result})

def say_hello3(request):
    queryset = Product.objects.filter(title__icontains = 'coffee')
    return render(request, 'hello.html', {'name': 'Mirko', 'products': queryset})

def say_hello4(request):
    queryset = Product.objects.filter(Q(inventory__lt = 10) | Q(unit_price__lt=20)) # or, i Q objects servono per poter fare questo, potrei mettere anche and ma è meglio usare due filtri concatenati perchè è più semplice da leggere
    return render(request, 'hello.html', {'name': 'Mirko', 'products': queryset})

def say_hello4(request):
    # facciamo finta di volere i prodotti il quale ammontare ad inventario sia uguale al proprio prezzo
    queryset = Product.objects.filter(inventory = F('unit_price')) # devo usare gli F objects
    return render(request, 'hello.html', {'name': 'Mirko', 'products': queryset})

def say_hello5(request):
    
    queryset = Product.objects.order_by('unit_price', '-title') # unit price ascending title descenting
    return render(request, 'hello.html', {'name': 'Mirko', 'products': queryset})


def say_hello6(request):
    queryset = Product.objects.all[:5] # i primi 5 oggetti
    return render(request, 'hello.html', {'name': 'Mirko', 'products': queryset})

def say_hello7(request):
    
    # values restituisce tra le varie cose, un dizionario di elementi e non un oggetto di tipo queryset
    Product.objects.values('id', 'title', 'collection__title') # proiezione sulle colonne che ci interessano, più innerjoin su collection.title
    # values list invece restituisce una tupla al posto di un dizionario
    
    # Prodotti che sono stati ordinati, in ordine ascendente per titolo
    Product.objects.filter(id__in = OrderItem.objects.values('product_id').distinct()).order_by('title')


    Product.objects.only('id', 'title') # specifichiamo i campi che vogliamo, come values, solo che non otteniamo dizionari
    # c'è da stare attenti perchè a differenza dei dizionari, se vado poi a printare una colonna che non ho selezionato farà una query per prendere il valore di tale colonna, ma per ogni oggetto nel nostro db

    Product.objects.defer('description') # tutto tranne description


    Product.objects.select_related('collection').all() # è una join con collection, che però è 1:1


    Product.objects.prefetch_related('promotions').all() # è una join con promotions che è 1:n

    Product.objects.prefetch_related('promotions').select_related('collection').all()

    Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5] # orderitem_set è il nome di default della relazione inversa che ha order su orderitem dato che su orderitem ho una relazione diretta su order

    Product.objects.aggregate(Count('id'), min_price = Min('unit_price')) # ci restituisce un dizionario

    # how many orders do we have
    Order.objects.aggregate(Count('id'))

    # how many units of product 1 have we sold
    OrderItem.objects.filter(product__id = 1).aggregate(Sum('quantity'))

    #How many orders has customer 1 placed?
    Order.objects.filter(customer__id = 1).aggregate(Count('id'))

    # What is the min, max and average price of the products in collection 3?
    Product.objects.filter(collection_id = 3).aggregate(Min('unit_price'), Max('unit_price'), Avg('unit_price'))



    Customer.objects.annotate(is_new = Value(True)) # attributi addizionali da mettere nella query di ritorno, va wrappato in Value, che è un sottotipo di Expression
    
    Customer.objects.annotate(new_id = F('id')) # creiamo new_id e mettiamo gli stessi valori referenziati da id (bisogna farlo con F)

    Customer.objects.annotate( full_name = Func(F('first_name'), Value(' '), F('last_name'), function = 'CONCAT') ) # Stiamo utilizzando una funzione del DBMS chiamata CONCAT

    Customer.objects.annotate(full_name = Concat('first_name', Value(' '), 'last_name')) # Sto utilizzando una funzione di django importata sopra per fare la concatenazione, che chiamerà la funzione apposita del DBMS che c'è sotto

    #Numero di ordini per ogni customer, per qualche motivo non server order_set ma order
    Customer.objects.annotate(orders_count = Count('order'))

    Product.objects.annotate(discounter_price = ExpressionWrapper(F('unit_price') * 0.8, output_field = DecimalField())) # per fare query complesse serve un ExpressionWrapper

    
    # Customers with .com accounts
    Customer.objects.filter(email__icontains = '.com')

    # Collections that don't have a featured product
    Collection.objects.filter(featured_product__isnull = True)

    # Products with low inventory (less than 10)
    Product.objects.filter(inventory__lt = 10)

    # Orders placed by customer with id = 1
    Order.objects.filter(customer__id = 1).aggregate(Count('id'))

    # Order items for products in collection 3
    OrderItem.objects.filter(product__collection__id = 3)


    # Metodo per poter connettere due moduli stagni tra di loro, come prendere i tag di un determinato product
    content_type = ContentType.objects.get_for_model(Product)
    queryset = TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type = content_type,
                object_id = 1  # questo dovrebbe essere dinamico, ma per ora prendiamo l'id 1
            )
    # abbiamo spostato questo codice in tags, così da avere sempre questo metodo sotto mano
    queryset = TaggedItem.objects.get_tags_for(Product, 1)



    # creazione di una nuova collezione INSERT INTO 
    collection = Collection()
    collection.title = 'Video Games'
    collection.featured_product = Product(pk = 1)
    collection.save()

    # update di una collezione UPDATE
    collection = Collection.objects.get(pk = 11) # ovviamente l'oggetto con questa pk deve esistere, l'oggetto va prelevato, altrimenti in caso di omissione di alcuni campi ed update di solo alcuni, verranno azzerati a quello esistente
    collection.title = 'Games'
    collection.featured_product = None
    collection.save()

    Collection.objects.filter(pk=11).update(featured_product = None) # alternativamente ho questa notazione per fare l'update ma se cambio il nome del parametro in futuro questo pezzo di codice si romperà, è più sicuro quello sopra anche se fa una get prima di eseguire update


    # eliminazione di una collezione
    collection = Collection(pk = 11)
    collection.delete()

    # eliminazione di molteplici collezioni
    Collection.objects.filter(id__gt = 5).delete()

    # transazione atomica
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()


    queryset = Product.objects.raw('SELECT * FROM store_product') # questo è per fare una query grezza, il queryset ritornato da questa funzione è diverso dal classico queryset

    with connection.cursor() as cursor:
        #cursor.execute()
        cursor.callproc('get_customers', [1, 2, 'a']) # chiamata a funzione SQL con annessi parametri

    return render(request, 'hello.html', {'name' : 'Mirko', 'products': queryset})



# alternativamente aggiungendo questo decoratore, l'intera transazione della funzione sarà atomica, e se fallisce a metà non lascerà inconsistenze ma effettuerà rollback
@transaction.atomic()
def atomic_transaction(request):
    order = Order()
    order.customer_id = 1
    order.save()

    item = OrderItem()
    item.order = order
    item.product_id = 1
    item.quantity = 1
    item.unit_price = 10
    item.save()

    return render(request, 'hello.html')