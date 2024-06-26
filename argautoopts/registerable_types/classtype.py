import inspect

from typing import Any, List

from ..registry import RegistryArg, RegisterableType

class ClassType(RegisterableType):
    def is_of_type(x:Any) -> bool:
        """Checks whether or not the type matches
        """
        return inspect.isclass(x)
    
    def get_name(obj: type) -> str:
        """Get the name from a class

        Returns:
            Callable[[], str]: A callback to fetch the name
        """
        return obj.__name__
    
    def get_args(obj: type) -> List[RegistryArg]:
        """Gets the registered type arguments
        """
        signature = inspect.signature(obj)
        
        args = []
        for name, parameter in signature.parameters.items():
            arg = RegistryArg(
                arg_name=name,
                type=parameter.annotation,
                value=parameter.default if parameter.default is not inspect.Parameter.empty else None,
                has_default = parameter.default is not inspect.Parameter.empty
            )
            args.append(arg)
            
        return args