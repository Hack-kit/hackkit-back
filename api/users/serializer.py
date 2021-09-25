import typing

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from apps.oauth.models import OAuth
from apps.users.models import User, Review, Address

from phonenumber_field.modelfields import PhoneNumberField


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['text']


class LoginSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    auth_user = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    @staticmethod
    def get_user(request: Request) -> typing.Optional[User]:
        jwt_auth = JWTAuthentication()
        user, validated_token = jwt_auth.authenticate(request=request)
        if user is None:
            raise serializers.ValidationError('invalid login credentials')
        return user

    @staticmethod
    def get_auth_user(obj: OAuth):
        try:
            return User.objects.get(oauth_id=obj.id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_token(user: User) -> typing.Optional[dict]:
        refresh = RefreshToken.for_user(user)
        token = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
        return token


class SignUpSerializer(serializers.Serializer):
    google_id = serializers.CharField(read_only=True)
    user_type = serializers.ChoiceField(choices=User.USER_CHOICES)
    email = serializers.EmailField()
    nickname = serializers.CharField()
    address = AddressSerializer(read_only=False, partial=True)
    number = PhoneNumberField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['oauth', 'email', 'phone', 'address','user_type']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
