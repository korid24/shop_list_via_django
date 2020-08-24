from datetime import datetime

from rest_framework import serializers

from purchase.models import PurchasesList, Purchase
from users.models import CustomUser


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ('ind', 'title')


class PurchasesListSerializer(serializers.ModelSerializer):
    items = PurchaseSerializer(many=True)

    class Meta:
        model = PurchasesList
        fields = ('ind', 'title', 'items_count', 'items')

class UserDetailSerializer(serializers.ModelSerializer):
    '''Детальная информация о пользователе'''
    items = PurchasesListSerializer(many=True)
    last_login = serializers.DateTimeField(read_only=True, format='%d.%m.%Y %X')
    date_joining = serializers.DateTimeField(read_only=True, format='%d.%m.%Y %X')
    position_in_telegram_session = serializers.IntegerField(source='telegram_session.position', read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'telegram_id',
            'first_name',
            'last_name',
            'nickname',
            'last_login',
            'date_joining',
            'position_in_telegram_session',
            'items'
            )

class UserBotApiSerializer(serializers.ModelSerializer):
    '''Информация о пользователе, передаваемая боту'''
    items = serializers.SlugRelatedField(slug_field='title', read_only=True, many=True)
    position = serializers.IntegerField(source='telegram_session.position', read_only=True)

    class Meta:
        model = CustomUser
        fields = ('telegram_id', 'first_name', 'position', 'items_count', 'items')

class PurchasesListBotApiSerializer(serializers.ModelSerializer):
    '''Информация о списке покупок, передаваемая боту'''
    telegram_id = serializers.CharField(source='author.telegram_id', read_only=True)
    items = serializers.SlugRelatedField(slug_field='title', read_only=True, many=True)
    position = serializers.IntegerField(source='author.telegram_session.position', read_only=True)

    class Meta:
        model = PurchasesList
        fields = (
            'telegram_id',
            'title',
            'position',
            'items_count',
            'items',
            )
