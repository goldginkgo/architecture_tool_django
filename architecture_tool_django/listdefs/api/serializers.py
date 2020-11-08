from collections import OrderedDict

import jsonschema
from jsonschema import Draft4Validator
from rest_framework import serializers

from architecture_tool_django.modeling.models import Schema

from ..models import List


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ["key", "schema", "listdef"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        return OrderedDict([(key, ret[key]) for key in ret if ret[key] is not None])

    def validate_listdef(self, value):
        s = self.get_initial().get("schema")
        v = Draft4Validator(
            Schema.objects.get(pk=s).schema,
            format_checker=jsonschema.FormatChecker(),
        )
        errors = []
        for error in v.iter_errors(value):
            errors.append(error.message)

        if errors:
            raise serializers.ValidationError(errors)

        return value
