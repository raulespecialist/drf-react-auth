from django.test import TestCase
from api.serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User

# Test serializer Register
class RegisterSerializerTest(TestCase):
    def test_register_serializer(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')

# Test serializer Login
class LoginSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_login_serializer(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.validate(data)
        self.assertEqual(user, self.user)