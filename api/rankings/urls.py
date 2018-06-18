from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views
urlpatterns = [
    url(r'^indicators/categories/(?P<cat_id>[\d+])$',
        cache_page(600)(views.CategoryIndicatorOverallRankView.as_view()),
        name='category_indicator'),
    url(r'^indicators/governments/(?P<govid>[\d]+)$',
        cache_page(600)(views.GovernmentIndicatorRankingView.as_view()),
        name='indicator'),
    url(r'^mandates/categories/(?P<cat_id>[\d]+)$',
        cache_page(600)(views.GovernmentMandateRankingView.as_view()),
        name='category_government'),
    url(r'^mandates/governments/(?P<govid>[\d]+)$',
        cache_page(600)(views.GovernmentRankingView.as_view()),
        name='government'),
]
