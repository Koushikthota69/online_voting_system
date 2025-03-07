from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_save_profile(sender, instance, created, **kwargs):
    # Use sender and **kwargs to avoid warnings
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        if hasattr(instance, "userprofile"):
            instance.userprofile.save()
