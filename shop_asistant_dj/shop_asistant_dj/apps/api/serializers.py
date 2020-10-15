from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from purchase.models import PurchasesList, Purchase
from users.models import CustomUser
from .utils.mixins import CustomUpdateMixin


class PurchaseSerializer(CustomUpdateMixin, serializers.ModelSerializer):
    """
    Сериализатор покупки
    """
    creation_time = serializers.DateTimeField(
        read_only=True, format='%d.%m.%Y %X')

    class Meta:
        model = Purchase
        fields = ('ind', 'title', 'creation_time')

    def get_instance_parrent(self):
        return self.instance.purchase_list


class PurchasesListSerializer(CustomUpdateMixin, serializers.ModelSerializer):
    """
    Сериализатор списка покупок
    """
    items = PurchaseSerializer(many=True, read_only=True)
    creation_time = serializers.DateTimeField(
        read_only=True, format='%d.%m.%Y %X')
    last_change = serializers.DateTimeField(
        read_only=True, format='%d.%m.%Y %X')

    class Meta:
        model = PurchasesList
        fields = (
            'ind', 'title', 'items', 'creation_time', 'last_change')

    def get_instance_parrent(self):
        return self.instance.author


class UserSummarySerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя, в котором выводятся только названия списков
    покупок
    """
    last_activity = serializers.DateTimeField(
        source='last_change', read_only=True, format='%d.%m.%Y %X')
    date_joining = serializers.DateTimeField(
        read_only=True, format='%d.%m.%Y %X')
    items = serializers.SlugRelatedField(
        slug_field='title', read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ('telegram_id', 'first_name', 'last_name', 'nickname',
                  'items', 'date_joining', 'last_activity')

    def validate_telegram_id(self, value):
        if self.instance:
            if self.instance.telegram_id != value:
                raise ValidationError('telegram_id cannot be changed')
        return value


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя, в котором выводятся списки покупок в развернутом
    виде
    """
    telegram_id = serializers.IntegerField(read_only=True)
    last_activity = serializers.DateTimeField(
        source='last_change', read_only=True, format='%d.%m.%Y %X')
    date_joining = serializers.DateTimeField(
        read_only=True, format='%d.%m.%Y %X')
    items = PurchasesListSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ('telegram_id', 'first_name', 'last_name', 'nickname',
                  'items', 'date_joining', 'last_activity')


class PasswordSetSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input-type': 'password'})
