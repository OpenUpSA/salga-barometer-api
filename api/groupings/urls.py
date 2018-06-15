from django.views.decorators.cache import cache_page
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        cache_page(600)(views.GroupView.as_view()),
        name='grouping'),
    url(r'^(?P<gid>[\d]+)$',
        cache_page(600)(views.GroupDetailView.as_view()),
        name='subgroup'),
    url(r'^subgroups/(?P<gid>[\d]+)$',
        cache_page(600)(views.SubGroupIndicatorView.as_view()),
        name='subgroup_indicators'),
]
