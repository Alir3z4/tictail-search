import sys
import operator
from server import exceptions

from server.exceptions import ObjectDoesNotExist


class ModelObjectManager(object):
    model = None
    allowed_lookups = None
    raw_data = {}

    SORT_BY_ASCENDING = 1
    SORT_BY_DESCENDING = 2

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

    @staticmethod
    def filter_lookup_exact(data, attr, what):
        """
        :type data: dict
        :type attr: str
        :type lookup: dict
        """
        return data[attr] == what

    def get_filter_lookup_type(self, lookup_filter):
        """
        :type lookup_filter: str

        :rtype: str
        """
        return lookup_filter.split('__')[1]

    @staticmethod
    def sort_by(data_list, sort_by):
        """
        :type data_list: list of Model
        :type field_name: str

        :returns: Return list of Models sorted by `field_name`
        :rtype: list of Model
        """
        return sorted(
            data_list,
            key=operator.itemgetter(sort_by[0]),
            reverse=sort_by[1] == ModelObjectManager.SORT_BY_DESCENDING
        )

    def filter(self, filters, sort_by=None):
        """
        :type filters: dict
        :type sort_by: tuple of str
        :rtype: list of Model
        """
        data_list = []
        raw_data = self.get_raw_data()
        model = self.get_model()
        model_name = self.get_model_name()
        model_data = raw_data[model_name]
        allowed_lookups = self.get_allowed_lookups()
        # Just to get field names
        first_id = model_data.keys()[0]
        first_row = model_data[first_id]
        first_row['id'] = first_id

        for fn in filters:
            fn_key = fn.split('__')[0]
            if fn_key not in first_row.keys():
                raise exceptions.FieldDoesNotExist(fn_key)

            if sort_by and sort_by[0] not in first_row.keys():
                raise Exception()

            if not fn.endswith('__'):
                filters['{0}__exact'.format(fn)] = filters.pop(fn)

        for id, data in model_data.items():
            data['id'] = id
            row_matches = True

            for k, v in filters.items():
                lookup_type = self.get_filter_lookup_type(k)
                attr = k.split('__')[0]

                if lookup_type not in allowed_lookups:
                    raise Exception()

                filter_lookup = allowed_lookups[lookup_type]

                if not filter_lookup(data, attr, v):
                    row_matches = False

            if row_matches:
                data_list.append(model.__class__(**data))

        if sort_by:
            data_list = self.sort_by(data_list, sort_by)

        return data_list

    def all(self, sort_by=None):
        """
        :type sort_by: tuple of str
        :rtype: list of Model
        """
        raw_data = self.get_raw_data()
        model = self.get_model()

        data_list = []
        for k, v in raw_data[self.get_model_name()].items():
            v['id'] = k
            data_list.append(model.__class__(**v))

        if sort_by and sort_by[0] not in data_list[0].get_model_fields():
            raise exceptions.FieldDoesNotExist(sort_by[0])

        if sort_by:
            data_list = self.sort_by(data_list, sort_by)

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

        return model.__class__(**model_raw_data[id])


class Model(object):
    objects = None
    fields = []

    def __init__(self, *args, **kwargs):
        self.objects = ModelObjectManager(self)
        self.fields = kwargs.keys()

        for k, v in kwargs.items():
            setattr(self, k, v)

            if k.endswith('_id'):
                re_model_name = k.replace('_id', '')
                rel_model_class = getattr(sys.modules[__name__],
                                '{0}s'.format(re_model_name.capitalize()))
                setattr(self, re_model_name, rel_model_class.objects.get(id=v))

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

    def to_dict(self):
        """
        :rtype: dict
        """
        dictator = {}
        for f in self.get_model_fields():
            dictator[f] = getattr(self, f)
            if f.endswith('_id'):
                f = f.replace('_id', '')
                dictator[f] = getattr(self, f).to_dict()

        return dictator

    def __getitem__(self, item):
        if item in self.get_model_fields():
            return getattr(self, item)

        return None


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
