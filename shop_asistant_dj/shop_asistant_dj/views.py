from django.http import HttpResponse, Http404, HttpResponseRedirect
from users.models import CustomUser
from purchase.models import PurchasesList, Purchase
from api.models import TelegramSession

def index(request):
    u = CustomUser.objects.get(telegram_id='123456')
    s =''
    for item in TelegramSession._meta.fields:
        s += item + '\n'
    return HttpResponse(s)
