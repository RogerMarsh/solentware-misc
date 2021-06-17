# null.py
# Copyright 2010 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""This module is the placeholder object copied from Python Cookbook 2nd
edition 6.17.

"""

class Null(object):
    """Null objects always and reliably 'do nothing'.

    """
    
    # one instance per subclass optimization
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
        return cls._inst

    def __init__(self, *args, **kwargs):
        pass
    
    def __call__(self, *args, **kwargs):
        return self
    
    def __repr__(self):
        return 'Null()'
    
    def __bool__(self):
        return False
    
    def __getattr__(self, name):
        return self
    
    def __setattr__(self, name, value):
        return self
    
    def __delattr__(self, name):
        return self
    
