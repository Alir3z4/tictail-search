import csv
import os
from os.path import join
from os.path import isfile
from os import listdir

from server import models


def load_data():
    """
    Loading data
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


