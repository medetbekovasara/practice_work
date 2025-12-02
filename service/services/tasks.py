import datetime
import time

from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.db.models import F


def set_price(subscriptions_id):
    from services.models import Subscription

    with transaction.atomic():


        subscription = Subscription.objects.select_for_update().filter(id=subscriptions_id).annotate(
            annotated_price=F('service__full_price') -
                  F('service__full_price') * F('plan_discount_percent') / 100.00).first()


        subscription.price = subscription.annotated_price
        subscription.save()
    cache.delete(settings.PRICE_CACHE_NAME)


@shared_task
def set_comment(subscriptions_id):
    from services.models import Subscription

    with transaction.atomic():

        subscription = Subscription.objects.select_for_update().get(id=subscriptions_id)

        subscription.comment = str(datetime.datetime.now())
        subscription.save()

    cache.delete(settings.PRICE_CACHE_NAME)
