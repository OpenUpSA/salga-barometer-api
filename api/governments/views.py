import coreapi
import coreschema
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Max
from core.models import Gov, Yearref, Govindicator
from api import averages

from . import serializers


class GovernmentsView(APIView):
    """
    Return a list of all the governments
    """
    def get(self, request, format=None):
        query = Gov.objects.all()
        serialize = serializers.GovernmentDetailSerializer(
            query,
            context={'request': request},
            many=True
        )
        return Response(
            {'results': serialize.data}
        )


class GovernmentDetailView(APIView):
    """
    Return details about a particular government
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'govid',
            required=True,
            location='path',
            schema=coreschema.String(
                description='Unique identifier for a gorvernment'
            )
        ), coreapi.Field(
            'year',
            required=False,
            location='query',
            schema=coreschema.String(
                description='year'
            )
        ),
    ])

    def get(self, request, govid):
        year = request.query_params.get(
            'year',
            Yearref.objects.latest('yearid').yr
        )
        query = Gov.objects.get(govid=govid)
        serialize = serializers.GovernmentDetailSerializer(
            query,
            context={'request': request}
        )
        population = Govindicator\
                         .objects\
                         .only('iid__name', 'value', 'iid__short_name')\
                         .filter(
                             govid=govid,
                             iid__parentgid=1116,
                             yearid__yr=year
                         )

        household = Govindicator\
                    .objects\
                    .only('iid__name', 'value', 'iid__short_name')\
                    .filter(
                            govid=govid,
                            iid__parentgid=1119,
                            yearid__yr=year
                    )

        pop_density, total_population, area = averages.density(population)
        house_density, _, _ = averages.density(household)
        return Response(
            {'details': serialize.data,
             'overview': {
                'Households/km': house_density,
                'People/km': pop_density,
                'Population': total_population,
                'Area': area,
             },
             'year': year}
        )


class GovernmentIndicatorView(APIView):
    """
    Return indicator scores for a particular government
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
            'subgroup',
            required=False,
            location='query',
            schema=coreschema.String(
                description='Indicators are placed in certain '\
                'grouings, the ids of these groups can be found in '\
                '/api/v1/groupings'
            )
        ),
        coreapi.Field(
            'indicator',
            required=False,
            location='query',
            schema=coreschema.String(
                description='List of unique indicator ids'
            )
        ),
        coreapi.Field(
            'year',
            required=False,
            location='query',
            schema=coreschema.String(
                description='full year eg: 2015'
            )
        )
    ])

    def get(self, request, govid, format=None):
        subgroup = request.query_params.get('subgroup', None)
        indicators = request.query_params.get('indicator', None)
        year = request.query_params.get('year', None)
        if not year:
            year_latest = Govindicator\
                   .objects\
                   .aggregate(latest_year=Max('yearid'))
            year = Yearref.objects.get(yearid=year_latest['latest_year']).yr
        if indicators:
            indi = indicators.split(',')
            query = Govindicator.objects.filter(
                govid=govid,
                yearid__yr=year,
                iid__parentgid__in=indi
            )
        elif subgroup:
            query = Govindicator\
                .objects\
                .only('value', 'iid__name', 'iid__parentgid__name',
                      'iid__short_name')\
                .filter(
                    govid=govid,
                    yearid__yr=year,
                    iid__parentgid__parentgid=subgroup,
                )\
                .select_related('iid')
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        serialize = serializers.IndicatorValueSerializer(
            query,
            context={'request': request},
            many=True
        )

        return Response(
            {
                'results': serialize.data,
                'year': year
            }
        )
