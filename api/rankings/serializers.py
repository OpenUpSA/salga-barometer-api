from rest_framework import serializers

from api import quintiles
from core import models


class CategoryIndicatorListSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        gov_name_group = set([gov_name.govid.name for gov_name in instance])
        government_list = []
        for gov_name in gov_name_group:
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
    government = serializers.StringRelatedField(source='govid.name')

    class Meta:
        model = models.Govindicatorrank
        fields = ('iid', 'indicator', 'ranking', 'score', 'year')

    def to_representation(self, instance):
        govid = self.context.get('govid')
        try:
            value = models.Govindicator\
                          .objects\
                          .get(iid=instance.iid,
                               yearid=instance.yearid,
                               govid=govid).value
        except models.Govindicator.DoesNotExist:
            value = ''
        group = {}
        group['mandate'] = instance.iid.mgid.name
        group['government'] = instance.govid.name
        group['id'] = instance.iid.iid
        group['indicator'] = instance.iid.name
        group['data'] = {
            'ranking': instance.ranking,
            'score': instance.score,
            'value': value,
            'year': instance.yearid.yr
        }
        return group


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
        ranking_total = self.context.get('ranking_total')
        quintile = quintiles.calculate(instance, ranking_total)
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
        ranking_total = self.context.get('ranking_total')
        quintile = quintiles.calculate(instance, ranking_total)
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
