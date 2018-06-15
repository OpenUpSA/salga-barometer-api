from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    url(r'^$',
        cache_page(600)(views.CategoryView.as_view()),
        name='home'),
    url(r'^(?P<gcid>[\d]+)$',
        cache_page(600)(views.CategoryDescriptionView.as_view()),
        name='description')]
