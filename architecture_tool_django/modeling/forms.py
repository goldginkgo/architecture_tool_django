from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Field, Layout, Row, Submit
from django import forms

from .models import Edgetype, Nodetype, Schema


class NodeTypeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NodeTypeCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-10"
        self.helper.layout = Layout(
            Div(
                "key",
                "name",
                "description",
                "schema",
                "umlType",
                "keyFormat",
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
            "schema",
            "umlType",
            "keyFormat",
            "folder",
        )


class NodeTypeUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NodeTypeUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Row(
                    Column(
                        Field("key", readonly=True), readonly=True, css_class="col-md-6"
                    ),
                    Column("name", css_class="col-md-6"),
                ),
                "description",
                Row(
                    Column("schema", readonly=True, css_class="col-md-6"),
                    Column("umlType", readonly=True, css_class="col-md-6"),
                ),
                Row(
                    Column("keyFormat", css_class="col-md-6"),
                    Column("folder", css_class="col-md-6"),
                ),
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
            "schema",
            "umlType",
            "keyFormat",
            "folder",
        )


class SchemaCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SchemaCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-lg-1"
        self.helper.field_class = "col-lg-11"
        self.helper.layout = Layout(
            Div(
                "key",
                Field("schema", id="textarea-codemirror"),
                css_class="card-body",
            ),
            Div(
                Submit("submit", "Submit"),
                HTML(
                    '<button type="button" class="btn btn-primary float-left mr-2" id="format">Format</button>'
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
        self.helper.form_class = "form-horizontal"
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-lg-1"
        self.helper.field_class = "col-lg-11"
        self.helper.layout = Layout(
            Div(
                Field("key", readonly=True),
                Field("schema", id="textarea-codemirror"),
                css_class="card-body",
            ),
            Div(
                Submit("submit", "Submit"),
                HTML(
                    '<button type="button" class="btn btn-primary float-left mr-2" id="format">Format</button>'
                ),
                HTML(
                    '<button type="button" class="btn btn-primary float-left mr-2" data-toggle="modal" '
                    + 'data-target="#modal-diff">Preview</button>'
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


class EdgeTypeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EdgeTypeCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-10"
        self.helper.layout = Layout(
            Div(
                "key",
                "name",
                "description",
                css_class="card-body",
            ),
            Div(
                Submit("submit", "Submit"),
                HTML(
                    '<a class="btn btn-default float-right" href="{% url "modeling:edgetype.list" %}">Cancel</a>'
                ),
                css_class="card-footer",
            ),
        )

    class Meta:
        model = Edgetype
        fields = (
            "key",
            "name",
            "description",
        )


class EdgeTypeUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EdgeTypeUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-10"
        self.helper.layout = Layout(
            Div(
                Field("key", readonly=True),
                "name",
                "description",
                css_class="card-body",
            ),
            Div(
                Submit("submit", "Submit"),
                HTML(
                    '<a class="btn btn-default float-right" href="{% url "modeling:edgetype.list" %}">Cancel</a>'
                ),
                css_class="card-footer",
            ),
        )

    class Meta:
        model = Edgetype
        fields = (
            "key",
            "name",
            "description",
        )
