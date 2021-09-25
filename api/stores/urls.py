from django.urls import path

from api.stores.views import *

app_name = 'stores'
urlpatterns = [
    path('', StoreView.as_view(), name='store'),
    path('food', FoodView.as_view(), name='food'),
    path('food/create', FoodView.as_view(), name='food_create'),          # POST
    path('food/<int:pk>/edit', FoodView.as_view(), name='food_edit'),

    path('order/create', OrderView.as_view(), name='order'),
    path('order/<int:pk>/edit', OrderView.as_view(), name='order_edit'),
]