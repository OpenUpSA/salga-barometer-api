import coreapi
import coreschema
from rest_framework import generics
from rest_framework.schemas import AutoSchema

from .exceptions import TooManyResultsException

from .models import (Govcat, Gov,
                     Govindicatorrank, Indicator,
                     Mandategroup, Grouping,
                     Govrank,
                     Govindicator,
                     Yearref)

from .serializers import (CategorySerializer,
                          CategoryDescriptionSerializer,
                          GovernmentDetailSerializer,
                          IndicatorRankSerializer,
                          MandateGroupSerializer,
                          GroupingSerializer,
                          SubGroupingSerializer,
                          GovernmentRankingSerializer,
                          IndicatorValueSerializer,
                          MandateDetailSerializer,
                          YearSerializer)


class CategoryView(generics.ListAPIView):
    """
    Return a list of all the government categories.
    """
    serializer_class = CategorySerializer

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

    serializer_class = CategoryDescriptionSerializer

    def get_queryset(self):
        gcid = self.kwargs['gcid']
        return Govcat.objects.filter(gcid=gcid)


class GovernmentDetailView(generics.ListAPIView):
    """
    Return details about a particular government.
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            'govid',
            required=True,
            location='path',
            schema=coreschema.String(
                description='Unique identifier for a gorvernment'
            )
        ),
    ])
    serializer_class = GovernmentDetailSerializer

    def get_queryset(self):
        govid = self.kwargs['govid']
        return Gov.objects.filter(govid=govid)


class GovernmentIndicatorRankingView(generics.ListAPIView):
    """
    Return indicator rankings for a government
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
    serializer_class = IndicatorRankSerializer

    def get_queryset(self):
        govid = self.kwargs['govid']
        year = self.request.query_params.get('year', None)
        if year is not None:
            return Govindicatorrank.objects.filter(
                govid_id=govid,
                yearid__yr=year
            )
        return Govindicatorrank.objects.filter(govid_id=govid)


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
    serializer_class = GovernmentRankingSerializer

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
    serializer_class = GroupingSerializer

    def get_queryset(self):
        group_id = self.request.query_params.get('gid', None)
        if group_id is not None:
            return Grouping.objects.filter(gid=group_id)
        return Grouping.objects.filter(parentgid__isnull=True)


class SubGroup(generics.ListAPIView):
    """
    Return a list of subgroups for a group
    """
    serializer_class = SubGroupingSerializer

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
            'year',
            required=True,
            location='query',
            schema=coreschema.String(
                description='full year of ranking eg: 2016'
            )
        ),
        coreapi.Field(
            'gid',
            required=True,
            location='query',
            schema=coreschema.String(
                description='Unique identifier for a subgroup'
            )
        )
    ])
    serializer_class = IndicatorValueSerializer

    def get_queryset(self):
        subgroup_id = self.kwargs['gid']
        gov_id = self.request.query_params.get('gov', None)
        year = self.request.query_params.get('year', None)
        if gov_id is None or year is None:
            raise TooManyResultsException()
        else:
            indi_exists = Indicator\
                     .objects\
                     .filter(parentgid=subgroup_id)\
                     .exists()
            if not indi_exists:
                return Govindicator\
                    .objects\
                    .only('value', 'iid__name', 'iid__parentgid__name')\
                    .filter(govid=gov_id,
                            yearid__yr=year,
                            iid__parentgid__parentgid=subgroup_id
                    )\
                    .select_related('iid')
            return Govindicator\
                .objects\
                .only('value', 'iid__name', 'iid__parentgid__name')\
                .filter(
                    govid__name=gov_id,
                    yearid__yr=year,
                    iid__parentgid=subgroup_id
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
    serializer_class = MandateGroupSerializer

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

    serializer_class = MandateDetailSerializer

    def get_queryset(self):
        mandate_id = self.kwargs['mgid']
        return Indicator.objects.filter(mgid=mandate_id)


class YearView(generics.ListAPIView):
    """
    Return all the avaliable years
    """
    serializer_class = YearSerializer

    def get_queryset(self):
        return Yearref.objects.all()
