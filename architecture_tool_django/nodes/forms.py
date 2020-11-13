import jsonschema
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms
from django.contrib.postgres.forms import JSONField
from django.core.exceptions import ValidationError
from jsonschema import Draft4Validator

from architecture_tool_django.modeling.models import Nodetype


class NodeEditForm(forms.Form):
    nodejson = JSONField(label="nodejson")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.attrs["novalidate"] = True
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-lg-1"
        self.helper.field_class = "col-lg-11"
        self.helper.layout = Layout(
            Div(
                Field("nodejson", id="textarea-codemirror"),
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

    def clean_nodejson(self):
        data = self.cleaned_data["nodejson"]
        attributeSet = data.get("attributeSet")
        nodetype = data.get("nodetype")
        v = Draft4Validator(
            Nodetype.objects.get(pk=nodetype).attribute_schema.schema,
            format_checker=jsonschema.FormatChecker(),
        )
        errors = []
        for error in v.iter_errors(attributeSet):
            errors.append(error.message)

        if errors:
            raise ValidationError(errors)

        return data
