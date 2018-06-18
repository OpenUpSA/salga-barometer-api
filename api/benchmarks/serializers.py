from rest_framework import serializers

from core import models


class IndicatorRankSerializer(serializers.ModelSerializer):
    indicator = serializers.StringRelatedField(source='iid')
    year = serializers.StringRelatedField(source='yearid')
    government = serializers.StringRelatedField(source='govid.name')

    class Meta:
        model = models.Govindicatorrank
        fields = ('iid', 'indicator', 'ranking', 'score', 'year')

    def to_representation(self, instance):
        group = {}
        group['mandate'] = instance.iid.mgid.name
        group['government'] = instance.govid.name
        group['id'] = instance.iid.iid
        group['indicator'] = instance.iid.name
        group['data'] = {
            'ranking': instance.ranking,
            'score': instance.score,
            'year': instance.yearid.yr
        }
        return group


class BenchmarkMandateSerializer(serializers.ModelSerializer):
    govid = serializers.StringRelatedField(source='govid.name')

    class Meta:
        model = models.Govrank
        exclude = ('rankid', 'yearid', 'ranking')


class BenchmarkIndicatorSerializer(serializers.ModelSerializer):
    govid = serializers.StringRelatedField(source='govid.name')

    class Meta:
        model = models.Govindicatorrank
        fields = '__all__'
