import argparse

from typing import Dict, List

from ..register import RegistryItem

# from ..decorate import OBJECT_REGISTRATION

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
        class_group = parser.add_argument_group(class_key)

        for reg_arg in registry_item.named_args:
            a_dict = {'help': f'{reg_arg.arg_name} parameter ',
                      'dest': class_key,
                      }
            if reg_arg.has_default:
                a_dict['default'] = reg_arg.value
            
            class_group.add_argument(f'--{reg_arg.arg_name}', **a_dict)
            
    return parser