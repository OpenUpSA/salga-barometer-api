import coreapi
import coreschema
from rest_framework import generics
from rest_framework.schemas import AutoSchema
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view, schema as sch
from rest_framework.response import Response

from .exceptions import TooManyResultsException, NotEnoughParameters
from . import averages

from .models import (Govcat, Gov,
                     Govindicatorrank, Indicator,
                     Mandategroup, Grouping,
                     Govrank,
                     Govindicator,
                     Yearref)

from . import serializers


class CategoryView(generics.ListAPIView):
    """
    Return a list of all the government categories.
    """
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return Govcat.objects.all()


class CategoryDescriptionView(generics.ListAPIView):
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

    serializer_class = serializers.CategoryDescriptionSerializer

    def get_queryset(self):
        gcid = self.kwargs['gcid']
        return Govcat.objects.filter(gcid=gcid)


@api_view(['GET'])
@sch(AutoSchema(manual_fields=[
        coreapi.Field(
            'govid',
            required=True,
            location='path',
            schema=coreschema.String(
                description='Unique identifier for a gorvernment'
            )
        ),
    ]))
def government_detail(request, govid):
    """
    Return overview details about a government
    """
    latest_year = Yearref.objects.latest('yearid')
    government = Gov.objects.get(govid=govid)
    serialize = serializers.GovernmentDetailSerializer(government,
                                                       context={'request': request})

    population = Govindicator\
                         .objects\
                         .only('iid__name', 'value')\
                         .filter(
                             govid=govid,
                             iid__parentgid=1116,
                             yearid=latest_year
                         )\

    household = Govindicator\
                        .objects\
                        .only('iid__name', 'value')\
                        .filter(
                            govid=govid,
                            iid__parentgid=1119,
                            yearid=latest_year
                        )\

    pop_density, total_population, area = averages.density(population)
    house_density, _, _ = averages.density(household)

    return Response(
        {
            'Details': serialize.data,
            'Overview': {
                'Households/km': house_density,
                'People/km': pop_density,
                'Population': total_population,
                'Area': area,
            },

        }
    )


class CategoryIndicatorOverallRankView(generics.ListAPIView):
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
    ])

    serializer_class = serializers.CategoryIndicatorRankSerializer

    def get_queryset(self):
        cat_id = self.kwargs['cat_id']
        year = self.request.query_params.get('year', None)
        if year is not None:
            return Govindicatorrank.objects.filter(
                govid__gcid=cat_id,
                yearid__yr=year
            ).select_related('govid', 'iid').only('ranking', 'score',
                                                  'iid__name',
                                                  'govid__name')
        latest_year = Yearref.objects.latest('yearid')
        return Govindicatorrank.objects.filter(
            govid__gcid=cat_id,
            yearid=latest_year
        ).select_related('govid', 'iid').only('ranking', 'score',
                                              'iid__name',
                                              'govid__name')


class GovernmentIndicatorRankingView(generics.ListAPIView):
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
    serializer_class = serializers.IndicatorRankSerializer

    def get_queryset(self):
        govid = self.kwargs['govid']
        year = self.request.query_params.get('year', None)
        if year is not None:
            return Govindicatorrank.objects.filter(
                govid_id=govid,
                yearid__yr=year
            )
        return Govindicatorrank.objects.filter(govid_id=govid)


class GovernmentOverrallRankingView(generics.ListAPIView):
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
    ])
    serializer_class = serializers.CategoryOverallRankingSerializer

    def get_queryset(self):
        cat_id = self.kwargs['cat_id']
        year = self.request.query_params.get('year', None)
        if year is not None:
            result = Govrank.objects.filter(
                yearid__yr=year,
                govid__gcid=cat_id
            ).order_by('ranking')
            if not result:
                raise NotFound
            return result
        latest_year = Yearref.objects.latest('yearid')
        result = Govrank.objects.filter(
            yearid=latest_year,
            govid__gcid=cat_id
        ).order_by('ranking')
        if not result:
            raise NotFound
        return result


