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


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.HyperlinkedIdentityField(
        view_name='api:categories:description',
        lookup_field='gcid')

    class Meta:
        model = models.Govcat
        fields = ('gcid', 'description', 'link')


class CategoryDescriptionSerializer(serializers.ModelSerializer):
    """
    Show details about a specific category with relations
    """
    gov_set = GovernmentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = models.Govcat
        fields = ('gcid', 'description', 'gov_set',)
