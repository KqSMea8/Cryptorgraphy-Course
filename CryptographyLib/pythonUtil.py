class ClassProperty(object):
    # TODO
    # let the use needn't to use self param
    """
    read-only class property
    """

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)
