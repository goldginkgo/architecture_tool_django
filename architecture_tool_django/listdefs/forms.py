import jsonschema
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms
from django.core.exceptions import ValidationError
from jsonschema import Draft4Validator

from .models import List


class ListdefCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ListdefCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.attrs["novalidate"] = True
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-lg-1"
        self.helper.field_class = "col-lg-11"
        self.helper.layout = Layout(
            Div(
                "key",
                "schema",
                Field("listdef", id="textarea-codemirror"),
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

    def clean_listdef(self):
        schema = self.cleaned_data["schema"].schema
        data = self.cleaned_data["listdef"]
        v = Draft4Validator(schema, format_checker=jsonschema.FormatChecker())
        errors = []
        for error in v.iter_errors(data):
            errors.append(error.message)

        if errors:
            raise ValidationError(errors)

        return data

    class Meta:
        model = List
        fields = (
            "key",
            "schema",
            "listdef",
        )


class ListdefUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ListdefUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.attrs["novalidate"] = True
        self.helper.form_group_wrapper_class = "row"
        self.helper.label_class = "col-lg-1"
        self.helper.field_class = "col-lg-11"
        self.helper.layout = Layout(
            Div(
                Field("key", readonly=True),
                Field("schema", disabled=True),
                Field(
                    "schema", type="hidden"
                ),  # Add hidden value as disabled form elements are not sent by the form
                Field("listdef", id="textarea-codemirror"),
                css_class="card-body",
            ),
            Div(
                HTML(
                    '<button type="button" class="btn btn-primary float-left mr-2" id="format">Format</button>'
                ),
                HTML(
                    '<button type="button" class="btn btn-primary float-left mr-2" data-toggle="modal" '
                    + 'data-target="#modal-diff">Preview</button>'
                ),
                Submit("submit", "Submit"),
                css_class="card-footer",
            ),
        )

    def clean_listdef(self):
        schema = self.cleaned_data["schema"].schema
        data = self.cleaned_data["listdef"]
        v = Draft4Validator(schema, format_checker=jsonschema.FormatChecker())
        errors = []
        for error in v.iter_errors(data):
            errors.append(error.message)

        if errors:
            raise ValidationError(errors)

        return data

    class Meta:
        model = List
        fields = (
            "key",
            "schema",
            "listdef",
        )
