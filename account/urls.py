from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
 

from account import views as account_views

app_name = 'account'

urlpatterns = [

    url(r'^register-login', account_views.SignUpView.as_view(), name="register"),
    url(r'^login', account_views.login_page, name='login'),
    url(r'^logout', auth_views.LogoutView.as_view(next_page='main:home'), name='logout'),
    url(r'^change-password', account_views.change_password, name='change_password'),
    url(r'^reset-password/preprocess',
         auth_views.PasswordResetView.as_view(
             template_name='account/password-reset/password_reset.html',
             email_template_name='account/password-reset/password_reset_email.html',
             success_url=reverse_lazy('account:password_reset_done')
         ),
         name='password_reset'),
    url(r'^reset-password/done',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password-reset/password_reset_confirm.html',
             success_url=reverse_lazy('account:password_reset_complete')
         ),
         name='password_reset_confirm'),
    url(r'^reset-password/complete',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
