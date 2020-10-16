from rest_framework import serializers
from rest_framework.exceptions import ValidationError


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
                raise ValidationError(
                    'received index bigger than count of list elements')
            elif value < 1:
                raise ValidationError(
                    'index must be positive integer')
            else:
                return value
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
