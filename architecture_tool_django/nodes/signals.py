# from django.core import serializers
import os

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Node
from .tasks import update_component_page_task

# from django.forms.models import model_to_dict


@receiver(post_save, sender=Node)
def node_post_save_handler(sender, instance, created, **kwargs):
    # if created:
    #     pass
    # data = serializers.serialize("json", [instance])
    # print(model_to_dict(instance, exclude=["created", "updated", "target_nodes"]))
    # print(data)
    if os.getenv("SYNC_TO_CONFLUENCE", default=False):
        transaction.on_commit(lambda: update_component_page_task.delay(instance.key))
