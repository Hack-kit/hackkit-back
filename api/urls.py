from django.urls import include, path


urlpatterns = [
    path('oauth/', include('api.oauth.urls')),
    path('users/', include('api.users.urls')),
    path('stores/', include('api.stores.urls')),
]
