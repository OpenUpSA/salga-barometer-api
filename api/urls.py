from django.views.decorators.cache import cache_page
from django.conf.urls import url, include


from . import views

urlpatterns = [
    # url(r'^benchmarks/', include('api.benchmarks.urls',
    #                              namespace='benchmarks')),
    url(r'^categories/', include('api.categories.urls',
                                 namespace='categories')),
    url(r'^governments/', include('api.governments.urls',
                                  namespace='governments')),
    url(r'^groupings/', include('api.groupings.urls',
                                namespace='groupings')),
    url(r'^mandate/', include('api.mandate.urls',
                              namespace='mandate')),
    url(r'^rankings/', include('api.rankings.urls',
                               namespace='rankings')),

    url(r'^years$',
        cache_page(600)(views.YearView.as_view()),
        name='year')

]
