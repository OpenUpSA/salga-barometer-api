from django.conf.urls import url


from . import views

urlpatterns = [
    # url(r'^$', views.api_root, name='home'),

    url(r'^categories$', views.CategoryView.as_view(),
        name='category'),
    url(r'^categories/(?P<gcid>[\d]+)$',
        views.CategoryDescriptionView.as_view(),
        name='category_description'),

    url(r'^governments/(?P<govid>[\d]+)$',
        views.GovernmentDetailView.as_view(),
        name='government_detail'),

    # Rankings
    url(r'^rankings/indicators/(?P<govid>[\d]+)$',
        views.GovernmentIndicatorRankingView.as_view(),
        name='rankings_indicator'),
    url(r'^rankings/governments/(?P<govid>[\d]+)$',
        views.GovernmentRankingView.as_view(),
        name='rankings_government'),

    # url(r'^indicators$', views.Indicators.as_view(),
    #     name='indicator'),
    url(r'^mandate$', views.MandateView.as_view(),
        name='mandate'),
    url(r'^mandate/(?P<mgid>[\d]+)$', views.MandateDetailView.as_view(),
        name='mandate_detail'),

    url(r'^groupings$', views.Group.as_view(), name='grouping'),
    url(r'^groupings/(?P<gid>[\d]+)$', views.SubGroup.as_view(),
        name='sub_group'),
    url(r'^groupings/subgroups/(?P<gid>[\d]+)$',
        views.SubGroupIndicators.as_view(),
        name='subgroup_indicators'),
    url(r'^years$', views.YearView.as_view(), name='year')

]
