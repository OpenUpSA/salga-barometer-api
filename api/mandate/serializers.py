from rest_framework import serializers

from core import models


class MandateGroupSerializer(serializers.ModelSerializer):
    indicator_link = serializers.HyperlinkedIdentityField(
        view_name='api:mandate:detail',
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
