from django.urls import path
from . import views, allauth_views
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordChangeView


urlpatterns = [
    #path("post/<int:num>/delcom/id<int:id>/", views.del_comm, name="delcom"),
    path("register/", views.UserRegister.as_view(), name="user_register"),
    path("user=<user_id>/profile/", views.UserProfile.as_view(), name="current_user_profile"),
    path("user=<user_id>/profile/edit", views.EditUserProfile.as_view(), name="edit_current_user_profile"),
    path("out/", views.Logout.as_view(), name="out"),
    path("login/", views.Sign_in.as_view(), name="sign_in"),
    path("activate/<u_id>/<slug:token>", views.activate_user, name="activation"),
    #password reset views
    path("password_change/", views.PasswordChangeView2.as_view(), name="password_change"),
    path("password_reset/", views.PasswordResetView2.as_view(), name="reset_password"),
    path("password_reset_confirm/<uidb64>/<token>/", views.PasswordResetConfirmView2.as_view(), name="password_reset_confirmation"),
    path("password_reset_done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    #custom allauth
    path("sign-in/", allauth_views.CustomLoginView.as_view(), name="custom_login"),
    path("user=<int:user_id>/set-password/", allauth_views.SetPasswordView.as_view(), name="set_password"),
    path("delete/user=<int:user_id>/<provider>/", allauth_views.DeleteSocialAccount.as_view(), name="delete_social"),


    #path('', views.index, name='index'),
]
