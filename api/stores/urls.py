from django.urls import path

from api.stores.views import *

app_name = 'stores'
urlpatterns = [
    # owner_side
    path('', StoreView.as_view(), name='store'),
    path('food/create', FoodView.as_view(), name='food_create'),  # POST
    path('food/<int:pk>/edit', FoodView.as_view(), name='food_edit'),
    path('food/<int:pk>/delete', FoodView.as_view(), name='food_edit'),

    # customer_side
    path('food', FoodListView.as_view(), name='food'),
    path('order', OrderView.as_view(), name='order_list'),
    path('order/create', OrderView.as_view(), name='order'),
    path('order/<int:pk>/edit', OrderView.as_view(), name='order_edit'),
]