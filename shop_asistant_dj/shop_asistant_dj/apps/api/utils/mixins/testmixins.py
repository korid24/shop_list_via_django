import json
from typing import Optional, Dict
from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from users.models import CustomUser
from purchase.models import Purchase, PurchasesList


class BaseViewTest(TestCase):
    """
    Класс, от которого наследуются классы проверки вьюсетов.
    В зависимости от типа пользователя формирует разные ссылки и предоставляет
    разные права. Представления покупок тестируются в меньшей степени,
    так как наследуются от одного классса со списками покупок и работают
    идентично, за исключением метода get_queryset
    """
    bot = False

    def _get_path_to_users(self, telegram_id: Optional[int] = None) -> str:
        """
        Путь до пользователя для бота
        """
        path: str = ''
        if self.bot:
            path = '/api/bot_user/'
            if telegram_id:
                path += str(telegram_id) + '/'
        return path

    def _get_path_to_lists(self, list_ind: Optional[int] = None) -> str:
        """
        Пути до списков покупок для бота и обычного пользователя
        """
        path: str
        if self.bot:
            path = 'bot_purchaselist/'
        else:
            path = 'purchaselist/'
        if list_ind:
            path += str(list_ind) + '/'
        return path

    def _get_path_to_purchases(self, pur_ind: Optional[int] = None) -> str:
        """
        Пути до покупок для бота и обычного пользователя
        """
        path: str
        if self.bot:
            path = 'bot_purchase/'
        else:
            path = 'purchase/'
        if pur_ind:
            path += str(pur_ind) + '/'
        return path

    @property
    def _current_client(self) -> Client:
        """
        Клиент с правами текущего пользователя
        """
        if self.bot:
            return self.bot_client
        return self.common_user_client

    def get_current_client(self) -> Client:
        return self._current_client

    @property
    def _request_urls(self) -> Dict[str, str]:
        """
        Словарь с адесами, предназначенными для текущего пользователя
        """
        d = {}
        d['path_to_users'] = self._get_path_to_users()
        d['path_to_user'] = self._get_path_to_users(123456)
        d['path_to_purchaselists'] = (d['path_to_user'] +
                                      self._get_path_to_lists())
        d['path_to_purchaselist'] = (d['path_to_user'] +
                                     self._get_path_to_lists(1))
        d['path_to_purchases'] = (d['path_to_purchaselist'] +
                                  self._get_path_to_purchases())
        d['path_to_purchase'] = (d['path_to_purchaselist'] +
                                 self._get_path_to_purchases(1))
        return d

    def get_request_urls(self) -> Dict[str, str]:
        return self._request_urls

    def setUp(self):
        """
        Перед выполнением тестов создается два обычных пользователя и бот,
        создаются списки и покупки для пользователей
        """
        # создание тестового обычного пользователя с токеном и клиентом
        self.common_user = CustomUser.objects.create_user(
            telegram_id=123456,
            password='good_password')
        self.common_user_token = Token.generate_key(1)
        Token.objects.create(user=self.common_user, key=self.common_user_token)
        self.common_user_client = Client(
            HTTP_AUTHORIZATION='Token {}'.format(self.common_user_token),
            HTTP_ACCEPT_LANGUAGE='en-US')

        # создание тестового обыного пользователя
        self.another_common_user = CustomUser.objects.create_user(
            telegram_id=666666,
            password='another_good_password')
        self.not_authorized_client = Client(HTTP_ACCEPT_LANGUAGE='en-US')

        # создание бота с токеном и клиентом
        self.bot = CustomUser.objects.create_user(
            telegram_id=777777,
            password='bot_password',
            is_bot=True)
        self.bot_token = Token.generate_key(1)
        Token.objects.create(user=self.bot, key=self.bot_token)
        self.bot_client = Client(
            HTTP_AUTHORIZATION='Token {}'.format(self.bot_token),
            HTTP_ACCEPT_LANGUAGE='en-US')

        # создание списков покупок
        self.common_user_products = PurchasesList.objects.create(
            author=self.common_user,
            title='products')
        self.common_user_birthday = PurchasesList.objects.create(
            author=self.common_user,
            title='birthday')
        self.common_user_car = PurchasesList.objects.create(
            author=self.common_user,
            title='car')
        self.another_user_list = PurchasesList.objects.create(
            author=self.another_common_user,
            title='some_list')

        # создание покупок
        self.cheese = Purchase.objects.create(
            purchase_list=self.common_user_products,
            title='chesee')
        self.milk = Purchase.objects.create(
            purchase_list=self.common_user_products,
            title='milk')
        self.bread = Purchase.objects.create(
            purchase_list=self.common_user_products,
            title='bread')
        self.cake = Purchase.objects.create(
            purchase_list=self.common_user_birthday,
            title='cake')
        self.another_purchase = Purchase.objects.create(
            purchase_list=self.another_user_list,
            title='another_purchase')

    def tearDown(self):
        """
        Удаление всего
        """
        for model in [CustomUser, PurchasesList, Purchase]:
            model.objects.all().delete()

    def test_can_go_to_all_urls(self):
        """
        Пользователь или бот может переходить по всем предназначенным
        для него адресам
        """
        for path in self._request_urls.values():
            response = self._current_client.get(path)
            self.assertEqual(200, response.status_code)

    def test_sees_user_lists(self):
        path = self._get_path_to_users(123456) + self._get_path_to_lists()
        response = self._current_client.get(path)
        self.assertEqual(3, len(response.data))
        self.assertEqual(4, PurchasesList.objects.count())

    def test_can_choose_list_by_ind(self):
        path = self._get_path_to_users(123456) + self._get_path_to_lists(1)
        response = self._current_client.get(path)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.data.get('ind'))
        self.assertEqual('products', response.data.get('title'))
        self.assertEqual(3, len(response.data.get('items')))

    def test_can_add_list(self):
        path = self._get_path_to_users(123456) + self._get_path_to_lists()
        response = self._current_client.post(
            path=path,
            data={
                'title': 'some new list'})
        self.assertEqual(201, response.status_code)
        self.assertEqual(4, self.common_user.items.count())
        self.assertTrue(self.common_user.items.filter(ind=4))

    def test_can_replace_list(self):
        path = self._get_path_to_users(123456) + self._get_path_to_lists(3)
        self.assertEqual('birthday', self.common_user.items.get(ind=2).title)
        self.assertEqual('car', self.common_user.items.get(ind=3).title)
        response = self._current_client.patch(
            path=path,
            data=json.dumps({'ind': 2}),
            content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('car', self.common_user.items.get(ind=2).title)
        self.assertEqual('birthday', self.common_user.items.get(ind=3).title)

    def test_replace_with_too_big_ind(self):
        path = self._get_path_to_users(123456) + self._get_path_to_lists(1)
        response = self._current_client.patch(
            path=path,
            data=json.dumps({'ind': 100500}),
            content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            'received index bigger than count of list elements',
            response.data.get('ind')[0])

    def test_replace_with_zero_ind(self):
        path = self._get_path_to_users(123456) + self._get_path_to_lists(2)
        response = self._current_client.patch(
            path=path,
            data=json.dumps({'ind': 0}),
            content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            'index must be positive integer',
            response.data.get('ind')[0])

    def test_replace_with_negative_ind(self):
        path = self._get_path_to_users(123456) + self._get_path_to_lists(3)
        response = self._current_client.patch(
            path=path,
            data=json.dumps({'ind': -4}),
            content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            'index must be positive integer',
            response.data.get('ind')[0])

    def test_can_delete_list(self):
        path = self._get_path_to_users(123456) + self._get_path_to_lists(3)
        response = self._current_client.delete(path=path)
        self.assertEqual(204, response.status_code)
        self.assertFalse(self.common_user.items.filter(ind=3).count())
        response1 = self._current_client.get(path=path)
        self.assertEqual(404, response1.status_code)

    def test_can_bulk_create(self):
        path = (self._get_path_to_users(123456) + self._get_path_to_lists() +
                'bulk_create/')
        response = self._current_client.post(
            path=path,
            data=json.dumps([
                {'title': 'from bulk'},
                {'title': 'another from bulk'}]),
            content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(5, self.common_user.items.count())

    def test_can_bulk_delete(self):
        path = (self._get_path_to_users(123456) + self._get_path_to_lists() +
                'bulk_delete/')
        response = self._current_client.delete(
            path=path,
            data=json.dumps({
                'items': [2, 3]}),
            content_type='application/json')
        self.assertEqual(204, response.status_code)
        self.assertEqual(1, self.common_user.items.count())

    def test_can_choose_purchases_by_list_ind(self):
        path1 = self._get_path_to_users(123456) + self._get_path_to_lists(1)
        path2 = (self._get_path_to_users(123456) + self._get_path_to_lists(1) +
                 self._get_path_to_purchases())
        response1 = self._current_client.get(path1)
        response2 = self._current_client.get(path2)
        self.assertEqual(response1.data.get('items'), response2.data)
