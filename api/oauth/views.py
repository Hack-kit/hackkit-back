import json

from django.db.models import Q

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.oauth.models import OAuth
from api.oauth.serializer import OAuthValidateSerializer, OAuthSerializer


class OAuthValidateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OAuthValidateSerializer

    # def post(self, request, *args, **kwargs):
    #     data = json.loads(request.body)
    #
    #     try:
    #         OAuth.objects.get(
    #             type='Google',          # oauth_provider
    #             token=data['googleId']       # oauth_id
    #         )
    #     except OAuth.DoesNotExist:
    #         pass
    #
    #     auth_serializer = self.serializer_class(data=data)
    #     auth_serializer.is_valid(raise_exception=True)
    #     auth_data = auth_serializer.data

    pass