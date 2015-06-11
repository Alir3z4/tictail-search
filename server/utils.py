import csv
import os
from os.path import join
from os.path import isfile
from os import listdir

from server import models


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