class GovernmentRankingView(generics.ListAPIView):
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
    serializer_class = serializers.GovernmentRankingSerializer

    def get_queryset(self):
        govid = self.kwargs['govid']
        year = self.request.query_params.get('year', None)
        if year is not None:
            return Govrank.objects.filter(govid_id=govid,
                                          yearid__yr=year)
        return Govrank.objects.filter(govid_id=govid)


class Group(generics.ListAPIView):
    """
    Show all the various groupings
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'gid',
            required=True,
            location='query',
            schema=coreschema.String(
                description='Unique group identifier'
            )
        ),
    ])
    serializer_class = serializers.GroupingSerializer

    def get_queryset(self):
        group_id = self.request.query_params.get('gid', None)
        if group_id is not None:
            return Grouping.objects.filter(gid=group_id)
        return Grouping.objects.filter(parentgid__isnull=True)


class SubGroup(generics.ListAPIView):
    """
    Return a list of subgroups for a group
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
    serializer_class = serializers.SubGroupingSerializer

    def get_queryset(self):
        group_id = self.kwargs['gid']
        return Grouping.objects.filter(parentgid=group_id)


class SubGroupIndicators(generics.ListAPIView):
    """
    Return indicator values of a group for a particular government
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'gov',
            required=True,
            location='query',
            schema=coreschema.String(
                description='Unique identifier for gorvernment'
            )
        ),
        coreapi.Field(
            'gid',
            required=True,
            location='path',
            schema=coreschema.String(
                description='Unique identifier for a subgroup'
            )
        ),
        coreapi.Field(
            'indicator',
            required=False,
            location='query',
            schema=coreschema.String(
                description='Indicator Name for particular subgroup'
            )
        )
    ])
    serializer_class = serializers.IndicatorValueSerializer

    def get_queryset(self):
        subgroup_id = self.kwargs['gid']
        gov_id = self.request.query_params.get('gov', None)
        indicator = self.request.query_params.get('indicator', None)

        latest_year = Yearref.objects.latest('yearid')
        indi_exists = Indicator\
                     .objects\
                     .filter(parentgid=subgroup_id)\
                     .exists()

        if gov_id is None:
            raise NotEnoughParameters()
        if indicator is None:
            if not indi_exists:
                return Govindicator\
                    .objects\
                    .only('value', 'iid__name', 'iid__parentgid__name')\
                    .filter(govid=gov_id,
                            yearid=latest_year,
                            iid__parentgid__parentgid=subgroup_id
                    )\
                    .select_related('iid')
            else:
                return Govindicator\
                    .objects\
                    .only('value', 'iid__name', 'iid__parentgid__name')\
                    .filter(
                        govid=gov_id,
                        yearid=latest_year,
                        iid__parentgid=subgroup_id,
                    )\
                    .select_related('iid')
        else:
            if not indi_exists:
                return Govindicator\
                    .objects\
                    .only('value', 'iid__name', 'iid__parentgid__name')\
                    .filter(govid=gov_id,
                            yearid=latest_year,
                            iid__parentgid__parentgid=subgroup_id,
                            iid__parentgid__name__startswith=indicator
                    )\
                    .select_related('iid')
            return Govindicator\
                .objects\
                .only('value', 'iid__name', 'iid__parentgid__name')\
                .filter(
                    govid=gov_id,
                    yearid=latest_year,
                    iid__parentgid=subgroup_id,
                    iid__name__startswith=indicator
                )\
                .select_related('iid')


class MandateView(generics.ListAPIView):
    """
    Return a list of mandates
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
    serializer_class = serializers.MandateGroupSerializer

    def get_queryset(self):
        return Mandategroup.objects.all()


class MandateDetailView(generics.ListAPIView):
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

    serializer_class = serializers.MandateDetailSerializer

    def get_queryset(self):
        mandate_id = self.kwargs['mgid']
        return Indicator.objects.filter(mgid=mandate_id)


class YearView(generics.ListAPIView):
    """
    Return all the avaliable years
    """
    serializer_class = serializers.YearSerializer

    def get_queryset(self):
        return Yearref.objects.all()
