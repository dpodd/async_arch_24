from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session
from django.conf import settings
from django.contrib.auth import login

from users.models import User


def callback(request):
    state = request.GET.get('state')

    oauth = OAuth2Session(
        client_id=settings.OAUTH_CLIENT_ID,
        redirect_uri=settings.OAUTH_REDIRECT_URL,
        state=state
    )

    oauth.fetch_token(
        settings.OAUTH_TOKEN_URL,
        client_secret=settings.OAUTH_SECRET_KEY,
        code=request.GET.get('code'),
    )

    # Use the token to fetch the user's information from the auth service
    user_info = oauth.get(
        settings.OAUTH_USERINFO_URL
    ).json()

    # Find or create the local user based on the public_id
    try:
        user = User.objects.get(
            public_id=user_info['public_id']
        )
        user.email = user_info['email']
        user.first_name = user_info['first_name']
        user.last_name = user_info['last_name']
        user.role = user_info['role']
        user.save()
    except User.DoesNotExist:
        user = User.objects.create(
            public_id=user_info['public_id'],
            first_name=user_info['first_name'],
            last_name=user_info['last_name'],
            email=user_info['email'],
            role=user_info['role']
        )

    user = authenticate(request, public_id=user_info['public_id'])
    if not user:
        return HttpResponse("Unauthorized", status=401)

    login(request, user)
    request.session['user_public_id'] = str(user.public_id)

    next_path = request.session.pop('oauth_next', 'home')
    return redirect(next_path)
