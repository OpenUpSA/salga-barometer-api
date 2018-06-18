from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    url(r'^$',
        cache_page(600)(views.MandateView.as_view()),
        name='mandate'),
    url(r'^(?P<mgid>[\d]+)$',
        cache_page(600)(views.MandateDetailView.as_view()),
        name='detail'),
]
