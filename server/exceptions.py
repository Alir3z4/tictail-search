class ObjectDoesNotExist(Exception):
    pass


class FieldDoesNotExist(Exception):
    field_name = None

    def __init__(self, field_name):
        """
        :type field_name: str
        """
        self.field_name = field_name

    def __str__(self):
        """
        :rtype: str
        """
        return self.field_name