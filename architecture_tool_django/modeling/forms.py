from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Field, Layout, Row, Submit
from django import forms
from django.core.exceptions import ValidationError
from jsonschema import Draft4Validator

from .models import Edgetype, Nodetype, Schema


class NodeTypeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NodeTypeCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.attrs["novalidate"] = True
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-10"
        self.helper.layout = Layout(
            Div(
                "key",
                "name",
                "description",
                "attribute_schema",
                "umlType",
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
            "attribute_schema",
            "umlType",
            "folder",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class NodeTypeUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NodeTypeUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.attrs["novalidate"] = True
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
                    Column("attribute_schema", css_class="col-md-6"),
                    Column("umlType", css_class="col-md-6"),
                ),
                Row(
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
            "attribute_schema",
            "umlType",
            "folder",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class SchemaCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SchemaCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.attrs["novalidate"] = True
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-lg-1"
        self.helper.field_class = "col-lg-11"
        self.helper.layout = Layout(
            Div(
                "key",
                "description",
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

    def clean_schema(self):
        schema = self.cleaned_data["schema"]
        try:
            Draft4Validator.check_schema(schema)
        except Exception as err:
            raise ValidationError(err.message)

        return schema

    class Meta:
        model = Schema
        fields = (
            "key",
            "description",
            "schema",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class SchemaUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SchemaUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.attrs["novalidate"] = True
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-lg-1"
        self.helper.field_class = "col-lg-11"
        self.helper.layout = Layout(
            Div(
                Field("key", readonly=True),
                "description",
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

    def clean_schema(self):
        schema = self.cleaned_data["schema"]
        try:
            Draft4Validator.check_schema(schema)
        except Exception as err:
            raise ValidationError(err.message)

        return schema

    class Meta:
        model = Schema
        fields = (
            "key",
            "description",
            "schema",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class EdgeTypeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EdgeTypeCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.attrs["novalidate"] = True
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-10"
        self.helper.layout = Layout(
            Div(
                "source_nodetype",
                "target_nodetype",
                "edgetype",
                "edgetype_name",
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
            "source_nodetype",
            "target_nodetype",
            "edgetype",
            "edgetype_name",
            "description",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class EdgeTypeUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EdgeTypeUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.attrs["novalidate"] = True
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-10"
        self.helper.layout = Layout(
            Div(
                # Field("key", readonly=True),
                "source_nodetype",
                "target_nodetype",
                "edgetype",
                "edgetype_name",
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
            "source_nodetype",
            "target_nodetype",
            "edgetype",
            "edgetype_name",
            "description",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }
