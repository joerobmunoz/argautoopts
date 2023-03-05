import argparse
import inspect

from collections import defaultdict
from typing import Dict, List

from ..register import RegistryItem
from ..decorate import OBJECT_REGISTRATION
from ..resolver import IOCResolver

__EXT_SUBCMD_STORAGE__ = '__ext_subcmds__'

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

def parse_deps(parser):
    args = parser.parse.args()
    breakpoint()

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

    for class_key, registry_item in OBJECT_REGISTRATION.items():
        # each DI item gets its own option
        cls_help=f"{class_key} parameters:\n"
        expected_param_pattern = ""
        for reg_arg in registry_item.named_args:
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
            required = False,
            nargs = 1)
        
    # Override parse_args to add to container registry
    # parser.parse_args = parse_args_decorator
    # TODO: Strict/required storage in dict
    
    return parser
    
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


# def parse_args_decorator(self, *args, **kwargs):
#     # 'self' references parser
#     args = self.parse_args(*args, **kwargs)
    
#     # Register with IOC
    
#     return args
            
def resolver_from_args(parser: argparse.Namespace,) -> IOCResolver:
    """Create a fully-registered resolver object from the parser

    Args:
        parser (argparse.ArgumentParser): _description_
    """
    raise NotImplementedError