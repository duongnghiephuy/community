from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import Post


@receiver(post_delete, sender=Post)
def delete_associated_files(sender, instance, **kwargs):

    """Remove all files of an image after deletion."""
    path = instance.post_image.name
    if path:
        default_storage.delete(path)
