from django.db import models


class UrlsModel(models.Model):
    id = models.AutoField(primary_key=True)
    origin_url = models.CharField(max_length=150)
    short_url = models.URLField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    counter = models.IntegerField(default=0)
    session_key = models.CharField(max_length=150)

    def __str__(self):
        return self.short_url

    class Meta:
        db_table = 'shortener_urls'
        ordering = ('created',)
