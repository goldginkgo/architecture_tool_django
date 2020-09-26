from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms

from .models import Graph


class GraphCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GraphCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                "key",
                Field("graph", id="textarea-codemirror"),
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
        model = Graph
        fields = (
            "key",
            "graph",
        )


class GraphUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GraphUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Field("key", readonly=True),
                Field("graph", id="textarea-codemirror"),
                css_class="card-body",
            ),
            Div(
                HTML(
                    '<a href="#" class="btn btn-primary float-left mr-2" id="format">Format</a>'
                ),
                HTML(
                    '<a href="#" class="btn btn-primary float-left mr-2" data-toggle="modal" data-target="#modal-diff">'
                    + "Preview</a>"
                ),
                Submit("submit", "Submit"),
                css_class="card-footer",
            ),
        )

    class Meta:
        model = Graph
        fields = (
            "key",
            "graph",
        )
