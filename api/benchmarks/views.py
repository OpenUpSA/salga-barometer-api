import coreapi
import coreschema
from rest_framework.schemas import AutoSchema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from core.models import (Yearref,
                         Govrank,
                         Govindicatorrank)


class BenchmarkMandateView(APIView):
    """
    Return mandate rankings for for a particular government category
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'category',
            required=True,
            location='query',
            schema=coreschema.String(
                description='Unique government category ID'
            )
        ),
        coreapi.Field(
            'year',
            required=False,
            location='query',
            schema=coreschema.String(
                description='full year eg: 2016'
            )
        ),
    ])

    def get(self, request, format=None):
        year = self.request\
                   .query_params.get('year',
                                     Yearref.objects.latest('yearid').yr)
        category = self.request.query_params.get('category', None)
        if category is None:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        query = Govrank\
                .objects\
                .filter(govid__gcid=category,
                        yearid__yr=year)
        serialize = serializers.BenchmarkMandateSerializer(
            query,
            context={'request': request},
            many=True,
            )

        return Response(
            {'results': serialize.data}
        )


class BenchmarkIndicatorView(APIView):
    """
    Return a particular mandate indicator ranking for all governments
    within a particular government category
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'indicator',
            required=True,
            location='path',
            schema=coreschema.String(
                description='mandate indicator id'
            )
        ),
        coreapi.Field(
            'year',
            required=False,
            location='query',
            schema=coreschema.String(
                description='year eg: 2016'
            )
        ),
        coreapi.Field(
            'category',
            required=False,
            location='query',
            schema=coreschema.String(
                description='government category id'
            )
        ),
    ])

    def get(self, request, indicator, format=None):
        year = self.request.query_params.get('year',
                                             Yearref.objects.latest('yearid').yr)
        category = self.request.query_params.get('category', None)
        if category is None:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        query = Govindicatorrank.objects.filter(
            yearid__yr=year,
            iid=indicator,
            govid__gcid=category
        )
        serialize = serializers.IndicatorRankSerializer(
            query,
            context={'request': request},
            many=True,
        )
        return Response(
            {'results': serialize.data}
        )
