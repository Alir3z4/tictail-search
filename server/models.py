import sys

from server.exceptions import ObjectDoesNotExist


class ModelObjectManager(object):
    model = None
    raw_data = {}

    def __init__(self, model):
        """
        :rtype: model
        """
        self.model = model

    def get_raw_data(self):
        """
        :rtype: dict
        """
        return self.raw_data

    def get_model(self):
        """
        :rtype: Model
        """
        return self.model

    def get(self, id):
        """
        Return object by given `id`.

        :type id: str
        :raises ObjectDoesNotExist: If object doesn't exist from given `id`.
        """
        raw_data = self.get_raw_data()
        model = self.get_model()
        model_name = model.__class__.__name__
        model_raw_data = raw_data[model_name]

        if id not in model_raw_data:
            raise ObjectDoesNotExist()

        return model.__class__(id=id, **model_raw_data[id])


class Model(object):
    objects = None
    _fields = []

    def __init__(self, *args, **kwargs):
        self.objects = ModelObjectManager(self)

        for k, v in kwargs.items():
            self._fields.append(k)

            setattr(self, k, v)

            if k.endswith('_id'):
                model_name = k.replace('_id', '')
                model = getattr(sys.modules[__name__],
                                '{0}s'.format(model_name.capitalize()))
                setattr(self, model_name, model.objects.get(id=v))

    def get_model_fields(self):
        """
        :rtype: tuple of str
        """
        return self._fields

    def get_model_name(self):
        """
        :rtype: str
        """
        return self.__class__


class Products(Model):
    pass


class Shops(Model):
    pass


class Tags(Model):
    pass


class Taggings(Model):
    pass


Products = Products()
Shops = Shops()
Tags = Tags()
Taggings = Taggings()
