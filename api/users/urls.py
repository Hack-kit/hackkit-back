from django.urls import path

from api.users.views import *

app_name = 'users'
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('<int:pk>', MyPageView.as_view(), name='mypage'),
    path('<int:pk>/edit', MyPageView.as_view(), name='mypage_edit'),

    path('review/create', ReviewView.as_view(), name='review'),
    path('review/<int:pk>/edit', ReviewView.as_view(), name='review_edit'),
]