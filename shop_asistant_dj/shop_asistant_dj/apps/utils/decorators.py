import users.models
import purchase.models


def set_indexes(function):
    def wrapper(self, *args, **kwargs):
        function(self, *args, **kwargs)
        id_and_ind = self.items.values_list('id', 'ind')
        print(id_and_ind)
        for i in range(len(id_and_ind)):
            if id_and_ind[i][1] != i + 1:
                self.items.filter(id=id_and_ind[i][0]).update(ind=i+1)
    return wrapper
