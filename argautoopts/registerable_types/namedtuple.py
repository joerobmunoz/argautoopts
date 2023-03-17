import inspect

from typing import Any, List

from ..registry import RegistryArg, RegisterableType

class RegisterableType:
    def is_of_type(x:Any) -> bool:
        """Checks whether or not the type matches a namedtuple
        """
        return is_named_tuple(x)
    
    def get_name(obj: type) -> str:
        """Get the name from a namedtuple

        Returns:
            Callable[[], str]: A callback to fetch the name
        """
        return obj.__name__
    
    def get_args(obj: type) -> List[RegistryArg]:
        """Gets the registered type arguments
        """
        signature = inspect.signature(obj)
        
        args = []
        for name, parameter in signature.parameters.items():
            arg = RegistryArg(
                arg_name=name,
                type=parameter.annotation,
                value=parameter.default if parameter.default is not inspect.Parameter.empty else None,
                has_default = parameter.default is not inspect.Parameter.empty
            )
            args.append(arg)
            
        return args

def is_named_tuple(obj: Any) -> bool:
    """Check whether an object is a collections.namedtuple

    Args:
        obj (Any): Any object

    Returns:
        bool: True if namedtuple type, else False
    """
    t = type(obj)
    b = t.__bases__
    if len(b) != 1 or b[0] != tuple:
        return False
    
    f = getattr(t, '_fields', None)
    if not isinstance(f, tuple):
        return False
    
    return all(type(n)==str for n in f)
