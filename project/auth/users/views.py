from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LogoutView as _LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, UserProfileForm
from .models import User


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class ProfileView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.request.user.role
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Changes saved.')
        return super().form_valid(form)


class LogoutView(_LogoutView):
    next_page = reverse_lazy('login')


@login_required
def logout_confirmation(request):
    return render(request, 'users/logout_confirmation.html')


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/home.html'
    context_object_name = 'users'
    paginate_by = 10
    ordering = '-date_joined'

    def get_queryset(self):
        return User.objects.all().order_by(self.ordering)


class UserEditView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('user_list')

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.request.user.role
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Changes saved.')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, View):
    template_name = 'users/user_delete_confirm.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'user_id': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        user_to_delete = get_object_or_404(User, pk=self.kwargs['pk'])
        if request.user == user_to_delete:
            messages.error(request, "You cannot delete your own account while logged in.")
            return redirect('user_list')

        user_to_delete.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('user_list')