from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Profile
from knox.models import AuthToken
import pyotp

# Test for view RegisterAPI
class RegisterAPITest(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

# Test for view LoginAPI
class LoginAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_login_user(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

# Test for view GenerateQRAPI
class GenerateQRAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_generate_qr(self):
        url = reverse('generate-qr')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('qr_code', response.data)
        self.assertIsNotNone(self.user.profile.totp_secret)

# Test for view VerifyOTPAPI
class VerifyOTPAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = Profile.objects.create(user=self.user, totp_secret=pyotp.random_base32())
        self.client.force_authenticate(user=self.user)

    def test_verify_otp(self):
        url = reverse('verify-otp')
        totp = pyotp.TOTP(self.profile.totp_secret)
        data = {
            'otp': totp.now()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Código OTP válido.')

# Test for view LogoutAPI
class LogoutAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = AuthToken.objects.create(self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_logout_user(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(AuthToken.objects.filter(user=self.user).exists())