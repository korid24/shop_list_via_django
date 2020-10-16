from django.test import TestCase
from users.models import CustomUser
from api.utils.mixins import BaseViewTest


class LoginTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            telegram_id=777777,
            password='some_Password777')

    def tearDown(self):
        self.user.delete()

    def test_user_can_take_token(self):
        """
        Пользователь может получить токен по логину и паролю
        """
        response = self.client.post(
            path='/auth/token/login/',
            data={'telegram_id': 777777, 'password': 'some_Password777'})
        self.assertTrue(response.status_code == 200 and
                        response.data.get('auth_token'))


class CommonUserViewTest(BaseViewTest):
    bot = False

    def test_user_must_be_authenticated(self):
        for path in self.get_request_urls().values():
            response = self.not_authorized_client.get(path)
            self.assertEqual(401, response.status_code)


class BotVewTest(BaseViewTest):
    bot = True

    def test_only_bot_can_see_bots_urls(self):
        for path in self.get_request_urls().values():
            response1 = self.not_authorized_client.get(path)
            response2 = self.common_user_client.get(path)
            self.assertEqual(401, response1.status_code)
            self.assertEqual(403, response2.status_code)
