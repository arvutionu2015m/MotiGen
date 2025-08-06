from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CVEntry

@receiver(post_save, sender=User)
def create_welcome_entry(sender, instance, created, **kwargs):
    if created:
        CVEntry.objects.create(user=instance, content="Tere tulemast MotiGeni! Lisa oma CV siia.")
