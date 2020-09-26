from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
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
    def __init__(self, *args, **kwargs):
        super(SchemaCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "key",
            Field("schema", id="textarea-codemirror"),
        )

    class Meta:
        model = Schema
        fields = (
            "key",
            "schema",
        )


class SchemaUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SchemaUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "key",
            Field("schema", id="textarea-codemirror"),
        )

    class Meta:
        model = Schema
        fields = (
            "key",
            "schema",
        )
