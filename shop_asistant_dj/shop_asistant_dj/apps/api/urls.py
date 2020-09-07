from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    # path('pls/', views.PurchasesListsView.as_view()),
    # path('purs/', views.PurchasesView.as_view()),
    # path('user/', views.UserDetailView.as_view()),
    path('telegram_session/', views.TelegramSessionView.as_view()),
]
