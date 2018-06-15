from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Yearref
from . import serializers


class YearView(APIView):
    """
    Return all the avaliable years
    """
    def get(self, request, format=None):
        query = Yearref.objects.all()
        serialize = serializers.YearSerializer(
            query,
            context={'request': request},
            many=True
        )
        return Response(
            {'results': serialize.data}
        )
