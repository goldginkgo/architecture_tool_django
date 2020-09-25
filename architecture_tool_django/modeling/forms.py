from django import forms

from .models import Nodetype


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
