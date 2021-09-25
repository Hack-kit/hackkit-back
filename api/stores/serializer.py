import typing
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.stores.models import Food, Order
from api.users.serializer import UserSerializer


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=False)
    food = serializers.SerializerMethodField()
    valid_order = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['user', 'food', 'quantity']

    @staticmethod
    def get_food(pk: int) -> typing.Optional[Food]:
        # 존재하는 food 객체인지 확인
        try:
            return Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            raise ValidationError('food does not exists')

    @staticmethod
    def get_valid_order(obj: Food, order_quantity: int) -> typing.Optional[bool]:
        try:
            total_quantity = obj.quantity
        except AttributeError:
            return None

        if total_quantity - order_quantity < 0:
            return False
        else:
            return True
