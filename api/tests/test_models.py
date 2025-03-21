from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Profile

class ProfileModelTest(TestCase):
    def setUp(self):
        # Crear un usuario para las pruebas
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_profile_creation(self):
        # Verificar que se crea un perfil automáticamente al crear un usuario
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsNotNone(self.user.profile.totp_secret)