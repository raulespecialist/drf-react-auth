from django.urls import path
from knox.views import LogoutView
from .views import RegisterAPI, LoginAPI, GenerateQRAPI, VerifyOTPAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Endpoint de cierre de sesión
    path('generate-qr/', GenerateQRAPI.as_view(), name='generate-qr'),
    path('verify-otp/', VerifyOTPAPI.as_view(), name='verify-otp'),
]