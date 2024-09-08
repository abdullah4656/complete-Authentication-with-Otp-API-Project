from django.urls import path
from account import views
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
       path('profile/', views.UserProfileView.as_view(), name='profile'),
       path('changepass/',views.ChangePasswordView.as_view()),
          path('reset/',views.SendEmailReset.as_view()),
          path('resetpass/<uid>/<token>/',views.Userpasswordreset().as_view()),
                    path('otp/',views.otp.as_view()),
                    path('verify/',views.OtpVerificationView.as_view())
]

