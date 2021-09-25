import json

from django.forms import model_to_dict
from rest_framework import generics, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

from apps.users.models import User
from api.users.serializer import LoginSerializer
from apps.stores.models import Food, Order, Store
from api.stores.serializer import FoodSerializer, OrderSerializer, StoreSerializer, OrderModelSerializer


class StoreView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StoreSerializer
    queryset = Store.objects.all().prefetch_related('food_set')
    lookup_field = 'pk'
    lookup_url_kwarg = lookup_field

    def get(self, request, *args, **kwargs):
        user = LoginSerializer.get_user(request=request)
        user_type = User.objects.get(id=user.id).user_type
        if user_type == User.USER_CHOICES.owner:
            store = self.queryset.get(owner=user)
            food_set = FoodSerializer(instance=store.food_set.all(), many=True).data
            # print(FoodSerializer(instance=food_set, many=True).data)
            response = {
                'store_food_set': json.loads(JSONRenderer().render(data=food_set))
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'고객 객체에서는 가게를 조회할 수 없습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


class FoodView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    # GET, POST, PUT
    permission_classes = (IsAuthenticated,)
    serializer_class = FoodSerializer
    lookup_field = 'pk'
    queryset = Food.objects.all()

    # 사진 넣는 부분 해결할것!
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        food_serializer = self.serializer_class(data=data)
        food_serializer.is_valid(raise_exception=True)
        food = food_serializer.save()
        response = {
            'pk': food.pk,
            'food': food_serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        # 상세정보만 수정가능
        user = LoginSerializer.get_user(request=request)
        data = json.loads(request.body)

        try:
            food = self.queryset.get(store__owner=user, pk=self.kwargs[self.lookup_field])
        except Food.DoesNotExist:
            return Response({'음식 객체가 존재하지 않습니다'}, status=status.HTTP_404_NOT_FOUND)

        food_serializer = self.serializer_class(data=data, partial=True)
        food_serializer.is_valid(raise_exception=True)
        food.description = data['description']
        food.save(update_fields=['description'])

        response = {
            'food': model_to_dict(food, fields=['pk', 'name', 'category', 'description', 'quantity'])
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user = LoginSerializer.get_user(request=request)
        try:
            food = self.queryset.get(store__owner=user, pk=self.kwargs[self.lookup_field])
        except Food.DoesNotExist:
            return Response({'음식 객체가 존재하지 않습니다'}, status=status.HTTP_404_NOT_FOUND)

        food_pk, obj = food.delete()
        response = {
            'food_pk': food_pk
        }
        return Response(response, status=status.HTTP_200_OK)


class FoodListView(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        # 하나의 food만 보여줄 것인가, food의 list를 보여줄 것인가?
        user = LoginSerializer.get_user(request=request)
        # 범위 필터링을 어떻게 하지????
        return Response(None, status=status.HTTP_200_OK)


class OrderView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    # request.body = { customer_pk, food_pk, quantity }
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        user = LoginSerializer.get_user(request=request)
        order_list = OrderModelSerializer(
            instance=self.queryset.filter(user=request.user),
            partial=True,
            many=True
        ).data
        return Response(order_list, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        # 존재하는 food 객체인지 확인
        food = self.serializer_class.get_food(pk=data['food_pk'])
        if self.serializer_class.get_valid_order(obj=food, order_quantity=data['quantity']) is not True:
            raise ValidationError('invalid quantity')

        order = Order(
            user=request.user,
            food=food,
            quantity=data['quantity']
        )

        order_serializer = self.serializer_class(instance=order)
        order_serializer.is_valid(raise_exception=True)
        print(order_serializer.data)

        obj, pk = order_serializer.save()
        response = {
            'pk': pk,
            'order': order_serializer.data
        }

        return Response(response, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        data = json.loads(request.body)

        food = self.serializer_class.get_food(pk=data['food_pk'])
        if self.serializer_class.get_valid_order(obj=food, order_quantity=data['quantity']) is not True:
            raise ValidationError('invalid quantity')

        try:
            order = Order.objects.get(
                user=request.user,
                food=food
            )
        except Order.DoesNotExist:
            raise ValidationError('order does not exists')

        order.quantity = data['quantity']
        order.save()

        response = {
            'pk': order.pk,
            'order': self.serializer_class(instance=order).data
        }
        return Response(response, status=status.HTTP_201_CREATED)
