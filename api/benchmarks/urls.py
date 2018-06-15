from django.views.decorators.cache import cache_page
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^mandates$',
        cache_page(600)(views.BenchmarkMandateView.as_view()),
        name='mandates'),
    url(r'^indicators/(?P<indicator>[\d]+)$',
        cache_page(600)(views.BenchmarkIndicatorView.as_view()),
        name='indicators'),
]
