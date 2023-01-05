from abc import ABC, abstractclassmethod
from typing import Any, List, NamedTuple

class RegistryArg(NamedTuple):
    arg_name:Any      # Name of the argument
    type:Any         # Type hint
    value:Any        # Default signature value or set after user-supplied
    has_default:bool # Flag for whether it has a signature default

class RegisterableType(ABC):
    """New types must implement the following interfaces to be registerable.
    To implement a new type, simply inherit from this base class.
    """
    
    @abstractclassmethod
    def is_of_type(x:Any) -> bool:
        """Checks whether or not the type matches
        """
        pass
    
    @abstractclassmethod
    def get_name(obj: type) -> str:
        """Gets the type name
        """
        pass
    
    @abstractclassmethod
    def get_args(obj: type) -> List[RegistryArg]:
        """Gets the arguments
        """
        pass
    
class RegistryItem(NamedTuple):
    name:str
    reg_type:RegisterableType
    type: Any
    named_args:List[RegistryArg]
    
def type_is_registerable(obj: Any, t: RegisterableType) -> bool:
    return t.is_of_type(obj)