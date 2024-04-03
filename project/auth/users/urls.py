from django.urls import path
from django.contrib.auth.views import LoginView

from .views import (
    SignUpView, ProfileView, LogoutView, logout_confirmation, UsersListView, UserEditView,
    UserDeleteView)


urlpatterns = [
    path('', UsersListView.as_view(), name='user_list'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/confirm/', logout_confirmation, name='logout_confirm'),
    path('users/<int:pk>/edit/', UserEditView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),


    # path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]