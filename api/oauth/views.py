from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class OAuthView(generics.CreateAPIView):
    pass
