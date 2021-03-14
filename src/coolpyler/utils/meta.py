import inspect
from typing import List


def map_hierarchy(root: type, overrides: List[type], new_module):
    overrides = {override.__name__: override for override in overrides}

    def map_class(class_: type):
        # print("mapping", class_.__name__)
        try:
            new_class = overrides[class_.__name__]
        except KeyError:
            new_class = class_
        new_class = type(
            new_class.__name__,
            class_.__bases__,
            {**class_.__dict__, **new_class.__dict__, "__module__": new_module},
        )
        setattr(new_module, new_class.__name__, new_class)

        for subclass in class_.__subclasses__():
            map_class(subclass)

    map_class(root)


def map_to_module(obj: object, map_attr, module):
    module_obj = getattr(module, obj.__class__.__name__)
    args = inspect.getfullargspec(module_obj.__init__).args[1:]
    module_obj_args = [map_attr(getattr(obj, arg)) for arg in args]
    return module_obj(*module_obj_args)


def from_module(module):
    caller_frame = inspect.currentframe().f_back
    exec(inspect.getsource(module), caller_frame.f_globals, caller_frame.f_locals)
