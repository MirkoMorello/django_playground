from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class likedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # swappato user con l'auth trovato nelle settings, questo perchè ho overridato user in un altro pacchetto (core) ma non posso importarlo altrimenti likes ne diventa dipendente
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField() # Nella speranza che la PK sia effettivamente un integer
    content_object = GenericForeignKey()
