import sys
from server import exceptions

from server.exceptions import ObjectDoesNotExist


class ModelObjectManager(object):
    model = None
    raw_data = {}

    def __init__(self, model):
        """
        :rtype: model
        """
        self.model = model

    def get_allowed_lookups(self):
        """
        :rtype: dict
        """
        if not self.allowed_lookups:
            self.allowed_lookups = {
                'in': self.filter_lookup_in,
                'exact': self.filter_lookup_exact
            }

        return self.allowed_lookups

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

    def get_model_name(self):
        """
        :rtype: str
        """
        return self.model.__class__.__name__

    @staticmethod
    def filter_lookup_in(data, attr, what):
        """
        :type data: dict
        :type attr: str
        :type what: list

        :rtype: bool
        """
        return data[attr] in what
        """
        :type filters: dict
        :rtype: list of Model
        """
        data_list = []
        raw_data = self.get_raw_data()
        model = self.get_model()
        model_name = self.get_model_name()
        model_data = raw_data[model_name]
        # Just to get field
        first_row = model_data[model_data.keys()[0]]

        for field_name in filters:
            if field_name not in first_row.keys():
                raise exceptions.FieldDoesNotExist(field_name)

        for id, data in model_data.items():
            if all([data[k] == v for k, v in filters.items()]):
                data_list.append(model.__class__(id=id, **data))

        return data_list

    def all(self):
        """
        :rtype: list of Model
        """
        raw_data = self.get_raw_data()
        model = self.get_model()

        data_list = []
        for k, v in raw_data[self.get_model_name()].items():
            data_list.append(model.__class__(id=k, **v))

        return data_list

    def get(self, id):
        """
        Return object by given `id`.

        :type id: str
        :raises ObjectDoesNotExist: If object doesn't exist from given `id`.
        """
        raw_data = self.get_raw_data()
        model = self.get_model()
        model_name = self.get_model_name()
        model_raw_data = raw_data[model_name]

        if id not in model_raw_data:
            raise ObjectDoesNotExist()

        return model.__class__(id=id, **model_raw_data[id])


class Model(object):
    objects = None
    fields = []

    def __init__(self, *args, **kwargs):
        self.objects = ModelObjectManager(self)
        self.fields = kwargs.keys()

        for k, v in kwargs.items():
            setattr(self, k, v)

            if k.endswith('_id'):
                model_name = k.replace('_id', '')
                model = getattr(sys.modules[__name__],
                                '{0}s'.format(model_name.capitalize()))
                setattr(self, model_name, model.objects.get(id=v))

    def get_model_fields(self):
        """
        :rtype: list of str
        """
        return self.fields

    def get_model_name(self):
        """
        :rtype: str
        """
        return self.__class__.__name__


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
