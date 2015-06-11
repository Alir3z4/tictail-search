import sys
import operator

from server import exceptions
from server.exceptions import ObjectDoesNotExist


class ModelObjectManager(object):
    """
    ModelObjectManager

    Model Object Manager is the way for getting data from.

    Each ``Model`` will be using manager for dealing with:

    * Retrieving
    * Filtering
    * Sorting

    ``ModelObjectManager`` is set on ``Model`` class which will be inherited
    by other models. All the models then would have access to
    ``ModelObjectManager`` via ``objects`` attributes.

    Attributes:
    ===========

    * ``model``: The current ``Model`` that is using the model. All the
        actions on the manager will use the model name to deal with the data
        that are being kept in ``raw_data``.
    * ``allowed_lookups``: Allowed lookups includes ``in`` and ``exact`` which
        can be used in filters like: ``<field_name>__<lookup_type>``.
        * Lookup ``in`` is useful for passing a list or tuple into filter.
        * Lookup `exact` won't be used directly, is for internal usage of
        ``ModelObjectManager`` itself.
    * ``raw_data`` Hold the whole data in, it acts as the database in memory.
        Each set of data is kept with their unique ``id``.
    * ``SORT_BY_ASCENDING`` Define ascending.
    * ``SORT_BY_DESCENDING`` Define defending.
    """
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
        return self.model.get_model_name()

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

    @staticmethod
    def get_filter_lookup_type(lookup_filter):
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
        :raises exceptions.FieldDoesNotExist: If lookup field doesn't exist.
        :raises exceptions.InvalidSortKey: If the sort key is not valid.
        :raises exceptions.LookupIsNotAllowed: If lookup type is invalid.
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
                raise exceptions.InvalidSortKey(sort_by[0])

            if not fn.endswith('__'):
                filters['{0}__exact'.format(fn)] = filters.pop(fn)

        for pk, data in model_data.items():
            data['id'] = pk
            row_matches = True

            for k, v in filters.items():
                lookup_type = self.get_filter_lookup_type(k)
                attr = k.split('__')[0]

                if lookup_type not in allowed_lookups:
                    raise exceptions.LookupIsNotAllowed(lookup_type)

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
        :raises exceptions.InvalidSortKey: If the sort key is not valid.
        :rtype: list of Model
        """
        raw_data = self.get_raw_data()
        model = self.get_model()

        data_list = []
        for pk, v in raw_data[self.get_model_name()].items():
            v['id'] = pk
            data_list.append(model.__class__(**v))

        if sort_by and sort_by[0] not in data_list[0].get_model_fields():
            raise exceptions.InvalidSortKey(sort_by[0])

        if sort_by:
            data_list = self.sort_by(data_list, sort_by)

        return data_list

    def get(self, pk):
        """
        Return object by given `id`.

        :type pk: str
        :raises ObjectDoesNotExist: If object doesn't exist from given `pk`.
        """
        raw_data = self.get_raw_data()
        model = self.get_model()
        model_name = self.get_model_name()
        model_raw_data = raw_data[model_name]

        if pk not in model_raw_data:
            raise ObjectDoesNotExist()

        obj = model_raw_data[pk]
        obj['id'] = pk

        return model.__class__(**obj)


class Model(object):
    """
    Model

    Keeping the data that being hold in ``ModelObjectManager.raw_data``
    as models.

    ``Model`` can access the data in ``ModelObjectManager.raw_data`` through
    ``Model.object`` attribute.

    On the initializer of ``Model`` attributes will be set and can be
    treated as model fields. ``fields`` that that are ending with ``_id``
    are considered as relational keys and the related model would be set
    on th model.
    """
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
                setattr(self, re_model_name, rel_model_class.objects.get(pk=v))

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
        """
        :type item: str
        :raises exceptions.FieldDoesNotExist: When given field doesn't exist
            on the model.
        :rtype str
        """
        if item in self.get_model_fields():
            return getattr(self, item)

        raise exceptions.FieldDoesNotExist(item)


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
