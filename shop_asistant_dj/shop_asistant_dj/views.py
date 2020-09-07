from django.http import HttpResponse, Http404, HttpResponseRedirect
from users.models import CustomUser
from purchase.models import PurchasesList, Purchase
from api.models import TelegramSession

def index(request):
    u = CustomUser.objects.get(telegram_id='123456')
    itms = [item.title for item in u.items.all()]

    return HttpResponse(itms)
