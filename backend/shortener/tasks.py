from celery import shared_task
from datetime import timedelta
from django.utils import timezone

from .models import UrlsModel
from system_conf.redis import Redis


@shared_task
def clean_db():
    """
    Лучше переносить данные в архивную таблицу. для того чтоб в будущем ее анализировать.
    Но в данной ситуации это было некритично.

    Удаляем записи позже 48 часов с момента последнего обновления.
    """
    urls = UrlsModel.objects.filter(updated__lte=timezone.now() - timedelta(hours=48))
    redis = Redis()
    for url in urls:
        redis.delete_key(url.short_url)
    urls.delete()
