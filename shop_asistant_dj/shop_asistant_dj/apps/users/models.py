from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''Кастомная модель пользователя, уникальное
    значени telegram id вместо username'''
    telegram_id = models.IntegerField('Telegram id', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_bot = models.BooleanField(default=False)
    date_joining = models.DateTimeField(
        'Date of joining', auto_now_add=True)
    last_change = models.DateTimeField('Last action', auto_now=True)
    first_name = models.CharField(
        'First name', max_length=55, null=True, blank=True)
    last_name = models.CharField(
        'Second name', max_length=55, null=True, blank=True)
    nickname = models.CharField(
        'Nickname', max_length=55, null=True, blank=True)

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return '{}, {} ({} {})'.format(
            self.telegram_id,
            self.nickname,
            self.first_name,
            self.last_name)
