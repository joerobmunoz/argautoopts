from sys import argv
import unittest, argparse

from typing import List

from argautoopts.decorate import OBJECT_REGISTRATION
from argautoopts.frontends.argparse import extend_parser
from tests.mocks.decorators import DummyClass, DummyClass2

class TestDecoratedClassesShouldRegister(unittest.TestCase):
    def setUp(self):
        self.registered_dummy_class = OBJECT_REGISTRATION[DummyClass.__name__]
        self.parser = argparse.ArgumentParser()
        self.parser = extend_parser(self.parser, OBJECT_REGISTRATION)
        
    # def test_parser_help(self):
    #     """Help flag calls sys exit
    #     """
    #     command_with_help_flag, cmds = lambda: self.parser.parse_args(['DummyClass', '-h'])
    #     self.assertRaises(SystemExit, command_with_help_flag)
        
    def test_argparse_shows_multiple_sub_parsers(self):
        """When multiple classes ars registered, accept multiple groups
        """
        _h = self.parser.format_help()
        pass
        
    def test_cli_requires_dummy(self):
        """When configured as a CLI, it should show Dummy Class options
        """
        _h = self.parser.format_help()
        self.assertTrue(DummyClass.__name__ in _h)
        
    def test_cli_parses_subcommands(self):
        """CLI can recognize 2 DI classes at once
        """
        _cmd = ['DummyClass', '--test_num=1', '--test_str=test1b',
                'DummyClass2', '--test_num=2', '--test_str=test2b']
        rest = _cmd
        while rest:
            [args, rest] = self.parser.parse_known_args(rest)
            print(args)
            print(rest)
            print(print(self.parser.format_help()))
            breakpoint()
            
        # <Class> --opt --opt


        # args = self.parser.parse_args(_cmd)
        # self.assertTrue(args.DummyClass)
        
    # def test_config_requires_dummy(self):
    #     """When configured as a config file input, it should show Dummy Class options
    #     """
    #     pass
    
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
    return parser
    # return parser.parse_args(args)
    
if __name__ == '__main__':
    unittest.main()