from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from api.oauth.views import *

app_name = 'oauth'
urlpatterns = [
    path('validate', OAuthValidateView.as_view(), name='oauth_validate'),
    path('token/obtain', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh')
]