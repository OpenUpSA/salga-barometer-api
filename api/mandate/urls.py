from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    url(r'^mandate$',
        cache_page(600)(views.MandateView.as_view()),
        name='mandate'),
    url(r'^mandate/(?P<mgid>[\d]+)$',
        cache_page(600)(views.MandateDetailView.as_view()),
        name='mandate_detail'),
]
