from math import fabs
from django.utils import timezone
from .decorators import set_indexes


class ItemOwnerMixin:
    '''Класс для наследования моделями-хозяевами каких-либо элементов'''
    def get_items(self):
        '''Возвращает все дочерние элементы'''
        return self.items.all()

    @property
    def items_count(self):
        '''Возвращает кол-во дочерних элементов'''
        return self.items.count()

    def add_items(self, items_titles_list:list):
        '''Добавляет в дочерние элементы значения из списка, которые отсутсвуют среди дочерних элементов'''
        current_list_items_titles = [item.title.upper() for item in self.get_items()]
        items_to_add = [t for t in items_titles_list if t.upper() not in current_list_items_titles]
        if items_to_add:
            new_items_count = self.items_count
            for item_title in items_to_add:
                new_items_count += 1
                self.items.create(ind=new_items_count, title=item_title.capitalize())
            self.last_change = timezone.now()
            self.save()
            print('Items {} has been successfully added to {}'.format(', '.join(items_to_add), self))
        else:
            print('No items to add')


    @set_indexes
    def remove_items(self, items_indexes_list:list):
        '''Удаляет дочерние элементы по индексам из списка, присваивает кореектные индексы после выполнения'''
        items_to_remove = sorted(set([int(ind) for ind in items_indexes_list if 0<int(ind)<=self.items_count]))
        for item_index in items_to_remove:
            self.items.get(ind=item_index).delete()
        self.last_change = timezone.now()
        self.save()
        print('{} item(s) has been removed'.format(str(len(items_to_remove))))


    @set_indexes
    def replace_items(self, old_index:int, new_index:int):
        '''Переназначает индексы дочерних элементов, присваивает кореектные индексы после выполнения'''
        if old_index != new_index and 0<old_index<=self.items_count and 0<new_index<=self.items_count:
            relocatable = self.items.get(ind=old_index)
            movable = self.items.get(ind=new_index)
            if fabs(relocatable.ind - movable.ind) == 1:
                relocatable.ind, movable.ind = movable.ind, relocatable.ind
                movable.save()
            else:
                if new_index > old_index:
                    if relocatable.creation_time > movable.creation_time:
                        relocatable.ind = new_index
                    else:
                        relocatable.ind = new_index + 1
                else:
                    if relocatable.creation_time > movable.creation_time:
                        relocatable.ind = new_index - 1
                    else:
                        relocatable.ind = new_index
            relocatable.save()
            self.last_change = timezone.now()
            self.save()
            print('{} now in position {}'.format(relocatable.title, str(new_index)))
