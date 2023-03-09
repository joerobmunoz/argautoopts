from functools import partial
from typing import NamedTuple, Union, Optional, Any

from .registry import (
    RegisterableType, RegistryItem, type_is_registerable)

from .registerable_types import *

REGISTERABLE_TYPES = RegisterableType.__subclasses__()
OBJECT_REGISTRATION = {}

def register_opts(
    optionable_obj: Union[object, NamedTuple],
    name: Optional[str] = None,
    ) -> None:
    """_summary_

    Args:
        optionable_obj (Union[object, NamedTuple]): A decorated type to register
        name (Optional[str], optional): Override the type name to be registered.
                Defaults to None.

    Raises:
        ValueError: validation errors for registered types
    """
    
    _type_is_registerable = partial(type_is_registerable, optionable_obj)
    reg_types = list(filter(_type_is_registerable, REGISTERABLE_TYPES))
    
    # Registration assertions
    if len(reg_types) > 1:
        raise ValueError(f'Multiple types were found for class {optionable_obj}')
    if len(reg_types) == 0:
        raise ValueError(f'Type {optionable_obj} is not a supported type')
    
    reg_type = reg_types[0]
    
    if not name:
        name = reg_type.get_name(optionable_obj)
    
    if name in OBJECT_REGISTRATION:
        raise ValueError(f'Duplicate object names registered for {OBJECT_REGISTRATION[name]} and {optionable_obj}')

    # Create registry object
    args = reg_type.get_args(optionable_obj)
    item = RegistryItem(name=name,
                        reg_type=reg_type,
                        type=optionable_obj,
                        named_args=args)

    # Register object
    OBJECT_REGISTRATION[name] = item

    return optionable_obj