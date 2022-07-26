from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name="register"),
    path('verify_otp', views.otp_verify, name="verify_otp"),
    path('login', views.login, name="login"),
]
