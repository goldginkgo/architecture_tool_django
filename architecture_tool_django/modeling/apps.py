from django.apps import AppConfig


class ModelingConfig(AppConfig):
    name = "architecture_tool_django.modeling"

    def ready(self):
        import architecture_tool_django.modeling.signals
