from rest_framework import serializers


from core import models


class YearSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Yearref
        fields = ('yearid', 'yr')
