from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views #so that we don't confuse with our own views (allows us to use LoginView and LogoutView)
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('stylist_signup/', views.StylistSignUp.as_view(), name = 'stylist_signup'),
    path('client_signup/', views.ClientSignUp.as_view(), name = 'client_signup'),
    path('user_delete//<int:pk>/', views.UserDeleteView.as_view(), name = 'user_delete'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html", success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html", success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name='password_reset_complete'),


]

# 1. Submit email form                         -> PasswordResetView.as_view()
# 2. Email sent success message               -> PasswordResetDoneView.as_view(password_reset_done)
# 3. Link to password reset form in mail      -> PasswordResetConfirmView.as_view()
# 4. Password successfully changed message      -> PasswordResetCompleteView.as_view()
