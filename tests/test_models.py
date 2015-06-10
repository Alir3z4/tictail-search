import os
from unittest import TestCase
from os.path import join, isfile
from os import listdir

from server import exceptions

from server.models import ModelObjectManager, Tags

class TestModelObjectManager(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestModelObjectManager, self).__init__(*args, **kwargs)

    def test_filter_lookup_in(self):
        attr = 'tag'
        data = {attr: 'men'}
        tags = ['no', 'country', 'for', 'old', 'men']

        self.assertTrue(ModelObjectManager.filter_lookup_in(data, attr, tags))
        self.assertFalse(ModelObjectManager.filter_lookup_in(data, attr, []))

    def test_filter_lookup_exact(self):
        attr = 'tag'
        data = {attr: 'men'}

        self.assertTrue(
            ModelObjectManager.filter_lookup_exact(data, attr, 'men')
        )
        self.assertFalse(
            ModelObjectManager.filter_lookup_exact(data, attr, 'women')
        )

    def test_get_model(self):
        manager = ModelObjectManager(Tags)
        model = manager.get_model()

        self.assertIsNotNone(model)
        self.assertIsInstance(model, Tags.__class__)

    def test_get(self):
        manager = ModelObjectManager(Tags)

        with self.assertRaises(exceptions.ObjectDoesNotExist):
            manager.get('jojo was a man who thought he was a loner')

        TAG_ID = 'b4a59f0e2e1342efa451237125bb331a'
        obj = manager.get(TAG_ID)

        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, Tags.__class__)
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.id, TAG_ID)

    def test_get_raw_data(self):
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        data_files = [join(data_path, f) for f in listdir(data_path)
                  if isfile(join(data_path, f))]

        manager = ModelObjectManager(Tags)
        raw_data = manager.get_raw_data()

        self.assertIsNotNone(raw_data)
        self.assertIsInstance(raw_data, dict)
        self.assertEqual(len(raw_data), len(data_files))

    def test_get_all(self):
        manager = ModelObjectManager(Tags)
        tags = manager.all()

        self.assertIsNotNone(tags)
        self.assertIsInstance(tags, list)

        for tag in tags:
            self.assertIsNotNone(tag)
            self.assertIsNotNone(tag.id)
            self.assertIsInstance(tag.id, str)
            self.assertIsNotNone(tag.tag)
            self.assertIsInstance(tag.tag, str)

    def test_filter(self):
        manager = ModelObjectManager(Tags)
        with self.assertRaises(exceptions.FieldDoesNotExist):
            manager.filter({'cat': 'miow'})

        tags = manager.filter({'tag': 'miow'})

        self.assertIsNotNone(tags)
        self.assertIsInstance(tags, list)
        self.assertEquals(len(tags), 0)

        tags = manager.filter({'tag': 'trousers'})

        self.assertIsNotNone(tags)
        self.assertIsInstance(tags, list)
        self.assertEquals(len(tags), 1)

        tag_list = ['trousers', 'plates']
        tags = manager.filter({'tag__in': tag_list})

        self.assertIsNotNone(tags)
        self.assertIsInstance(tags, list)
        self.assertEquals(len(tags), 2)

        tag_list = ['no', 'country', 'for', 'old', 'guys']
        tags = manager.filter({'tag__in': tag_list})

        self.assertIsNotNone(tags)
        self.assertIsInstance(tags, list)
        self.assertEquals(len(tags), 0)

    def test_sort_by(self):
        data_list = [
            {
                'name': 'me',
                'age': 42
            },
            {
                'name': 'you',
                'age': 23
            },
            {
                'name': 'wine',
                'age': 2000
            }
        ]
        sort_by = ('age', ModelObjectManager.SORT_BY_DESCENDING)
        data_sorted = ModelObjectManager.sort_by(data_list, sort_by)

        self.assertIsNotNone(data_sorted)
        self.assertEqual(data_sorted[0][sort_by[0]], 2000)
        self.assertEqual(data_sorted[1][sort_by[0]], 42)
        self.assertEqual(data_sorted[2][sort_by[0]], 23)

        sort_by = ('age', ModelObjectManager.SORT_BY_ASCENDING)
        data_sorted = ModelObjectManager.sort_by(data_sorted, sort_by)

        self.assertEqual(data_sorted[0][sort_by[0]], 23)
        self.assertEqual(data_sorted[1][sort_by[0]], 42)
        self.assertEqual(data_sorted[2][sort_by[0]], 2000)



class TestModel(TestCase):
    def test_get_model_fields(self):
        TAG_ID = 'b4a59f0e2e1342efa451237125bb331a'
        tag = Tags.objects.get(TAG_ID)
        model_fields = tag.get_model_fields()

        self.assertEquals(len(model_fields), 2)
        self.assertIn('id', model_fields)
        self.assertIn('tag', model_fields)

        for field_name in model_fields:
            attr = getattr(tag, field_name)

            self.assertIsNotNone(attr)
            self.assertIsInstance(attr, str)
            self.assertGreaterEqual(len(attr), 1)

    def test_get_model_name(self):
        #  You might ask why testing even Python's built-in
        #  It's because we're living a world of paranoia?
        #  No, model api might change in future and having the unit-test
        #  of that feature will insist of compatibility even in future
        model_name = Tags.get_model_name()

        self.assertIsNotNone(model_name)
        self.assertIsInstance(model_name, str)
        self.assertEqual(model_name, 'Tags')
