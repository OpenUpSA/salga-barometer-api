from rest_framework import serializers

from core import models


class SubGroupingSerializer(serializers.ModelSerializer):
    subgroup_url = serializers.HyperlinkedIdentityField(
        view_name="api:groupings:subgroup_indicators",
        lookup_field='gid'
    )

    class Meta:
        model = models.Grouping
        fields = ('gid', 'name', 'subgroup_url')


class GroupingSerializer(serializers.ModelSerializer):
    subgroup_link = serializers.HyperlinkedIdentityField(
        view_name='api:groupings:subgroup',
        lookup_field='gid')
    grouping_set = SubGroupingSerializer(many=True, read_only=True)

    class Meta:
        model = models.Grouping
        fields = ('gid', 'name', 'subgroup_link', 'grouping_set')
