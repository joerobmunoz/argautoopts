from functools import partial
from typing import Dict, Generic

from .register import RegistryItem, type_is_registerable
from .decorate import REGISTERABLE_TYPES

class ResolveException(Exception):
    pass

class IOCResolver:
    def __init__(self,
                 OBJECT_REGISTRATION: Dict[str, RegistryItem],) -> None:
        self.registry = OBJECT_REGISTRATION
    
    def resolve(self, container_t: type):
        """Given a type and parameters, create an object of that type"""
        pass
        # Find a matching type
        t_matches = list(filter(lambda reg_t: reg_t.is_of_type(container_t), REGISTERABLE_TYPES))
        if not t_matches:
            raise ResolveException(f'No type support found for {container_t} \
                when creating container')
            
        # Find a matching name
        reg_base_t = t_matches[0]
        reg_name = reg_base_t.get_name(container_t)
        
        if reg_name not in self.registry:
            raise ResolveException(f'Object type not found in the registry')
        
        # Create object from registry.
            # TODO: This needs to be populated by a front-end here