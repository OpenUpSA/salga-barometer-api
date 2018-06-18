import coreapi
import coreschema
from rest_framework import generics
from rest_framework.schemas import AutoSchema
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db.models import Max

from core.models import (Yearref,
                         Govindicatorrank,
                         Gov, Govrank)
from . import serializers


class CategoryIndicatorOverallRankView(APIView):
    """
    Return Overall indicator rankings for all the governments within a
    particular government category
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'cat_id',
            required=True,
            location='path',
            schema=coreschema.String(
                description='Unique identifier for a gorvernment category'
            )
        ),
        coreapi.Field(
            'year',
            required=False,
            location='query',
            schema=coreschema.String(
                description='full year of ranking eg 2016'
            )
        ),
    ])

    def get(self, request, cat_id):
        year = request.query_params.get('year', None)
        if not year:
            year_latest = Govindicatorrank\
                   .objects\
                   .aggregate(latest_year=Max('yearid'))
            year = Yearref.objects.get(yearid=year_latest['latest_year']).yr
        query = Govindicatorrank.objects.filter(govid__gcid=cat_id,
                                                yearid__yr=year)\
                                        .select_related('govid', 'iid')\
                                        .only('ranking', 'score',
                                              'iid__name', 'govid__name',
                                              'iid__short_name')

        serialize = serializers.CategoryIndicatorRankSerializer(
            query,
            context={'request': request},
            many=True
        )
        return Response(
            {'results': serialize.data,
             'year': year}
        )


class GovernmentIndicatorRankingView(APIView):
    """
    Return performance indicator rankings for a particular government.
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'govid',
            required=True,
            location='path',
            schema=coreschema.String(
                description='Unique identifier for gorvernment'
            )
        ),
        coreapi.Field(
            'year',
            required=False,
            location='query',
            schema=coreschema.String(
                description='full year of ranking eg: 2016'
            )
        ),
        coreapi.Field(
            'mandate',
            required=False,
            location='query',
            schema=coreschema.String(
                description='Unique Mandate id'
            )
        ),
        coreapi.Field(
            'indicator',
            required=False,
            location='query',
            schema=coreschema.String(
                description='Unique mandare indicator id'
            )
        )
    ])

    def get(self, request, govid):
        year = self.request.query_params.get('year', None)
        if not year:
            year_latest = Govindicatorrank\
                   .objects\
                   .aggregate(latest_year=Max('yearid'))
            year = Yearref.objects.get(yearid=year_latest['latest_year']).yr

        mandate = self.request.query_params.get('mandate', None)
        indicator = self.request.query_params.get('indicator', None)

        if indicator and mandate:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        if mandate:
            query = Govindicatorrank.objects.filter(
                govid_id=govid,
                iid__mgid=mandate,
                yearid__yr=year
            ).select_related('iid')
        elif indicator:
            query = Govindicatorrank.objects.filter(
                govid_id=govid,
                iid=indicator,
                yearid__yr=year,
            )
        else:
            query = Govindicatorrank.objects.filter(
                govid_id=govid,
                yearid__yr=year
            )
        serialize = serializers.IndicatorRankSerializer(
            query,
            context={'request': request},
            many=True
        )
        category = Gov.objects.only('gcid').get(govid=govid)
        ranking_total = Gov.objects.filter(gcid=category.gcid).count()
        return Response(
            {'results': serialize.data,
             'ranking_out_of': ranking_total,
             'year': year}
        )


class GovernmentMandateRankingView(generics.ListAPIView):
    """
    Return government rankings based on the mandate scores for a particular
    government category
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'cat_id',
            required=True,
            location='path',
            schema=coreschema.String(
                description='Unique identifier for a gorvernment category'
            )
        ),
        coreapi.Field(
            'year',
            required=False,
            location='query',
            schema=coreschema.String(
                description='full year eg: 2015'
            )
        ),
    ])

    def get(self, request, cat_id):
        year = self.request.query_params.get('year', None)
        if not year:
            year_latest = Govindicatorrank\
                   .objects\
                   .aggregate(latest_year=Max('yearid'))
            year = Yearref.objects.get(yearid=year_latest['latest_year']).yr

        query = Govrank.objects.filter(
            yearid__yr=year,
            govid__gcid=cat_id
        ).order_by('ranking')

        serialize = serializers.CategoryOverallRankingSerializer(
            query,
            context={'request': request},
            many=True
        )

        return Response(
            {'results': serialize.data,
             'year': year}
        )


class GovernmentRankingView(APIView):
    """
    Return the mandate indicator rankings for a particular government

    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'govid',
            required=True,
            location='path',
            schema=coreschema.String(
                description='Unique identifier for gorvernment'
            )
        ),
        coreapi.Field(
            'year',
            required=False,
            location='query',
            schema=coreschema.String(
                description='full year of ranking eg: 2016'
            )
        )
    ])

    def get(self, request, govid):
        year = request.query_params.get('year', None)
        try:
            if year:
                int(year)
                query = Govrank.objects.filter(
                    govid_id=govid,
                    yearid__yr=year,
                )
            else:
                query = Govrank.objects.filter(govid_id=govid)
        except Govrank.DoesNotExist:
            raise exceptions.NotFound()
        except ValueError:
            raise exceptions.ParseError()
        else:
            category = Gov.objects.only('gcid').get(govid=govid)
            ranking_total = Gov.objects.filter(gcid=category.gcid).count()
            serialize = serializers.GovernmentRankingSerializer(
                query,
                context={'request': request},
                many=True
            )

            return Response(
                {'results': serialize.data,
                 'ranking_out_of': ranking_total}
            )
