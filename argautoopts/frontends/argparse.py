import argparse
import inspect

from typing import Dict, List

from ..register import RegistryItem
from ..decorate import OBJECT_REGISTRATION
from ..resolver import IOCResolver

def create_parser(*args, **kwargs):
    """Create a simple parser object with registered objects
            args and kwargs are passed to the ArgumentParser __init__
            method

    Returns:
        argparse.ArgumentParser: Argparse parser object with registrations
    """
    parser = argparse.ArgumentParser(*args, **kwargs)
    parser = extend_parser(parser, OBJECT_REGISTRATION)
    return parser

def extend_parser(parser: argparse.ArgumentParser,
                  OBJECT_REGISTRATION: Dict[str, RegistryItem],
                  ) -> argparse.ArgumentParser:
    """Given a parser instance, extend it with registered classes

    Args:
        parser (argparse.ArgumentParser): an argparse parser
        OBJECT_REGISTRATION (Dict): the dictionary of registerable types
    Returns:
        argparse.ArgumentParser: an argparse parser
    """
    
    subparser = parser.add_subparsers(title='Define dependencies')
    for class_key, registry_item in OBJECT_REGISTRATION.items():
        # each DI item gets its own group
        
        _class_parser_desc = f'Parameter namespace for class {class_key}'
        _class_parser = subparser.add_parser(class_key,
                                              description=_class_parser_desc,
                                              )
        
        for reg_arg in registry_item.named_args:
            help_str = f'{reg_arg.arg_name} parameter'
            a_dict = { 'help': {help_str} }
            
            if reg_arg.has_default:
                a_dict['default'] = reg_arg.value
                a_dict['help'] = f'{help_str}. (Default: "{reg_arg.value}")'
                
            if reg_arg.type != inspect.Parameter.empty:
                a_dict['type'] = reg_arg.type
            
            _class_parser.add_argument(f'--{reg_arg.arg_name}', **a_dict)
            
    return parser

def resolver_from_parser(parser: argparse.ArgumentParser,) -> IOCResolver:
    """Create a fully-registered resolver object from the parser

    Args:
        parser (argparse.ArgumentParser): _description_
    """
    raise NotImplementedError