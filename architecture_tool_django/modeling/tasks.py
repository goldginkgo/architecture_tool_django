import logging

from celery import shared_task
from django.shortcuts import get_object_or_404
from jsonschema import Draft4Validator

from .models import Schema

logger = logging.getLogger(__name__)


@shared_task
def schema_validation_task(schema_key):
    schema = get_object_or_404(Schema, pk=schema_key)

    for nodetype in schema.nodetypes.all():
        for node in nodetype.nodes.all():
            node.validation_error = not Draft4Validator(schema.schema).is_valid(
                node.attributeSet
            )
            node.save(schema_validation_task=True)

    for li in schema.lists.all():
        li.validation_error = not Draft4Validator(schema.schema).is_valid(li.listdef)
        li.save(schema_validation_task=True)

    for graph in schema.graphs.all():
        graph.validation_error = not Draft4Validator(schema.schema).is_valid(
            graph.graph
        )
        graph.save(schema_validation_task=True)

    logger.info(
        f"Related node/list/graph validtion errors updated successfully for schema { schema_key }"
    )
