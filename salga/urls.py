from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
import debug_toolbar


urlpatterns = [
    url(r'^api/v1/', include('api.urls', namespace='api')),
    url(r'^', include_docs_urls(title='Salga Barometer API')),
    url(r'^__debug__/', include(debug_toolbar.urls)),
]
