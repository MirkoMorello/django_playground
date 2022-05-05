# Appunti corso  

## Prima parte

    pipenv shell
per inizializzare l'environment

    django-admin startproject testProject
per iniziare un nuovo progetto

    python manage.py
da gli stessi comandi di django

    python manage.py runserver

    python manage.py startapp store
per inizializzare una nuova app

    python manage.py makemigrations
per creare i file di migrazione che possono effettivamente poi essere uploadati su github, devi mettere le app nella lista delle applicazioni per farle migrare, altrimenti non verranno selezionate

    python magage.py migrate
per migrare effettivamente i dati su questo dispositivo

    python manage.py sqlmigrate store 0003
per vedere i comandi sql effettuati in quella migration
dentro sqlite, in django migrations puoi vedere tutto il flow delle migrazioni effettuate

    python manage.py migrate store 0003
per revertare una qualsivoglia migrazione ad un determinato punto

    git reset --hard HEAD~1
per tornare indietro di un commit

    python manage.py makemigrations store --empty
per creare una migrazione vuota

Django ORM serve per fare query in maniera semplice attraverso python, le query sono dette lazy, vengono evaluate all'ultimo

    python manage.py createsuperuser
per creare un superuser

    python manage.py changepassword user
per cambiare password a user

cerca django modeladmin per controllare tutte le cose customizzabili per le app nella dashboard admin

-----------------
## API

#### REST:
Resources (come product, cart, reviews), dovremmo riuscire ad arrivarci tramite http://nomesito.com/products/1/reviews/1
Representations: html/xml/json
Methods: metodi http Get ottenere/Post creare/Put modificare/Patch modificare singola cosa/Delete eliminare

abbiamo aggiunto tramite pipenv restframework e l'abbiamo aggiunto alle installed apps, che permette di vedere per bene le nostre api quando visito attraverso browser
in Views metto le funzioni che rispondono alle chiamate http, in urls le abilito
JsonRenderer prende un oggetto di tipo dizionario e lo trasforma in json
Serializer converte un modello in un dizionario  

Il nostro modello API è ben diverso dal nostro Data Model, ed è giusto che continui ad essere così, l'API model deve essere una interfaccia dell'implementazione Data Model che deve rimanere nascosta, in modo tale che rimanga stabile  

Mixin, serve per creare classi di views generiche  

Ricapitolando:  
Per creare una api serve:  
- creare un serializer
- una view
- registrare la route

#### drf nested routers, su github
usiamo questo pacchetto per poter fare risorse innestate