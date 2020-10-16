from rest_framework_nested import routers
from . import views


app_name = 'api'

urlpatterns = []

# Начальные роутеры (пользователи для бота и списки покупок для обыного
# пользователя)
router = routers.SimpleRouter()
router.register(
    'purchaselist',
    views.PurchasesListsViewSet,
    basename='purchaselist')
router.register(
    'bot_user',
    views.BotUserViewSet,
    basename='bot_user'
)

# Вложенные роутеры
purchase_router = routers.NestedSimpleRouter(
    router, 'purchaselist', lookup='purchase_list')
purchase_router.register(
    'purchase',
    views.PurchaseViewSet,
    basename='purchase')

bot_purchase_list_router = routers.NestedSimpleRouter(
    router, 'bot_user', lookup='user_telegram_id')
bot_purchase_list_router.register(
    'bot_purchaselist',
    views.PurchasesListsViewSet,
    basename='bot_purchaselist')

bot_purchase_router = routers.NestedSimpleRouter(
    bot_purchase_list_router, 'bot_purchaselist', lookup='purchase_list')
bot_purchase_router.register(
    'bot_purchase',
    views.PurchaseViewSet,
    basename='bot_purchase')

# добавление всех роутеров к URLам
urlpatterns += (router.urls + purchase_router.urls +
                bot_purchase_list_router.urls + bot_purchase_router.urls)
