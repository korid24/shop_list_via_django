from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where telegram_id is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, telegram_id, password, **extra_fields):
        """
        Create and save a User with the given telegram_id and password.
        """
        # telegram_id = self.telegram_id
        user = self.model(telegram_id=telegram_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, telegram_id, password, **extra_fields):
        """
        Create and save a SuperUser with the given telegram_id and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(telegram_id, password, **extra_fields)
