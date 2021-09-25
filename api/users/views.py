import json

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.users.models import User, Review
from api.users.serializer import UserSerializer, ReviewSerializer


class LoginView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        pass


class SignUpView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        pass


class MyPageView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    # GET, PUT
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    lookup_field = 'pk'
    queryset = User.objects.all()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = self.get_object()

    def get(self, request, *args, **kwargs):
        return self.user

    def put(self, request, *args, **kwargs):
        return self.user


class ReviewView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    # GET, PUT
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer
    lookup_field = 'pk'
    queryset = Review.objects.all()

    def __init__(self):
        super(ReviewView, self).__init__()
        self.review = self.get_object()

    def get(self, request, *args, **kwargs):
        # self.review
        review_list = self.serializer_class(
            instance=Review.objects.filter(user=request.user),
            many=True
        ).data
        return Response(review_list, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        review = Review(
            customer=request.user,
            rate=data['rate'],
            content=data['content']
        )
        review_serializer = self.serializer_class(instance=review)
        review_serializer.is_valid(raise_exception=True)
        obj, pk = review_serializer.save()
        response = {
            'pk': pk,
            'review': review_serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)

