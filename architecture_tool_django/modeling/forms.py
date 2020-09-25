from django import forms

from .models import Nodetype, Schema


class NodeTypeCreateForm(forms.ModelForm):
    class Meta:
        model = Nodetype
        fields = (
            "key",
            "name",
            "description",
            "umlType",
            "keyFormat",
            "inherits",
            "folder",
        )


class NodeTypeUpdateForm(forms.ModelForm):
    class Meta:
        model = Nodetype
        fields = (
            "key",
            "name",
            "description",
            "umlType",
            "keyFormat",
            "inherits",
            "folder",
        )


class SchemaCreateForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = (
            "key",
            "schema",
        )


class SchemaUpdateForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = (
            "key",
            "schema",
        )
