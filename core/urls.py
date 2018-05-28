from django.views.decorators.cache import cache_page
from django.conf.urls import url


from . import views

urlpatterns = [
    # url(r'^$', views.api_root, name='home'),

    url(r'^categories$',
        cache_page(600)(views.CategoryView.as_view()),
        name='category'),
    url(r'^categories/(?P<gcid>[\d]+)$',
        cache_page(600)(views.CategoryDescriptionView.as_view()),
        name='category_description'),

    url(r'^governments$',
        cache_page(600)(views.GovernmentsView.as_view()),
        name='government'),
    url(r'^governments/(?P<govid>[\d]+)$',
        cache_page(600)(views.GovernmentDetailView.as_view()),
        name='government_detail'),
    url(r'governments/indicators/(?P<govid>[\d]+)$',
        cache_page(600)(views.GovernmentIndicatorView.as_view()),
        name='government_indicators'),

    # Rankings
    url(r'^rankings/indicators/categories/(?P<cat_id>[\d+])$',
        cache_page(600)(views.CategoryIndicatorOverallRankView.as_view()),
        name='rankings_category_indicator'),
    url(r'^rankings/indicators/governments/(?P<govid>[\d]+)$',
        cache_page(600)(views.GovernmentIndicatorRankingView.as_view()),
        name='rankings_indicator'),
    url(r'^rankings/mandates/categories/(?P<cat_id>[\d]+)$',
        cache_page(600)(views.GovernmentMandateRankingView.as_view()),
        name='rankings_category_government'),
    url(r'^rankings/governments/(?P<govid>[\d]+)$',
        cache_page(600)(views.GovernmentRankingView.as_view()),
        name='rankings_government'),

    # Benchmarks
    url(r'^benchmarks/mandates$',
        cache_page(600)(views.BenchmarkMandateView.as_view()),
        name='benchmark_mandates'),
    url(r'^benchmarks/indicators/(?P<indicator>[\d]+)$',
        cache_page(600)(views.BenchmarkIndicatorView.as_view()),
        name='benchmarks_indicators'),

    url(r'^mandate$',
        cache_page(600)(views.MandateView.as_view()),
        name='mandate'),
    url(r'^mandate/(?P<mgid>[\d]+)$',
        cache_page(600)(views.MandateDetailView.as_view()),
        name='mandate_detail'),

    url(r'^groupings$',
        cache_page(600)(views.GroupView.as_view()),
        name='grouping'),
    url(r'^groupings/(?P<gid>[\d]+)$',
        cache_page(600)(views.GroupDetailView.as_view()),
        name='sub_group'),
    url(r'^groupings/subgroups/(?P<gid>[\d]+)$',
        cache_page(600)(views.SubGroupIndicatorView.as_view()),
        name='subgroup_indicators'),
    url(r'^years$',
        cache_page(600)(views.YearView.as_view()),
        name='year')

]
