import json

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.oauth.models import OAuth
from api.oauth.serializer import OAuthValidateSerializer
from api.users.serializer import LoginSerializer, UserSerializer


class OAuthValidateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OAuthValidateSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        try:
            oauth = OAuth.objects.get(
                type='Google',          # oauth_provider
                token=data['google_id']       # oauth_id
            )
            user = LoginSerializer.get_auth_user(obj=oauth)
            if user:
                token = LoginSerializer.get_token(user=user)
                return Response(token, status=status.HTTP_406_NOT_ACCEPTABLE)
        except OAuth.DoesNotExist:
            return Response(data, status=status.HTTP_200_OK)
