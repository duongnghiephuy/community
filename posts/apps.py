from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "posts"

    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        from . import signals
