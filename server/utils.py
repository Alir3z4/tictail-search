import csv
import logging
import os
from os.path import join
from os.path import isfile
from os import listdir

from werkzeug.contrib.cache import SimpleCache

from server import models

cache = SimpleCache()


def load_data():
    """
    Beginning of getting our data into memory.

    In the beginning of app_creation in flask, ``load_data`` will be called
    walk through ``./data/`` directory to get all the data files which are
    in `CSV` format.

    CSV files then will be loaded into `ModelObjectManager.raw_data`
    dictionary. The ``key`` for each data set will be set by their
    corresponding ``server.models.Model`` name.

    All the data are being casted/converted into hash/dictionary data type.

    :rtype: None
    """
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    data_files = [join(data_path, f) for f in listdir(data_path)
                  if isfile(join(data_path, f))]
    raw_data = {}

    for file_name in data_files:
        data = {}
        with open(file_name, 'r') as infile:
            reader = csv.DictReader(infile)
            for i in reader:
                data[i['id']] = {k: v for k, v in i.items() if k != 'id'}

        model_name = file_name.split('/')[-1].split('.')[0].capitalize()
        raw_data[model_name] = data
        setattr(models, model_name, getattr(models, model_name))

    setattr(models.ModelObjectManager, 'raw_data', raw_data)


def get_cash(key, timeout=60*60*24, new_value=None, default_value=None):
    """
    A simple cache utility method to get cached value based on the provided key.
    If the the returning value is `None` it will be generated and cached.
    Of course new value should be provided. So basically this method never
    return `None` value.
    Internal cache doesn't have this functionality. `cache.get` will
    return None or a default value but there's no new generated value.

    :param key: Cache key
    :type key: str

    :param timeout: Cache value timeout
    :type timeout: int

    :param new_value: New value to set if the stored cache value doesn't exist.
    This value will be cached and `default_value` will be ignored.
    :type new_value: object

    :param default_value: Default value if the stored cache value doesn't exist.
    This value will be returned and `new_value` will be ignored.
    :type default_value: object
    """
    logging.info(u"[get_cash]: Getting cache for: '{0}'".format(key))

    value = cache.get(key)
    if value is None:
        logging.info("[get_cash]: Cache is empty")

        if not new_value and not default_value:
            return None

        if default_value:
            logging.info("[get_cash]: Returning `default_value`")

            return default_value

        if new_value:
            logging.info("[get_cash]: Caching new value")
            cache.set(key, new_value, timeout)

            return new_value

    return value
