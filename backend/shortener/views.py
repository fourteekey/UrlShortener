import datetime
import logging
import secrets
import requests
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework.views import APIView

from system_conf.redis import Redis
from .serializers import *

logger = logging.getLogger(__name__)


def check_user_session(request):
    """
    Создает сессию или обновляет время ее действия.
    """
    # user = request.session.get('user_key', None)
    # if not user: request.session['user_key'] = 1
    request.session.modified = True


class GeneratorAPIView(APIView):
    def get(self, request):
        page_number = request.query_params.get('page', 1)
        urls_list = UrlsModel.objects.filter(session_key=request.session.session_key)

        # Пагинация
        paginator = Paginator(urls_list, 5)
        if paginator.num_pages < int(page_number):
            return Response({'error': 'На странице отсутствует контент'}, status=status.HTTP_204_NO_CONTENT)
        urls_list = paginator.page(page_number)
        serializer = UrlSerializer(urls_list, many=True, context={"request": request}).data

        return Response({'current_page': int(page_number), 'max_page': paginator.num_pages, 'content': serializer})

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'origin_url': openapi.Schema(type=openapi.TYPE_STRING,
                                             description='Урл на который произойдет редирект.'),
                'short_url': openapi.Schema(type=openapi.TYPE_STRING,
                                            description='Короткое название для новой сссылке. '
                                                        'НЕОБЯЗАТЕЛЬНО к заполнению.')
            }
        ))
    def post(self, request):
        origin_url = request.data.get('origin_url', None)
        short_url = request.data.get('short_url', None)
        if not origin_url:
            return Response({'detail': 'url cannot be empty',
                                            'detail_ru': 'Поле "ссылка" не может быть пустым'},
                                           status=status.HTTP_400_BAD_REQUEST)
        try:
            rq = requests.get(origin_url, timeout=2)
        except Exception as e:
            logger.error(f'Cannot open original url: {origin_url} | {e}')
            rq = None

        if (rq and rq.status_code != 200) or not rq:
            return Response({'detail': 'Incorrect  url',
                             'detail_ru': 'Введенный урл некоректен или вебсайт сейчас недоступен.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif short_url and UrlsModel.objects.filter(short_url=short_url):
            return Response({'detail': 'Duplicate url name',
                             'detail_ru': 'Короткое имя не уникально используйте другое'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif not short_url: short_url = secrets.token_urlsafe(5)

        redis = Redis()
        redis.set(short_url, origin_url)
        UrlsModel.objects.create(session_key=request.session.session_key, origin_url=origin_url, short_url=short_url)

        return Response({'short_url': short_url}, status=status.HTTP_201_CREATED)


def index_page(request):
    if request.path == '/':
        check_user_session(request)
        return render(request, 'index.html',
                      {'user_urls': UrlsModel.objects.filter(session_key=request.session.session_key)})
    else:
        """
        Можно доработать и счетчик хранить в редис. А потом раз в 5-10 мин обновлять данные во всех записях.
        Но тут проект маленький и это незначительно.
        """
        data_url = get_object_or_404(UrlsModel, short_url=request.path[1:])  # Убираем /
        data_url.counter += 1
        data_url.save()
        return HttpResponseRedirect(data_url.origin_url)
