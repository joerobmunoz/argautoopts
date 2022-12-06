import unittest, argparse

from typing import List

from argautoopts.decorate import OBJECT_REGISTRATION
from argautoopts.frontends.argparse import extend_parser
from tests.mocks.decorators import DummyClass

class TestDecoratedClassesShouldRegister(unittest.TestCase):
    def setUp(self):
        self.registered_dummy_class = OBJECT_REGISTRATION[DummyClass.__name__]
        
    def test_parser(self):
        parser = parser = argparse.ArgumentParser()
        parser = extend_parser(parser, OBJECT_REGISTRATION)
        
        parser.print_help()
        parsed = parser.parse_args(['DummyClass', '--test_num', '5'])
        import pdb;pdb.set_trace()
        
    def test_cli_requires_dummy(self):
        """When configured as a CLI, it should show Dummy Class options
        """
        pass
        
    def test_config_requires_dummy(self):
        """When configured as a config file input, it should show Dummy Class options
        """
        pass
    
def parse_args(args: List[str],
               parser: argparse.ArgumentParser=None,
               ) -> argparse.ArgumentParser:
    """Take command line arguments and create an argparse parser. If a paser is provided, it
    is augmented to include registered classes.

    Args:
        args (List[str]): The sys.argv[1:] args
        parser (argparse.ArgumentParser, optional): An argparse parser. Defaults to None.

    Returns:
        argparse.ArgumentParser: An argparse parser
    """
    
    if not parser:
        parser = argparse.ArgumentParser()
    
    parser = extend_parser(parser, OBJECT_REGISTRATION)
    
    return parser.parse_args(args)
    
if __name__ == '__main__':
    unittest.main()