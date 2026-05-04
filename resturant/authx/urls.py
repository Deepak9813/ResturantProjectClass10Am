from django.urls import path

from .views import loginPage, registerPage, logout_function, changePassword, resetPasswordEmailSend, verifyOtp, resetPassword, profilePage, editProfile

urlpatterns = [
    path("login/", loginPage, name="login"),
    path("register/", registerPage, name="register"),
    path("logout/", logout_function, name="logout"),
    path("change-password/", changePassword, name="change_password"),
    path("reset-password-email-send/", resetPasswordEmailSend, name="reset_password_email_send"),
    path("verify-otp/", verifyOtp, name="verify_otp"),
    path("reset-password/", resetPassword, name="reset_password"),
    path('profile/', profilePage, name='profile_page'),
    path('edit-profile/', editProfile, name='edit_profile'),
    
]
