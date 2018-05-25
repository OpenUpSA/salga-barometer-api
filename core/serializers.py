from rest_framework import serializers


from . import models
from . import quintiles


class SubGroupingSerializer(serializers.ModelSerializer):
    subgroup_url = serializers.HyperlinkedIdentityField(
        view_name="api:subgroup_indicators",
        lookup_field='gid'
    )

    class Meta:
        model = models.Grouping
        fields = ('gid', 'name', 'subgroup_url')


class GroupingSerializer(serializers.ModelSerializer):
    subgroup_link = serializers.HyperlinkedIdentityField(
        view_name='api:sub_group',
        lookup_field='gid')
    grouping_set = SubGroupingSerializer(many=True, read_only=True)

    class Meta:
        model = models.Grouping
        fields = ('gid', 'name', 'subgroup_link', 'grouping_set')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.HyperlinkedIdentityField(
        view_name='api:category_description',
        lookup_field='gcid')

    class Meta:
        model = models.Govcat
        fields = ('gcid', 'description', 'link')


class GovernmentMandateSerializer(serializers.ModelSerializer):
    year = serializers.StringRelatedField(source='yearid')
    indicator = serializers.StringRelatedField(source='iid')

    class Meta:
        model = models.Govindicator
        fields = ('value', 'year', 'indicator')


class GovernmentDetailSerializer(serializers.ModelSerializer):
    government_url = serializers.HyperlinkedIdentityField(
        view_name='api:government_detail',
        lookup_field='govid')
    indicator_rank_url = serializers.HyperlinkedIdentityField(
        view_name='api:rankings_indicator',
        lookup_field='govid')
    government_rank_url = serializers.HyperlinkedIdentityField(
        view_name='api:rankings_government',
        lookup_field='govid'
    )

    class Meta:
        model = models.Gov
        fields = ('govid', 'name', 'code', 'mdbcode', 'government_url',
                  'indicator_rank_url', 'government_rank_url')


class CategoryDescriptionSerializer(serializers.ModelSerializer):
    """
    Show details about a specific category with relations
    """
    gov_set = GovernmentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = models.Govcat
        fields = ('gcid', 'description', 'gov_set',)


class CategoryOverallRankingSerializer(serializers.ModelSerializer):
    government = serializers.StringRelatedField(source='govid')
    idp_score = serializers.StringRelatedField(source='idpscore')
    service_del_score = serializers.StringRelatedField(
        source='servicedelscore')
    finance_score = serializers.StringRelatedField(source='financescore')
    hr_score = serializers.StringRelatedField(source='hrscore')
    combined_score = serializers.StringRelatedField(source='combinedscore')
    gov_score = serializers.StringRelatedField(source='govscore')
    year = serializers.StringRelatedField(source='yearid')

    class Meta:
        model = models.Govrank
        fields = ('government', 'ranking', 'idp_score',
                  'service_del_score', 'finance_score',
                  'hr_score', 'gov_score',
                  'combined_score', 'year')

    def to_representation(self, instance):
        quintile = quintiles.calculate(instance)
        group = {}
        group['government'] = instance.govid.name
        group['data'] = {
            'idp_score': instance.idpscore,
            'idp_quintile': quintile['idp_score'],
            'service_del_score': instance.servicedelscore,
            'service_del_quintile': quintile['service_del_score'],
            'finance_score': instance.financescore,
            'finance_quintile': quintile['finance_score'],
            'hr_score': instance.hrscore,
            'hr_quintile': quintile['hr_score'],
            'combined_score': instance.combinedscore,
            'gov_score': instance.govscore,
            'year': instance.yearid.yr,
            }
        return group


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
        model = models.Govrank
        fields = ('ranking', 'idp_score', 'service_del_score', 'finance_score',
                  'hr_score', 'gov_score', 'combined_score', 'year')

    def to_representation(self, instance):
        quintile = quintiles.calculate(instance)
        group = {}
        group['ranking'] = instance.ranking
        group['data'] = {
            'idp_score': instance.idpscore,
            'idp_quintile': quintile['idp_score'],
            'service_del_score': instance.servicedelscore,
            'service_del_quintile': quintile['service_del_score'],
            'finance_score': instance.financescore,
            'finance_quintile': quintile['finance_score'],
            'hr_score': instance.hrscore,
            'hr_quintile': quintile['hr_score'],
            'combined_score': instance.combinedscore,
            'gov_score': instance.govscore,
            'year': instance.yearid.yr,
            }
        return group

class GovernmentIndicatorSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='iid')
    year = serializers.StringRelatedField(source='yearid')
    unit = serializers.StringRelatedField(source='iid.unitid.unit')
    short_name = serializers.StringRelatedField(source='iid.short_name')

    class Meta:
        model = models.Govindicator
        fields = ('value', 'name', 'year', 'unit', 'short_name')


class CategoryIndicatorListSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        gov_name_group = set([gov_name.govid.name for gov_name in instance])
        government_list = []
        for gov_name in gov_name_group:
            print(gov_name)
            groups = {}
            indicator_results = []
            for obj in instance:
                if obj.govid.name == gov_name:
                    indicator_results.append(
                        {
                            'Ranking': obj.ranking,
                            'Score': obj.score,
                            'Indicator': obj.iid.name,
                            'Short_Name': obj.iid.short_name
                        }
                    )
            groups['government'] = gov_name
            groups['data'] = indicator_results
            government_list.append(groups)
        return government_list


class CategoryIndicatorRankSerializer(serializers.ModelSerializer):
    government = serializers.StringRelatedField(source='govid')
    indicator = serializers.StringRelatedField(source='iid')
    year = serializers.StringRelatedField(source='yearid')

    class Meta:
        list_serializer_class = CategoryIndicatorListSerializer
        model = models.Govindicatorrank
        fields = ('government', 'indicator', 'ranking', 'score', 'year')


class IndicatorRankSerializer(serializers.ModelSerializer):
    indicator = serializers.StringRelatedField(source='iid')
    year = serializers.StringRelatedField(source='yearid')

    class Meta:
        model = models.Govindicatorrank
        fields = ('iid', 'indicator', 'ranking', 'score', 'year')

    def to_representation(self, instance):
        group = {}
        group['Mandate'] = instance.iid.mgid.name
        group['id'] = instance.iid.iid
        group['indicator'] = instance.iid.name
        group['data'] = {
            'ranking': instance.ranking,
            'score': instance.score,
            'year': instance.yearid.yr
        }
        return group


class IndicatorSerializer(serializers.ModelSerializer):
    unit = serializers.StringRelatedField(source='unitid')
    group = serializers.StringRelatedField(source='parentgid')

    class Meta:
        model = models.Indicator
        fields = ('name', 'code', 'group', 'unit', 'short_name')


class IndicatorListSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        gov_group = set([x.iid.parentgid.name for x in instance])
        indicator_list = []
        for group in gov_group:
            indicator_group = {}
            indicator_results = []
            for indi in instance:
                if indi.iid.parentgid.name == group:
                    indicator_results.append(
                        {
                            'name': indi.iid.name,
                            'value': indi.value,
                            'short_name': indi.iid.short_name
                        }
                    )
            indicator_group = {
                'name': group.rstrip(),
                'data': indicator_results
            }
            indicator_list.append(indicator_group)

        return indicator_list


class IndicatorValueSerializer(serializers.Serializer):
    name = serializers.StringRelatedField(source='iid.name')
    short_name = serializers.StringRelatedField(source='iid.short_name')

    class Meta:
        list_serializer_class = IndicatorListSerializer
        model = models.Govindicator
        fields = ('value', 'name', 'group', 'short_name')


class MandateGroupSerializer(serializers.ModelSerializer):
    indicator_link = serializers.HyperlinkedIdentityField(
        view_name='api:mandate_detail',
        lookup_field='mgid')
    indicator_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Mandategroup
        fields = ('mgid', 'name', 'indicator_link', 'indicator_set')


class MandateDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Indicator
        fields = ('iid', 'name', 'code', 'scale', 'short_name')

    def to_representation(self, instance):
        group = {}
        group['name'] = instance.name
        group['data'] = {
            'iid': instance.iid,
            'code': instance.code,
            'scale': instance.scale,
            'short_name': instance.short_name
        }
        return group


class YearSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Yearref
        fields = ('yearid', 'yr')
