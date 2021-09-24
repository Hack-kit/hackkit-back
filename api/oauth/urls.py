from django.urls import path

from api.oauth.views import *

app_name = 'oauth'
urlpatterns = [
    path('validate', OAuthView.as_view(), name='oauth_validate'),
]