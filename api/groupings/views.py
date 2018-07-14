import coreapi
import coreschema

from rest_framework.schemas import AutoSchema
from rest_framework.response import Response
from rest_framework.views import APIView


from core.models import Grouping, Indicator
from . import serializers


class GroupView(APIView):
    """
    Return a list of the top level indicator groupings
    """
    def get(self, request, format=None):
        query = Grouping\
                .objects\
                .filter(parentgid__isnull=True)\
                .select_related('parentgid')
        serialize = serializers.GroupingSerializer(
            query,
            context={'request': request},
            many=True
        )

        return Response(
            {'results': serialize.data}
        )


class GroupDetailView(APIView):
    """
    Return a list of subgroups for a particular top level group
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'gid',
            required=True,
            location='path',
            schema=coreschema.String(
                description='Unique top level group identifier'
            )
        ),
    ])

    def get(self, request, gid, format=None):
        query = Grouping.objects\
                        .filter(parentgid=gid)\
                        .select_related('parentgid')
        serialize = serializers.SubGroupingSerializer(
            query,
            context={'request': request},
            many=True
        )

        return Response(
            {'results': serialize.data}
        )


class SubGroupIndicatorView(APIView):
    """
    Return a list of a subgroups indicators
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'gid',
            required=True,
            location='path',
            schema=coreschema.String(
                description='Unique group identifier'
            )
        ),
    ])

    serializer_class = serializers.GroupingSerializer

    def get(self, request, gid, format=None):
        indi_exists = Indicator\
                      .objects\
                      .filter(parentgid=gid)\
                      .exists()
        if indi_exists:
            query = Grouping.objects\
                            .filter(gid=gid)\
                            .select_related('parentgid')
        else:
            query = Grouping.objects\
                            .filter(parentgid=gid)\
                            .select_related('parentgid')

        serialize = serializers.GroupingSerializer(
            query,
            context={'request': request},
            many=True
        )

        return Response(
            {'results': serialize.data}
        )
