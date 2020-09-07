
from django.db import models
from django.utils import timezone
from utils.mixins import ItemOwnerMixin


class PurchasesList(ItemOwnerMixin, models.Model):
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='items')
    ind = models.IntegerField('List index', default=1000)
    title = models.CharField('List title', max_length=20)
    creation_time = models.DateTimeField('Creation time', default=timezone.now)
    last_change = models.DateTimeField('Last change', default=timezone.now)

    class Meta:
        ordering = ('ind', 'creation_time')

    def __str__(self):
        return 'List \'{}\' by {}, includes {} element(s)'.format(self.title, \
        self.author.telegram_id, str(self.items_count))


class Purchase(models.Model):
    purchase_list = models.ForeignKey(PurchasesList, on_delete=models.CASCADE, related_name='items')
    ind = models.IntegerField('Purchase index', default=1000)
    title = models.CharField('Purchase title', max_length=20)
    creation_time = models.DateTimeField('Creation time', default=timezone.now)

    class Meta:
        ordering = ('ind', 'creation_time')

    def __str__(self):
        return self.title

    def get_user(self):
        return self.purchase_list.author
