from django.test import TestCase
from users.models import CustomUser


class LoginTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            telegram_id=777777,
            password='some_Password777')

    def tearDown(self):
        self.user.delete()

    def test_correct_login(self):
        response = self.client.post(
            path='/auth/token/login/',
            data={'telegram_id': 777777, 'password': 'some_Password777'})
        self.assertTrue(response.status_code == 200 and
                        response.data.get('auth_token'))
