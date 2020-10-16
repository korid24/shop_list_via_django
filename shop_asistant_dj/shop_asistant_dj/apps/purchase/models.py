
from django.db import models


class PurchasesList(models.Model):
    """
    Модель списка покупок
    """
    author = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE, related_name='items')
    ind = models.IntegerField('List index', blank=True)
    title = models.CharField('List title', max_length=256)
    creation_time = models.DateTimeField('Creation time', auto_now_add=True)
    last_change = models.DateTimeField('Last change', auto_now=True)

    class Meta:
        ordering = ('ind', 'creation_time')

    def __str__(self):
        return ('List \'{}\' by {}'
                .format(
                    self.title,
                    self.author))

    def save(self, *args, **kwargs):
        """
        При создании нового экземпляра проставляет ему индекс.
        Если у пользователя не было списков, то выставляет единицу,
        а если были то на единицу больше максимального существующего
        """
        if not self.id:
            try:
                latest_ind = self.author.items.latest('ind').ind
            except self.DoesNotExist:
                latest_ind = 0
            self.ind = latest_ind + 1
        return super(PurchasesList, self).save(*args, **kwargs)


class Purchase(models.Model):
    """
    Модель покупки
    """
    purchase_list = models.ForeignKey(
        PurchasesList, on_delete=models.CASCADE, related_name='items')
    ind = models.IntegerField('Purchase index', blank=True)
    title = models.CharField('Purchase title', max_length=256)
    creation_time = models.DateTimeField('Creation time', auto_now_add=True)

    class Meta:
        ordering = ('ind', 'creation_time')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        При создании нового экземпляра проставляет ему индекс.
        Если в списке не было покупок, то выставляет еденицу,
        а если были то на еденицу больше максимального существующего
        """
        if not self.id:
            try:
                latest_ind = self.purchase_list.items.latest('ind').ind
            except self.DoesNotExist:
                latest_ind = 0
            self.ind = latest_ind + 1
        return super(Purchase, self).save(*args, **kwargs)

    def get_user(self):
        return self.purchase_list.author
