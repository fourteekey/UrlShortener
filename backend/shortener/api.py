from django.urls import path
from .views import *


urlpatterns = [
    path('generator', GeneratorAPIView.as_view(), name='generator_api'),
]
