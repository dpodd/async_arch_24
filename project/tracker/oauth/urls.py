from django.urls import path

from .callback_view import callback

urlpatterns = [
    path('oauth/callback/', callback, name='oauth_callback'),
]
