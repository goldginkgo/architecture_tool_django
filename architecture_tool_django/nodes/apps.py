from django.apps import AppConfig


class NodesConfig(AppConfig):
    name = "architecture_tool_django.nodes"

    def ready(self):
        import architecture_tool_django.nodes.signals
