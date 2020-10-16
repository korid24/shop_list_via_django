from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from api.utils.permissions import BotPermission


class CustomViewSetMixin:
    """
    Миксин с общими методами для вьюсетов списков покупок и покупок
    """
    def get_permissions(self):
        """
        В случае обращения к спискам покупок с указанием telegram id,
        необходимы права доступа бота, без указания - необходимо
        быть авторизированным
        """
        if self.kwargs.get('user_telegram_id_pk'):
            permission_classes = [BotPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_user(self):
        """
        В случае обращения к спискам покупок с указанием telegram id,
        пользователь определяется через telegram id, без указания -
        пользователем является тот, кто совершает запрос
        """
        user_telegram_id = self.kwargs.get(
            'user_telegram_id_pk', self.request.user.telegram_id)
        return get_object_or_404(
            CustomUser.objects.all(), telegram_id=user_telegram_id)

    def get_object(self):
        """
        Получает объект по переданному в URL индексу
        """
        ind = self.kwargs.get('pk')
        return get_object_or_404(self.get_queryset(), ind=ind)

    def destroy(self, request, *args, **kwargs):
        """
        Стандарное удаление, но выставляет правильные индексы после
        """
        self.get_object().delete()
        i = 1
        for obj in self.get_queryset():
            if obj.ind != i:
                self.get_queryset().filter(id=obj.id).update(ind=i)
            i += 1
        return Response(status=204)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request, *args, **kwargs):
        """
        Дает возможность создавать несколько элементов за раз
        """
        serializer = self.serializer_class(data=request.data, many=True)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        except ValidationError:
            return Response({
                'Error': 'A list with values was expected'},
                status=400)

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request, *args, **kwargs):
        """
        Дает возможность удалять несколько элементов за раз.
        Выставляет правильные индексы после удаления
        """
        numbers = self.request.data.get('items', [])
        items_to_delete = [n for n in numbers if isinstance(n, int)]
        if not items_to_delete:
            return Response({
                'items': 'A list with integers was expected'},
                status=400)
        deleted = self.get_queryset().filter(ind__in=items_to_delete).delete()
        i = 1
        for obj in self.get_queryset():
            if obj.ind != i:
                self.get_queryset().filter(id=obj.id).update(ind=i)
            i += 1
        return Response({'number of items removed': deleted[0]}, status=204)
