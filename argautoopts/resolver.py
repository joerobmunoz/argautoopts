from typing import Dict, Any

from .registry import RegistryItem
from .decorate import REGISTERABLE_TYPES, OBJECT_REGISTRATION

__OBJ_META__ = '__obj_meta__'

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
        
    def register(self, class_name: str, 
                 items: Dict[str, Any],
                 unsafe: bool = False,
                 ) -> 'IOCResolverType':
        """Register a new item so that it can be resolved.
        
        This is typically called from a front-end, as arguments
        are parsed. If a non-default 

        Args:
            class_name (str): The string class to register
            items (List[str, Any]): A dictionary of parameters and their
                values.
            unsafe (bool): Flag allowing the registration of undecorated
                types.

        Returns:
            IOCResolverType: The IOC Resolver object.
        """
        
        if class_name not in self.expected_registry and not unsafe:
            raise RegistrationException('You cannot register a type ' \
                f'{class_name} because it was not previously registered ' \
                'and this was not marked as unsafe.')

        # Avoid polluting the front-end refs        
        items_c = items.copy()

        # If unsafe, mark as a dynamic type
        items_c[__OBJ_META__] = { 'unsafe': unsafe }
        self._registered[class_name] = items_c
        
        return self
    
    def resolve(self, container_t: type, ignore_extra_params:bool=False):
        """Given a type and parameters, create an object of that type

        Args:
            container_t (type): The type to resolve. Must be decorated
                or used in non-strict mode.
            ignore_extra_params (False): Do not error when discovering
                unnecessary parameters. This may result in unintended 
                behavior.

        Raises:
            ResolveException: General error with descriptor from
                resolution failure.
        """
        
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
            raise ResolveException(f'Type was unexpected and must be registered before ' \
                'attempting resolution.')
        if reg_name not in self._registered:
            raise ResolveException(f'Type <{reg_name}> was expected, but not supplied to ' \
                'a front-end. Verify that it is provided as arguments before resolving.')

        # Inflate a class with args
        inflate_args = self._registered[reg_name].copy()
        del(inflate_args[__OBJ_META__])
        
        # If an arg is missing and there's a default, fill it
        for reg_arg in self.expected_registry[reg_name].named_args:
            if reg_arg.arg_name not in inflate_args and \
                not reg_arg.has_default:
                raise ResolveException(f'Parameter {reg_arg.arg_name} ' \
                    f'for type {reg_name} has no supplied or default parameter')
        
        expected_arg_keys = map(lambda x: x.arg_name, self.expected_registry[reg_name].named_args)
        if ignore_extra_params:
            # Clear unexpected args
            # keys_in_common = set(inflate_args).intersection(expected_arg_keys)
            inflate_args = dict((k, inflate_args[k]) for k in inflate_args if k in expected_arg_keys)
        else:
            # Validate no extra params
            extra_keys = set(inflate_args) - set(expected_arg_keys)
            if len(extra_keys):
                raise ResolveException(f'Extra keys {extra_keys} were supplied during registry and ' \
                    'cannot be resolved. To ignore these, resolve with `ignore_extra_params=True`.')
        
        # If a missing arg and no default, check strict.
        obj = self.expected_registry[reg_name].type(**inflate_args)
        return obj
    
# Global resolver object, singleton
# Update must be called before you can use the registry
resolver : IOCResolverType = IOCResolverType(OBJECT_REGISTRATION)