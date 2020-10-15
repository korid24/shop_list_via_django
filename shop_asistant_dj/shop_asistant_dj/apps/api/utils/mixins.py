from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from .permissions import BotPermission


class CustomUpdateMixin:
    """
    Миксин для переопределения метода update, при котором будут
    проставлятьстя индесы
    """

    def get_instance_parrent(self):
        """
        Абстрактный метод для получения владельца элемента
        """
        raise NotImplementedError(
            'You need to override the method \'get_instance_parrent\' in {}'
            .format(self.__class__.__name__))

    def validate_ind(self, value):
        items_count = self.get_instance_parrent().items.count()
        if value is not None:
            if value > items_count:
                return items_count
            elif value < 1:
                return 1
        else:
            return value

    def update(self, instance, validated_data):
        """
        Проставление корректных индексов при изменении порядка элементов
        """
        if validated_data.get('ind', instance.ind) != instance.ind:
            elements_sequence = list(
                self.get_instance_parrent().items.values_list('id', 'ind'))
            replaced_element = elements_sequence.pop(instance.ind - 1)
            elements_sequence.insert(
                validated_data['ind'] - 1, replaced_element)
            numbers_sequence = list(range(1, len(elements_sequence) + 1))
            for i in range(len(numbers_sequence)):
                element_id, element_ind = elements_sequence[i]
                if numbers_sequence[i] != element_ind:
                    (self.get_instance_parrent().items
                     .filter(id=element_id).update(ind=numbers_sequence[i]))
        return serializers.ModelSerializer.update(
            self, instance, validated_data)


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
            return Response(serializer.data, status=200)
        except ValidationError:
            return Response({
                'Error': 'A list with values was expected'},
                status=400)

    @action(detail=False, methods=['delete'])
    def bulk_destroy(self, request, *args, **kwargs):
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
