from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms

from .models import Nodetype, Schema


class NodeTypeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NodeTypeCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"
        self.helper.layout = Layout(
            Div(
                "key",
                "name",
                "description",
                "umlType",
                "keyFormat",
                "inherits",
                "folder",
                css_class="card-body",
            ),
            Div(
                Submit("submit", "Submit"),
                HTML(
                    '<a class="btn btn-default float-right" href="{% url "modeling:nodetype.list" %}">Cancel</a>'
                ),
                css_class="card-footer",
            ),
        )

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
    def __init__(self, *args, **kwargs):
        super(NodeTypeUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"
        self.helper.layout = Layout(
            Div(
                Field("key", readonly=True),
                "name",
                "description",
                "umlType",
                "keyFormat",
                "inherits",
                "folder",
                css_class="card-body",
            ),
            Div(
                Submit("submit", "Submit"),
                HTML(
                    '<a class="btn btn-default float-right" href="{% url "modeling:nodetype.list" %}">Cancel</a>'
                ),
                css_class="card-footer",
            ),
        )

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
        self.helper.layout = Layout(
            Div(
                "key",
                Field("schema", id="textarea-codemirror"),
                css_class="card-body",
            ),
            Div(
                Submit("submit", "Submit"),
                HTML(
                    '<a href="#" class="btn btn-primary float-left mr-2" id="format">Format</a>'
                ),
                css_class="card-footer",
            ),
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
        self.helper.layout = Layout(
            Div(
                Field("key", readonly=True),
                Field("schema", id="textarea-codemirror"),
                css_class="card-body",
            ),
            Div(
                Submit("submit", "Submit"),
                HTML(
                    '<a href="#" class="btn btn-primary float-left mr-2" id="format">Format</a>'
                ),
                HTML(
                    '<a href="#" class="btn btn-primary float-left mr-2" data-toggle="modal" data-target="#modal-diff">'
                    + "Preview</a>"
                ),
                css_class="card-footer",
            ),
        )

    class Meta:
        model = Schema
        fields = (
            "key",
            "schema",
        )
