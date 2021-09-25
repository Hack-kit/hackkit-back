import typing
from rest_framework import serializers

from apps.oauth.models import OAuth


class OAuthValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OAuth
        fields = '__all__'
