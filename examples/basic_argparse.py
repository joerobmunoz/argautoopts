
import argautoopts as aa
# from argautoopts.frontends.argparse import extend_parser
import argparse

"""
Usage:
    python examples/basic/__init__.py -h TestClass --basic_int 1 --basic_str 'test1' TestClassTwo --basic_int 2 --basic_str 'test2'
"""

@aa.register
class TestClass(object):
    def __init__(self, basic_int:int, basic_str:str='default') -> None:
        pass
    
@aa.register
class TestClassTwo(object):
    def __init__(self, basic_int:int, basic_str:str='default') -> None:
        pass
    

# Simulating CLI args, ignore me
cliargs = ['--TestClass', 'basic_int=1,test_str="this is a long test string"',]

if __name__ == "__main__":
    # Create a parser like normal
    parser = argparse.ArgumentParser()
    
    # Extend it with our front-end
    parser = aa.frontends.argparse.extend_parser(parser)
    
    # Parse, parse, parse-a-delphia
    args = parser.parse_args(cliargs)
    
    # Create an object with the injected parameters
    obj = aa.resolve(TestClass)
    breakpoint()