#!/usr/bin/python

# TODO: sort fields in __str__ alphabetically

import types

class Class:
    # handles both dictionary and DynamicObject
    def extend (self, values):
        # if type is DynamicObject
        try:
            isDynamicObject = getattr(values, "toDictionary")
            if (isDynamicObject): values = values.toDictionary()
            pass
        except AttributeError:
            pass

        for key in values:
            setattr(self, key, values[key])

    def __init__(self, values):
        # if type is DynamicObject
        try:
            isDynamicObject = getattr(values, "toDictionary")
            if (isDynamicObject): values = values.toDictionary()
            pass
        except AttributeError:
            pass
            
        for key in values:
            setattr(self, key, values[key])

    def __str__ (self):
        temp = {}
        for attr in vars(self):
            if (type(getattr(self, attr)) == types.InstanceType): temp[attr] = str(getattr(self, attr)) # if object
            else: temp[attr] = getattr(self, attr) # if regular field
        return str(temp)

    def __getitem__ (self, item):
        try:
            value = getattr(self, item)
            return value
        except AttributeError:
            return None

    def __setitem__ (self, item, value):
        setattr(self, item, value)

    def toDictionary (self):
        dictionary = {}
        for key in vars(self):
            dictionary[key] = self[key]
        return dictionary
    pass
