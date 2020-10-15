# from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.exceptions import ValidationError
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from purchase.models import Purchase, PurchasesList
from users.models import CustomUser
# from .models import TelegramSession
from .utils.mixins import CustomViewSetMixin
from .utils.permissions import BotPermission
from .serializers import (
    PurchasesListSerializer,
    PurchaseSerializer,
    UserSummarySerializer,
    UserDetailSerializer,
    PasswordSetSerializer)


class PurchasesListsViewSet(CustomViewSetMixin, viewsets.ModelViewSet):
    """
    Представление списков покупок
    """
    serializer_class = PurchasesListSerializer

    def get_queryset(self):
        """
        queryset - все списки покупок пользователя
        """
        return self.get_user().items.all()

    def perform_create(self, serializer):
        """
        Пользователь становится автором нового списка
        """
        serializer.save(author=self.get_user().user)


class PurchaseViewSet(CustomViewSetMixin, viewsets.ModelViewSet):
    """
    Представление покупок
    """
    serializer_class = PurchaseSerializer

    def get_purchase_list(self):
        """
        Получает текущий список
        """
        purchase_list_ind = self.kwargs.get('purchase_list_pk')
        return get_object_or_404(
            self.get_user().items.all(), ind=purchase_list_ind)

    def get_queryset(self):
        """
        queryset - все покупки из текущего списка
        """
        return self.get_purchase_list().items.all()

    def perform_create(self, serializer):
        """
        Создаваемая покупка попадает в текущий список
        """
        serializer.save(purchase_list=self.get_purchase_list())


class BotUserViewSet(viewsets.ModelViewSet):
    """
    Представление пользователей для бота
    """
    queryset = CustomUser.objects.all()
    permission_classes = (BotPermission, )
    http_method_names = ('get', 'post', 'put', 'patch', 'head', 'options')

    def get_serializer_class(self):
        """
        При вызове списка пользователей выводятся только названия списков
        покупок, в остальных случаях - полная информация
        """
        if self.request.method == 'GET' and self.kwargs.get('pk'):
            return UserDetailSerializer
        elif self.request.method == 'POST' and self.kwargs.get('pk'):
            return PasswordSetSerializer
        return UserSummarySerializer

    def get_object(self):
        """
        Получение пользователя через telegram_id в URL
        """
        telegram_id = self.kwargs.get('pk')
        return get_object_or_404(self.queryset, telegram_id=telegram_id)

    @action(detail=True, methods=['post'])
    def set_password(self, request, *args, **kwargs):
        current_user = self.get_object()
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user.set_password(serializer.validated_data['password'])
        current_user.save()
        return Response(status=204)


# class BotPurchaseListViewSet(CustomViewSetMixin, viewsets.ModelViewSet):
#     serializer_class = PurchasesListSerializer
#     permission_classes = (BotPermission, )
#
#     def get_user(self):
#         user_telegram_id = self.kwargs.get('user_telegram_id_pk')
#         return get_object_or_404(
#             CustomUser.objects.all(), telegram_id=user_telegram_id)
#
#     def get_queryset(self):
#         return self.get_user().items.all()
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.get_user())
#
#
# class BotPurchaseViewSet(CustomViewSetMixin, viewsets.ModelViewSet):
#     serializer_class = PurchaseSerializer
#     permission_classes = (BotPermission, )
#
#     def get_user(self):
#         user_telegram_id = self.kwargs.get('user_telegram_id_pk')
#         return get_object_or_404(
#             CustomUser.objects.all(), telegram_id=user_telegram_id)
#
#     def get_purchase_list(self):
#         purchase_list_ind = self.kwargs.get('purchase_list_pk')
#         return get_object_or_404(
#             self.get_user().items.all(), ind=purchase_list_ind)
#
#     def get_queryset(self):
#         return self.get_purchase_list().items.all()
#
#     def perform_create(self, serializer):
#         serializer.save(purchase_list=self.get_purchase_list())
