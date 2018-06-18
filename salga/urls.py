from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^api/v1/', include('api.urls', namespace='api')),
    #url(r'^', include('rest_framework_docs.urls')),
    #url(r'^', schema_view)
    url(r'^', include_docs_urls(title='Salga Barometer API'))
]
