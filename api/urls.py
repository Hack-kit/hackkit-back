from django.urls import include, path


urlpatterns = [
    path('users/', include('api.oauth.urls')),
    path('oauth/', include('api.users.urls')),
    path('programs/', include('api.stores.urls')),
]
