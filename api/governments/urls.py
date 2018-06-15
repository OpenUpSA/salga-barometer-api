from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    url(r'^$',
        cache_page(600)(views.GovernmentsView.as_view()),
        name='home'),
    url(r'^(?P<govid>[\d]+)$',
        cache_page(600)(views.GovernmentDetailView.as_view()),
        name='detail'),
    url(r'^indicators/(?P<govid>[\d]+)$',
        cache_page(600)(views.GovernmentIndicatorView.as_view()),
        name='indicators'),
]
