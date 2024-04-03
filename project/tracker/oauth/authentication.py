# from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from requests_oauthlib import OAuth2Session

from users.models import User


def oauth2_authentication_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        # Check if the user is already authenticated in the session
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        request.session['oauth_next'] = request.get_full_path()

        # Start OAuth2 flow if the user is not authenticated
        oauth = OAuth2Session(
            client_id=settings.OAUTH_CLIENT_ID,
            redirect_uri=settings.OAUTH_REDIRECT_URL
        )
        authorization_url, state = oauth.authorization_url(settings.OAUTH_AUTHORIZATION_URL)

        return redirect(authorization_url)

    return _wrapped_view_func
