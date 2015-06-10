class ObjectDoesNotExist(Exception):
    """
    ObjectDoesNotExist

    Should be raised when looked up object does not exist.
    """
    pass


class FieldDoesNotExist(Exception):
    """
    FieldDoesNotExist

    Should be raised when an filed is being passed object which doesn't
    exists on the `server.models.Model`
    """
    field_name = None

    def __init__(self, field_name):
        """
        :type field_name: str
        """
        self.field_name = field_name

    def __repr__(self):
        """
        :rtype: str
        """
        return self.field_name


class LookupIsNotAllowed(FieldDoesNotExist):
    """
    LookupIsNotAllowed

    Should be raised when an invalid lookup is being used on filtering.
    """
    pass


class InvalidSortKey(FieldDoesNotExist):
    """
    LookupIsNotAllowed

    Should be raised when the sort key is invalid and doesn't exists on model.
    A sort key is obviously a field on the `server.models.Model`.
    """
    pass
