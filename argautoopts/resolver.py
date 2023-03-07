from collections import defaultdict
from functools import partial
from typing import Dict, Tuple, List, Union, Any

from .register import RegistryItem, type_is_registerable
from .decorate import REGISTERABLE_TYPES, OBJECT_REGISTRATION


class ArgAutoOptsException(Exception):
    pass

class ResolveException(ArgAutoOptsException):
    pass

class RegistrationException(ArgAutoOptsException):
    pass

class IOCResolverType:
    def __init__(self,
                 expected_registry: Dict[str, RegistryItem],) -> None:
        self.expected_registry = expected_registry
        self._registered = {}
        
    def register(self, class_name: str, items: List[Tuple[str, Any]]) -> 'IOCResolverType':
        """Register a new item so that it can be resolved.
        
        This is typically called from a front-end, as arguments
        are parsed. If a non-default 

        Args:
            class_name (str): The string class to register
            items (List[str, Any]): A dictionary of parameters and their
                values.

        Returns:
            IOCResolverType: The IOC Resolver object.
        """
        
        if class_name not in OBJECT_REGISTRATION:
            raise RegistrationException
        self._registered[class_name] = items
        return self
    
    def resolve(self, container_t: type):
        """Given a type and parameters, create an object of that type"""
        if not self.expected_registry:
            raise ResolveException("No items have been added to the registry. \
                Please use the appropriate front-end function to add parsed \
                items to the IOC_Resolver.")
        # Find a matching type
        t_matches = list(filter(lambda reg_t: reg_t.is_of_type(container_t), REGISTERABLE_TYPES))
        if not t_matches:
            raise ResolveException(f'No type support found for {container_t} \
                when creating container')
            
        # Find a matching name
        reg_base_t = t_matches[0]
        reg_name = reg_base_t.get_name(container_t)
        
        if reg_name not in self.expected_registry:
            raise ResolveException(f'Type was unexpected and must be registered before \
                attempting resolution.')
        if reg_name not in self._registered:
            raise ResolveException(f'<{reg_name}> was expected, but must be registered \
                by the frontend before requesting objects.')

# Global resolver object, singleton
IOC_Resolver : IOCResolverType = IOCResolverType(OBJECT_REGISTRATION)

# Update must be called before you can use the registry

    # parser[__EXT_SUBCMD_STORAGE__] = defaultdict(None)
    
    # subparser = parser.add_subparsers(title='Define dependencies')
    # for class_key, registry_item in OBJECT_REGISTRATION.items():
    #     # each DI item gets its own group
    #     _class_parser_desc = f'Parameter namespace for class {class_key}'
    #     _class_parser = subparser.add_parser(class_key,
    #                                           description=_class_parser_desc,
    #                                           )
        
    #     for reg_arg in registry_item.named_args:
    #         help_str = f'{reg_arg.arg_name} parameter'
    #         a_dict = { 'help': {help_str} }
            
    #         if reg_arg.has_default:
    #             a_dict['default'] = reg_arg.value
    #             a_dict['help'] = f'{help_str}. (Default: "{reg_arg.value}")'
                
    #         if reg_arg.type != inspect.Parameter.empty:
    #             a_dict['type'] = reg_arg.type
            
    #         _class_parser.add_argument(f'--{reg_arg.arg_name}', **a_dict)
            
    # # Augment parser to support nested subparsers
    # parser.parse_deps = parse_deps
    # return parser
    
        # parser[__EXT_SUBCMD_STORAGE__][class_key] = a_dict
