import argparse
import inspect

from typing import Dict, List

from ..register import RegistryItem

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
        # each DI item gets its own group
        subparsers = parser.add_subparsers(title='Define dependencies')
        _class_parser_desc = f'Parameter namespace for class {class_key}'
        _class_parser = subparsers.add_parser(class_key,
                                              description=_class_parser_desc,
                                              )
        
        for reg_arg in registry_item.named_args:
            help_str = f'{reg_arg.arg_name} parameter'
            a_dict = {'help': f'{reg_arg.arg_name} parameter',
                    #   'dest': f'{class_key}.{reg_arg.arg_name}',
                      }
            if reg_arg.has_default:
                help_str += '. Default: {reg_arg.value}'
                a_dict['default'] = reg_arg.value
                
            if reg_arg.type != inspect.Parameter.empty:
                a_dict['type'] = reg_arg.type
            
            _class_parser.add_argument(f'--{reg_arg.arg_name}', **a_dict)
            
    return parser