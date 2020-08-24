from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect


from rest_framework.response import Response
from rest_framework.views import APIView

from .secret import API_TOKEN_FOR_BOT
from purchase.models import Purchase, PurchasesList
from users.models import CustomUser
from .models import TelegramSession
from .serializers import (
    PurchasesListSerializer,
    PurchaseSerializer,
    UserDetailSerializer,
    # UserForBotSerializer,
    #TelegramSessionSerializer,
    )
# Create your views here.

def index(request):
    return HttpResponse('ready')


class PurchasesListsView(APIView):
    def get(self, request):
        pls = PurchasesList.objects.all()
        serializer = PurchasesListSerializer(pls, many=True)
        return Response(serializer.data)

class PurchasesView(APIView):
    '''Представление покупок'''
    def get(self, request):
        purs = Purchase.objects.all()
        serializer = PurchaseSerializer(purs, many=True)
        return Response(serializer.data)

    def post(self,request):
        print(request.user)
        print(request.data.get('message'))
        print(request.data)

        purs = Purchase.objects.all()
        serializer = PurchaseSerializer(purs, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    '''Детальная информация о пользователе'''
    def get(self,request):
        try:
            serializer = UserDetailSerializer(request.user)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'detail':'does not exist'})


class TelegramSessionView(APIView):
    '''Информация, передаваемая боту'''
    def post(self, request):
        if request.data.get('api_token') == API_TOKEN_FOR_BOT:
            user_telegram_id = str(request.data.get('telegram_id'))
            current_user, is_new_user = CustomUser.objects.get_or_create(
                telegram_id=user_telegram_id,
            )

            current_session, is_new_session = TelegramSession.objects.get_or_create(
                user=current_user,
            )
            serializer = current_session.action(**request.data)
            return Response(serializer.data)
        else:
            return Response({
                'Error' : True,
                'details' : 'Для доступа к информации недостаточно прав'
                })
