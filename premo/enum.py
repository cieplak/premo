from __future__ import unicode_literals


class Enum(list):

    def __init__(self, *args, **kwargs):
        for arg in args:
            kwargs[arg] = arg
        super(Enum, self).__init__(kwargs.values())
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
