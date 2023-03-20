
import argparse

import argautoopts as aa

"""
Usage:
    python examples/hello_world_argparse.py --TestClass basic_int=1,test_str="hey its me ur class"
"""

@aa.register
class TestClass(object):
    def __init__(self, basic_int:int, test_str:str='default') -> None:
        self.basic_int = basic_int
        self.test_str = test_str
        
    def do_some_complicated_thing(self):
        print(f'My values are "{self.basic_int}" and "{self.test_str}"')

if __name__ == "__main__":
    # Create a parser like normal
    parser = argparse.ArgumentParser()
    
    # Extend it with our front-end
    parser = aa.frontends.argparse.extend_parser(parser)
    
    # Parse, parse, parse-a-delphia
    args = parser.parse_args()
    
    # Create an object with the injected parameters
    obj = aa.resolve(TestClass)
    print(obj.__dict__)
    obj.do_some_complicated_thing()