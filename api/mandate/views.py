import coreapi
import coreschema
from rest_framework.schemas import AutoSchema
from rest_framework.response import Response
from rest_framework.views import APIView


from core.models import Mandategroup, Indicator
from . import serializers


class MandateView(APIView):
    """
    Return a list of mandates
    """
    def get(self, request, format=None):
        query = Mandategroup.objects.all()
        serialize = serializers.MandateGroupSerializer(
            query,
            context={'request': request},
            many=True
        )
        return Response(
            {'results': serialize.data}
        )


class MandateDetailView(APIView):
    """
    Return details about a particular mandate
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'mgid',
            required=True,
            location='path',
            schema=coreschema.String(
                description='Unique mandate identifier'
            )
        ),
    ])

    def get(self, request, mgid, format=None):
        query = Indicator.objects.filter(mgid=mgid)
        serialize = serializers.MandateDetailSerializer(
            query,
            context={'request': request},
            many=True
        )

        return Response(
            {'results': serialize.data}
        )
