import users.models
import purchase.models


def set_indexes(function):
    def wrapper(self, *args, **kwargs):
        function(self, *args, **kwargs)
        items = self.get_items()
        i = 1
        for item in items:
            if item.ind != i:
                item.ind = i
                item.save()
            i += 1
    return wrapper
