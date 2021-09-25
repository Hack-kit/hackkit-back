import json

from django.db import transaction
from django.forms import model_to_dict
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.oauth.models import OAuth
from apps.users.models import User, Review, Address
from api.users.serializer import UserSerializer, ReviewSerializer, LoginSerializer, SignUpSerializer
from api.users.services import AddressService


class LoginView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        user = self.serializer_class.get_user(request=request)
        if user:
            response = {
                'user': UserSerializer(instance=user).data,
                'token': self.serializer_class.get_token(user=user)
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data)
        with transaction.atomic():
            auth = OAuth.objects.create(
                type=OAuth.OAUTH_CHOICES.Google,
                token=data['google_id']
            )
            print(auth)
            address_service = AddressService()
            lat, long = address_service.get_address_point(text=data['address']['text'])
            print(lat)
            print(long)
            address = Address.objects.create(
                name=data['nickname'],
                text=data['address']['text'],
                lat=lat,
                long=long
            )
            user = User.objects.create(
                oauth=auth,
                email=data['email'],
                phone=data['number'],
                address=address,
                user_type=data['user_type']
            )
            user.save()
            print(user)
            response = {
                'pk': user.pk,
                'user': UserSerializer(instance=user).data,
                'token': LoginSerializer.get_token(user=user)
            }
            print(response)
            return Response(response, status=status.HTTP_201_CREATED)


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

