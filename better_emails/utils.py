from django.utils.importlib import import_module

def import_object(dottedpath):
    """
    Load a class/object from a module in dotted-path notation.
    E.g.: load_class("package.module.class").
    """
    splitted_path = dottedpath.split('.')
    module = '.'.join(splitted_path[:-1])
    obj = splitted_path[-1]
    
    module = import_module(module)
    
    return getattr(module, obj)
