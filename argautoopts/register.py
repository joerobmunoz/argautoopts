from abc import ABC, ABCMeta, abstractmethod
from typing import Any, List, NamedTuple

class RegistryArg(NamedTuple):
    argname:Any      # Name of the argument
    type:Any         # Type hint
    value:Any        # Default signature value or set after user-supplied
    has_default:bool # Flag for whether it has a signature default

class RegisterableType(object):
    """New types must implement the following interfaces to be registerable.
    To implement a new type, simply inherit from this base class.
    """
    # __metaclass__ = ABCMeta
    
    @abstractmethod
    def is_of_type(self, x:Any) -> bool:
        """Checks whether or not the type matches
        """
        pass
    
    @abstractmethod
    def get_name(self, obj: type) -> str:
        """Gets the type name
        """
        pass
    
    @abstractmethod
    def get_args(self, obj: type) -> List[RegistryArg]:
        """Gets the arguments
        """
        pass
    
class RegistryItem(NamedTuple):
    name:str
    reg_type:RegisterableType
    type: Any
    named_args:List[RegistryArg]