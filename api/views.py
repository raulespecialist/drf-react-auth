from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import login
import pyotp
import qrcode
from io import BytesIO
import base64
from .serializers import VerifyOTPSerializer

# Vista para el registro de usuarios
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Vista para el inicio de sesión
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        # Verificar si el usuario tiene un totp_secret configurado
        if hasattr(user, 'profile') and user.profile.totp_secret:
            # Si tiene totp_secret, redirigir a la página de verificación de OTP
            return Response({
                "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
                "redirect_to": "verify-otp"  # Indicar a React que redirija a /verify-otp
            }, status=status.HTTP_200_OK)
        else:
            # Si no tiene totp_secret, redirigir a la página de configuración del QR
            return Response({
                "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
                "redirect_to": "qr"  # Indicar a React que redirija a /qr
            }, status=status.HTTP_200_OK)

# Vista para generar el QR de Google Authenticator
class GenerateQRAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        secret = pyotp.random_base32()
        user.profile.totp_secret = secret  # Guardar el secreto en el perfil del usuario
        user.profile.save()

        # Generar la URL para Google Authenticator
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(user.email, issuer_name="MyApp")

        # Generar el código QR
        img = qrcode.make(totp_uri)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return Response({"qr_code": img_str})


# Vista para Verificar el OTP
class VerifyOTPAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        otp = serializer.validated_data['otp']

        # Verificar si el usuario tiene un perfil y un secreto OTP configurado
        if not hasattr(user, 'profile') or not user.profile.totp_secret:
            return Response(
                {"error": "Google Authenticator no está configurado para este usuario."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Depuración: Imprimir el secreto y el código OTP actual
        print("Secreto OTP:", user.profile.totp_secret)
        totp = pyotp.TOTP(user.profile.totp_secret)
        print("Código OTP actual:", totp.now())
        print("Código OTP recibido:", otp)

        # Verificar el código OTP
        if totp.verify(otp, valid_window=1):  # Permite un margen de ±30 segundos
            return Response({"message": "Código OTP válido."}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Código OTP inválido o expirado."},
                status=status.HTTP_400_BAD_REQUEST
            )