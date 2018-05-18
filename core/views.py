import coreapi
import coreschema
from rest_framework import generics
from rest_framework.schemas import AutoSchema
from rest_framework import exceptions
from rest_framework import decorators
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import NotEnoughParameters
from . import averages

from .models import (Govcat, Gov,
                     Govindicatorrank, Indicator,
                     Mandategroup, Grouping,
                     Govrank,
                     Govindicator,
                     Yearref)

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
        query = Govcat.objects.get(gcid=gcid)
        serialize = serializers.CategoryDescriptionSerializer(
            query,
            context={'request': request},
        )
        return Response(
            {'results': serialize.data}
        )


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
    Return overview details about a government
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
    Return government indicator values
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
                description='Unique identifier for subgroup'
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
        year = request.query_params.get(
            'year',
            Yearref.objects.latest('yearid').yr
        )
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
            raise NotEnoughParameters()

        serialize = serializers.IndicatorValueSerializer(
            query,
            context={'request': request},
            many=True
        )

        return Response(
            {
                'results': serialize.data
            }
        )


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
        year = request.query_params.get(
            'year',
            Yearref.objects.latest('yearid').yr
        )
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
            {'results': serialize.data}
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
        )
    ])

    def get(self, request, govid):
        year = self.request.query_params.get(
            'year', Yearref.objects.latest('yearid').yr
        )
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
             'ranking_out_of': ranking_total}
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
        year = self.request.query_params.get(
            'year',
            Yearref.objects.latest('yearid').yr
        )

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
            {'results': serialize.data}
        )


class GovernmentRankingView(APIView):
    """
    Return the mandate scores for a government
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


class GroupView(APIView):
    """
    Return a list of the top level indicator groupings
    """
    def get(self, request, format=None):
        query = Grouping.objects.filter(parentgid__isnull=True)
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
        query = Grouping.objects.filter(parentgid=gid)
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
            query = Grouping.objects.filter(gid=gid)
        else:
            query = Grouping.objects.filter(parentgid=gid)

        serialize = serializers.GroupingSerializer(
            query,
            context={'request': request},
            many=True
        )

        return Response(
            {'results': serialize.data}
        )


@decorators.api_view(['GET'])
def government_indicators(request, govid):
    """
    Return government indicator values
    """
    indicators = request.query_params.get('indicator', None)
    year = request\
           .query_params\
           .get('year', Yearref.objects.latest('yearid').yr)
    if indicators:
        indi = indicators.split(',')
        results = Govindicator.objects.filter(
            govid=govid,
            yearid__yr=year,
            iid__parentgid__in=indi
        )
        serializer = serializers.GovernmentIndicatorSerializer(
            results,
            context={'request': request}
        )
    return Response({
        serializer.data
    })


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
