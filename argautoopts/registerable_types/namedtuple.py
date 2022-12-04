# from typing import Any

# raise NotImplementedError("Data classes are not implemented")

# def is_named_tuple(obj: Any) -> bool:
#     """Check whether an object is a collections.namedtuple

#     Args:
#         obj (Any): Any object

#     Returns:
#         bool: True if namedtuple type, else False
#     """
#     t = type(obj)
#     b = t.__bases__
#     if len(b) != 1 or b[0] != tuple:
#         return False
    
#     f = getattr(t, '_fields', None)
#     if not isinstance(f, tuple):
#         return False
    
#     return all(type(n)==str for n in f)
