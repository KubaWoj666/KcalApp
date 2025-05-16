from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WeightEntry, UserAccount

@receiver(post_save, sender=WeightEntry)
def update_user_weight(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.weight = instance.weight
        user.save()