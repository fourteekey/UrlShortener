from rest_framework import serializers

from .models import *


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlsModel
        fields = ['origin_url', 'short_url', 'counter']

