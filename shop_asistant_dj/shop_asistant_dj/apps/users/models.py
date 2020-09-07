from django.db import models
from purchase.models import PurchasesList
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
from utils.mixins import ItemOwnerMixin


class CustomUser(ItemOwnerMixin, AbstractBaseUser, PermissionsMixin):
    '''Кастомная модель пользователя, уникальное значени telegram id вместо username'''
    telegram_id = models.CharField('Telegram id', max_length=15, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joining = models.DateTimeField('Date of joining', default=timezone.now)
    last_change = models.DateTimeField('Last action', default=timezone.now)
    first_name = models.CharField('First name', max_length=15, default='unknown')
    last_name = models.CharField('Second name', max_length=15, default='unknown')
    nickname = models.CharField('Nickname', max_length=15, default='unknown')

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def set_personal_information(self, first_name=None, last_name=None, nickname=None):
        '''Присваевает юзеру персональную информацию'''
        self.first_name = first_name or 'unknown'
        self.last_name = last_name or 'unknown'
        self.nickname = nickname or 'unknown'
        self.save()
        print('Personal information for {} assigned!'.format(self.telegram_id))

    def __str__(self):
        return '{}, {} ({} {})'.format(self.telegram_id, self.nickname, \
        self.first_name, self.last_name)
