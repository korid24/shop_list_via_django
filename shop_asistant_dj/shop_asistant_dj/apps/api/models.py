from django.db import models
from django.utils import timezone
from users.models import CustomUser
from .serializers import UserBotApiSerializer, PurchasesListBotApiSerializer


class TelegramSession(models.Model):
    # Связь сессии и пользователя - одна сессия - один пользователь
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='telegram_session')
    # Текущая позиция сессииб 0 - старт
    position = models.IntegerField('Position', default=0)
    last_activity = models.DateTimeField('Last activity', default=timezone.now)


    def __str__(self):
        return 'Telegram session of {} now in list {}'.format(self.user,self.position)


    def action_field(self):
        '''Возвращает объект, над которым будут проводиться действия'''
        if self.position > 0:
            return self.user.items.get(ind=self.position)
        else:
            return self.user


    def move(self, way):
        '''Меняет позицию сессии'''
        if 0 <= way <= self.user.items_count:
            self.position = way
        else:
            self.position = 0
            print('Списка под номером {} не существует'.format(str(way)))
        self.save()


    def action(self, operation='move', data=[0], *args, **kwargs):
        '''Выполняет действие в сесси по запросу'''
        current_field = self.action_field()
        if operation == 'start':
            self.user.set_personal_information(*data)
            self.move(0)
        elif operation == 'add':
            current_field.add_items(data)
        elif operation == 'remove':
            current_field.remove_items(data)
        elif operation == 'replace' and len(data) == 2:
            old_index, new_index = data
            current_field.replace_items(old_index, new_index)
        elif operation == 'move':
            self.move(*data)
        else:
            print('Неверный запрос')

        if isinstance(self.action_field(), CustomUser):
            return UserBotApiSerializer(self.action_field())
        else:
            return PurchasesListBotApiSerializer(self.action_field())
