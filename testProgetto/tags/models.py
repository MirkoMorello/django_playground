from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class TaggedItemManager(models.Manager):
    # Classe apposita che eredita da Manager, ed implementa il metodo get_tags_for per poter prendere i tag dato un qualsiasi object type molto velocemente
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return TaggedItem.objects \
            .select_related('tag') \
            .filter(
                content_type = content_type,
                object_id = obj_id
            )

class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label
 
class TaggedItem(models.Model):
    # What tag applied to what item
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # Tipo generico ContentType
    object_id = models.PositiveIntegerField() # Nella speranza che la PK sia effettivamente un integer
    content_object = GenericForeignKey()    # Chiave esterna generica