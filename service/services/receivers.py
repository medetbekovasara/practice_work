from django.db.models.signals import post_save
from django.dispatch import receiver
from services.models import Subscription

@receiver(post_save, sender=Subscription)
def delete_cache_total_sum(sender, instance, **kwargs):
    print("Сигнал сработал!")
