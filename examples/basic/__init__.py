
from argautoopts.decorate import register_opts
from argautoopts.frontends.argparse import create_parser

# from front

@register_opts
class TestClass(object):
    def __init__(self, basic_int:int, basic_str:str='default') -> None:
        pass
    
@register_opts
class TestClassTwo(object):
    def __init__(self, basic_int:int, basic_str:str='default') -> None:
        pass
    
    
if __name__ == "__main__":
    parser = create_parser()
    parser.parse_args()