"""Resolve from environment variables"""

import os

from copy import copy
from typing import Dict

from ..registry import RegistryItem
from ..resolver import IOCResolverType, resolver

def resolver_from_env(
                       OBJECT_REGISTRATION: Dict[str, RegistryItem],
                       ignore_none: bool = True) -> IOCResolverType:
    """Create a fully-registered resolver object from the parser

    Args:
        OBJECT_REGISTRATION: singleton dict of registrations
        ignore_none (bool): Do not populate empty --options
    """
    env_vars = clean_env_vars = copy(os.environ)
    for class_name in vars(env_vars):
        # If it's a registerable type, register it
        if class_name not in OBJECT_REGISTRATION:
            continue
        # Must have args
        _cls_args = getattr(env_vars, class_name)
        
        if not _cls_args and class_name in OBJECT_REGISTRATION:
            # Argparse will keep the key of any --option we
            # previously created. Remove it here.
            clean_env_vars.__dict__.pop(class_name)
            continue
        
        # Argparse uses a list of args
        _cls_args_dict = _cls_args[0]
        _r = resolver.register(class_name, _cls_args_dict)
        
    # breakpoint()
    return clean_env_vars, resolver