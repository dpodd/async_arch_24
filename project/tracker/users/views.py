from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse


def logout_view(request):
    request.session.flush()

    # URL of the auth service login page
    auth_service_login_url = settings.LOGOUT_URL

    return redirect(auth_service_login_url)
