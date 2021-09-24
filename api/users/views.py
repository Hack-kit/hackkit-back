from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class LoginView(generics.CreateAPIView):
    # POST
    pass


class SignUpView(generics.CreateAPIView):
    # POST
    pass


class MyPageView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    # GET, PUT
    pass


class ReviewView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    # GET, PUT
    pass
