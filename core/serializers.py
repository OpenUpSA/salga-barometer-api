from .models import (Govcat,
                     Gov, Govindicatorrank,
                     Indicator, Grouping,
                     Mandategroup, Govrank,
                     Govindicator, Yearref)

from rest_framework import serializers
from rest_framework.reverse import reverse


class GovernmentMandateLink(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        print(type(obj))
        url_kwargs = {
            'govid': obj.govid,
            'mandate':  obj.govindicator_set.iid__mgid
        }
        return reverse(view_name, kwargs=url_kwargs,
                       request=request, format=format)


class GroupingSerializer(serializers.ModelSerializer):
    subgroup_link = serializers.HyperlinkedIdentityField(
        view_name='api:sub_group',
        lookup_field='gid')
    grouping_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Grouping
        fields = ('gid', 'name', 'subgroup_link', 'grouping_set')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.HyperlinkedIdentityField(
        view_name='api:category_description',
        lookup_field='gcid')

    class Meta:
        model = Govcat
        fields = ('gcid', 'description', 'link')


class GovernmentMandateSerializer(serializers.ModelSerializer):
    year = serializers.StringRelatedField(source='yearid')
    indicator = serializers.StringRelatedField(source='iid')

    class Meta:
        model = Govindicator
        fields = ('value', 'year', 'indicator')


class GovernmentDetailSerializer(serializers.ModelSerializer):
    indicator_rank_url = serializers.HyperlinkedIdentityField(
        view_name='api:rankings_indicator',
        lookup_field='govid')
    government_rank_url = serializers.HyperlinkedIdentityField(
        view_name='api:rankings_government',
        lookup_field='govid'
    )
    group_url = GroupingSerializer(read_only=True, many=True)

    class Meta:
        model = Gov
        fields = ('govid', 'name', 'code', 'mdbcode', 'indicator_rank_url',
                  'government_rank_url', 'group_url')


class CategoryDescriptionSerializer(serializers.ModelSerializer):
    """
    Show details about a specific category with relations
    """
    gov_set = GovernmentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Govcat
        fields = ('gcid', 'description', 'gov_set')


class GovernmentRankingSerializer(serializers.ModelSerializer):
    year = serializers.StringRelatedField(source='yearid')
    idp_score = serializers.StringRelatedField(source='idpscore')
    service_del_score = serializers.StringRelatedField(
        source='servicedelscore')
    finance_score = serializers.StringRelatedField(source='financescore')
    hr_score = serializers.StringRelatedField(source='hrscore')
    combined_score = serializers.StringRelatedField(source='combinedscore')
    gov_score = serializers.StringRelatedField(source='govscore')

    class Meta:
        model = Govrank
        fields = ('ranking', 'idp_score', 'service_del_score', 'finance_score',
                  'hr_score', 'gov_score', 'combined_score', 'year')


class GovernmentIndicatorSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='iid')
    year = serializers.StringRelatedField(source='yearid')
    unit = serializers.StringRelatedField(source='iid.unitid.unit')

    class Meta:
        model = Govindicator
        fields = ('value', 'name', 'year', 'unit')


class IndicatorRankSerializer(serializers.ModelSerializer):
    indicator = serializers.StringRelatedField(source='iid')
    year = serializers.StringRelatedField(source='yearid')

    class Meta:
        model = Govindicatorrank
        fields = ('indicator', 'ranking', 'score', 'year')


class IndicatorSerializer(serializers.ModelSerializer):
    unit = serializers.StringRelatedField(source='unitid')
    group = serializers.StringRelatedField(source='parentgid')

    class Meta:
        model = Indicator
        fields = ('name', 'code', 'group', 'unit')


class GroupingSerializer(serializers.ModelSerializer):
    subgroup_link = serializers.HyperlinkedIdentityField(
        view_name='api:sub_group',
        lookup_field='gid')
    grouping_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Grouping
        fields = ('gid', 'name', 'subgroup_link', 'grouping_set')


class SubGroupHyperLink(serializers.HyperlinkedRelatedField):
    view_name = 'api:subgroup_indicators'
    queryset = Grouping.objects.all()

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'group': obj.pk,
            'subgroup': obj.pk
        }

        return reverse(view_name, kwargs=url_kwargs,
                       request=request, format=format)


class SubGroupingSerializer(serializers.ModelSerializer):
    subgroup_url = serializers.HyperlinkedIdentityField(
        view_name="api:subgroup_indicators",
        lookup_field='gid'
    )

    class Meta:
        model = Grouping
        fields = ('gid', 'name', 'subgroup_url')


class IndicatorListSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        gov_group = set([x.iid.parentgid.name for x in instance])
        groups = {}
        for group in gov_group:
            indicator_results = []
            for indi in instance:
                if indi.iid.parentgid.name == group:
                    indicator_results.append(
                        {
                            'name': indi.iid.name,
                            'value': indi.value
                        }
                    )
            groups[group.rstrip()] = indicator_results
        return [
            groups
        ]


class IndicatorValueSerializer(serializers.Serializer):
    name = serializers.StringRelatedField(source='iid.name')

    class Meta:
        list_serializer_class = IndicatorListSerializer
        model = Govindicator
        fields = ('value', 'name', 'group')


class MandateGroupSerializer(serializers.ModelSerializer):
    indicator_link = serializers.HyperlinkedIdentityField(
        view_name='api:mandate_detail',
        lookup_field='mgid')
    indicator_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Mandategroup
        fields = ('mgid', 'name', 'indicator_link', 'indicator_set')


class MandateDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Indicator
        fields = ('iid', 'name', 'code', 'scale')


class YearSerializer(serializers.ModelSerializer):

    class Meta:
        model = Yearref
        fields = ('yearid', 'yr')
