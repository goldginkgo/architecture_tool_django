from django.core import serializers
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict

from .models import Node
from .tasks import node_post_save_task


@receiver(post_save, sender=Node)
def node_post_save_handler(sender, instance, created, **kwargs):
    if not created:
        data = serializers.serialize("json", [instance])
        print(model_to_dict(instance, exclude=["created", "updated", "target_nodes"]))
        print(data)
        node_post_save_task.delay()
