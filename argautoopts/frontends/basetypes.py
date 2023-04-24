from enum import Enum
from abc import ABC, abstractmethod, abstractstaticmethod

from .usertypes import Interfaces
from ..resolver import IOCResolverType

# Define front-end contracts


class FrontEndType(ABC):
    # @property
    # @abstractmethod
    # def interface() -> Interfaces:
    #     raise NotImplementedError('Front end types must declare an interface')
    
    
    @abstractstaticmethod
    def on_decorate() -> IOCResolverType:
        """
        When we need to resolve something, the appropriate chain of 
        front-end resolve dependencies will require this delegate.
        """
        raise NotImplementedError('A registration method must be created for\
                             each frontend.')    
