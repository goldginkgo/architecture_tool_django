from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms

from .models import Graph


class GraphCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GraphCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "key",
            Field("graph", id="textarea-codemirror"),
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
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field("key", readonly=True),
            Field("graph", id="textarea-codemirror"),
        )

    class Meta:
        model = Graph
        fields = (
            "key",
            "graph",
        )
