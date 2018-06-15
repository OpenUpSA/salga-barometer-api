from rest_framework import serializers

from api import models


class GovernmentDetailSerializer(serializers.ModelSerializer):
    government_url = serializers.HyperlinkedIdentityField(
        view_name='api:governments:detail',
        lookup_field='govid')
    indicator_rank_url = serializers.HyperlinkedIdentityField(
        view_name='api:rankings:indicator',
        lookup_field='govid')
    government_rank_url = serializers.HyperlinkedIdentityField(
        view_name='api:rankings:government',
        lookup_field='govid'
    )

    class Meta:
        model = models.Gov
        fields = ('govid', 'name', 'code', 'mdbcode', 'government_url',
                  'indicator_rank_url', 'government_rank_url')


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
