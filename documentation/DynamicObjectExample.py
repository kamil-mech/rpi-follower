#!/usr/bin/python

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import DynamicObject
DynamicObject = DynamicObject.Class

# create object
print("# create object:")
obj = DynamicObject({ "a": 5, "b": "something"})
print(obj)
print("")

# access with dot notation
print("# access with dot notation")
print(obj.a)
print("")

# update / create field with dot notation
print("# update / create field with dot notation")
obj.c = True
print(obj)
print("")

# access like a dictionary / map
print("# access like a dictionary / map")
print(obj["a"])
print("")

# update / create field like a dictionary / map
print("# update / create field like a dictionary / map")
obj["d"] = 8
print(obj)
print("")

# extend object with dictionary - only affects values specified
print("# update object - only affects values specified")
obj.extend({"a": 10, "e": False})
print(obj)
print("")

# extend object with another DynamicObject
print("# extend object with another DynamicObject")
obj2 = DynamicObject({"a": 999, "w": True})
obj.extend(obj2)
print(obj)
print("")

# nested objects
print("# nested objects")
obj.f = DynamicObject({"x": 1, "y": 2, "z": 3})
print(obj)
print("")
