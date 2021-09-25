import typing
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.oauth.models import OAuth


class OAuthValidateSerializer(serializers.Serializer):
    pass


class OAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = OAuth
        fields = '__all__'
