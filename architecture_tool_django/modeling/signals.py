from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Schema
from .tasks import schema_validation_task


@receiver(post_save, sender=Schema)
def schema_post_save_handler(sender, instance, created, **kwargs):
    schema_validation_task.delay(instance.key)
