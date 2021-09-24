from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class StoreView(generics.ListAPIView):
    pass


class FoodView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    # GET, POST, PUT
    pass


class OrderView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    pass
