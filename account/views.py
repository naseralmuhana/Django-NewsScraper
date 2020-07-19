from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm

from account import forms as account_forms


class SignUpView(SuccessMessageMixin, CreateView):

    form_class = account_forms.SignUpForm
    success_url = reverse_lazy('account:register')
    success_message = 'Sign Up successfully, you can login now.'
    template_name = 'account/register_login.html'


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('main:home')
        else:
            messages.warning(request, 'Invalid login or password.')

    return redirect('account:register')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your Password has been changed successfully.')
            return redirect('account:register')
        else:
            messages.warning(request, 'Check your data, something goes wrong.')
    form = PasswordChangeForm(user=request.user)
    context = {
        'form': form,
    }
    return render(request, 'account/change-password.html', context)
