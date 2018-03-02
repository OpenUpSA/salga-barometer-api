from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^api/v1/', include('core.urls', namespace='api')),
    url(r'^', include_docs_urls(title='Salga Barometer API'))
]
