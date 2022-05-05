from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import UserProfile, Community

# This is to delete post_image in media folder after a post is deleted


@receiver(post_delete, sender=UserProfile)
def delete_associated_files(sender, instance, **kwargs):

    """Remove all files of an image after deletion."""
    path = instance.avatar.name
    if path:
        default_storage.delete(path)


@receiver(post_delete, sender=Community)
def delete_associated_files(sender, instance, **kwargs):

    """Remove all files of an image after deletion."""
    path = instance.image.name
    if path:
        default_storage.delete(path)
