import coreapi
import coreschema
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import Govcat
from . import serializers


class CategoryView(APIView):
    """
    Return a list of all the government categories.
    """
    def get(self, request, format=None):
        query = Govcat.objects.all()
        serialize = serializers.CategorySerializer(
            query,
            context={'request': request},
            many=True
        )
        return Response(
            {'results': serialize.data}
        )


class CategoryDescriptionView(APIView):
    """
    Return details about a specific government category
    """

    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'gcid',
            required=True,
            location='path',
            schema=coreschema.String(
                description='Unique identifier for gorvernment category'
            )
        ),
    ])

    def get(self, request, gcid, format=None):
        try:
            query = Govcat.objects.get(gcid=gcid)
        except Govcat.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serialize = serializers.CategoryDescriptionSerializer(
            query,
            context={'request': request},
        )
        return Response(
            {'results': serialize.data}
        )
