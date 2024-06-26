import argparse
from copy import copy
import inspect

from collections import defaultdict
from typing import Dict, List

from .basetypes import FrontEndType

from ..registry import RegistryItem
from ..decorate import OBJECT_REGISTRATION
from ..resolver import IOCResolverType, resolver

__EXT_SUBCMD_STORAGE__ = '__ext_subcmds__'

class ArgparseFrontend(FrontEndType):
    def on_decorate():
        raise NotImplementedError()


def create_parser(*args, **kwargs):
    """Create a simple parser object with registered objects
            args and kwargs are passed to the ArgumentParser __init__
            method

    Returns:
        argparse.ArgumentParser: Argparse parser object with registrations
    """
    parser = argparse.ArgumentParser(*args, **kwargs)
    parser = extend_parser(parser)
    return parser

def extend_parser(parser: argparse.ArgumentParser,
                  ) -> argparse.ArgumentParser:
    """Given a parser instance, extend it with registered classes

    Args:
        parser (argparse.ArgumentParser): an argparse parser
        OBJECT_REGISTRATION (Dict): the dictionary of registerable types
    Returns:
        argparse.ArgumentParser: an argparse parser
    """

    for class_key, registry_item in OBJECT_REGISTRATION.items():
        # each DI item gets its own option
        cls_help=f"{class_key} parameters:\n"
        expected_param_pattern = ""
        for reg_arg in registry_item. named_args:
            if len(expected_param_pattern) > 1:
                expected_param_pattern += ","
                
            expected_param_pattern += f'{reg_arg.arg_name}='
            expected_param_pattern += f'<{str(reg_arg.type)[8:-2]}>'
                
        for c, reg_arg in enumerate(registry_item.named_args):
            if c != 0:
                cls_help += ', '
            if reg_arg.type != inspect.Parameter.empty:
                cls_help += f'{reg_arg.arg_name} ({str(reg_arg.type)[8:-2]}'
                if reg_arg.has_default:
                    cls_help += f', default: "{reg_arg.value}"'
                cls_help += ')'
            else:
                cls_help += f'{reg_arg.arg_name}'
            
        def _reflected_container_type(_str_arg:str):
            try:
                obj_injs = dict()
                for _arg_str in _str_arg.split(','):
                    k, v = _arg_str.split('=')
                    # Strip string quotes
                    obj_injs[k] = v.strip('\"')
                return obj_injs
            except:
                raise argparse.ArgumentTypeError(f"""Class arguments must be of format: \
                    --{class_key} {expected_param_pattern}
                    """)

        parser.add_argument(
            f'--{class_key}',
            help = cls_help,
            metavar = expected_param_pattern,
            # Assert unique class names
            dest = class_key,
            type = _reflected_container_type, 
            # required = True,
            nargs = 1)
        
    # Override parse_args to add to container registry
    parser.parse_args = decorate_parse_args(parser, OBJECT_REGISTRATION)
    
    return parser

def decorate_parse_args(parser: argparse.ArgumentParser,
                        OBJECT_REGISTRATION: Dict[str, RegistryItem],
                        ignore_none: bool = True) -> argparse.Namespace:
    _parse_args = parser.parse_args
    def wrapper(*args, **kwargs):
        _args = _parse_args(*args, **kwargs)
                
        # Register with IOC
        _args, _resolver = resolver_from_args(_args,
                                       OBJECT_REGISTRATION,
                                       ignore_none=ignore_none)
        
        return _args
    return wrapper
            
def resolver_from_args(cli_args: argparse.Namespace,
                       OBJECT_REGISTRATION: Dict[str, RegistryItem],
                       ignore_none: bool = True) -> IOCResolverType:
    """Create a fully-registered resolver object from the parser

    Args:
        parser (argparse.ArgumentParser): The argparse parser
        OBJECT_REGISTRATION: singleton dict of registrations
        ignore_none (bool): Do not populate empty --options
    """
    clean_cli_args = copy(cli_args)
    for class_name in vars(cli_args):
        # If it's a registerable type, register it
        if class_name not in OBJECT_REGISTRATION:
            continue
        # Must have args
        _cls_args = getattr(cli_args, class_name)
        
        if not _cls_args and class_name in OBJECT_REGISTRATION:
            # Argparse will keep the key of any --option we
            # previously created. Remove it here.
            clean_cli_args.__dict__.pop(class_name)
            continue
        
        # Argparse uses a list of args
        _cls_args_dict = _cls_args[0]
        _r = resolver.register(class_name, _cls_args_dict)
        
    # breakpoint()
    return clean_cli_args, resolver