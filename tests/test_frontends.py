from sys import argv
import unittest, argparse

from typing import List

from argautoopts.decorate import OBJECT_REGISTRATION
from argautoopts.frontends.argparse import extend_parser
from tests.mocks.decorators import DummyClass, DummyClass2

from argautoopts.resolver import IOC_Resolver

class TestDecoratedClassesShouldRegister(unittest.TestCase):
    def setUp(self):
        self.registered_dummy_class = OBJECT_REGISTRATION[DummyClass.__name__]
        self.parser = argparse.ArgumentParser()
        self.parser = extend_parser(self.parser, OBJECT_REGISTRATION)
        
    def test_parser_help(self):
        """Help flag calls sys exit
        """
        command_with_help_flag = lambda: self.parser.parse_args(['-h'])
        self.assertRaises(SystemExit, command_with_help_flag)
        
    def test_argparse_shows_multiple_dependencies(self):
        """When multiple classes ars registered, accept multiple groups
        """
        _h = self.parser.format_help()
        
    def test_cli_requires_dummy(self):
        """When configured as a CLI, it should show Dummy Class options
        """
        _h = self.parser.format_help()
        self.assertTrue(DummyClass.__name__ in _h)
        
    def test_cli_parses_subcommands(self):
        """CLI can recognize 2 DI classes at once
        """
        _cmd = ['--DummyClass', 
                'test_num=1,test_str="test1b"',
                '--DummyClass2',
                'test_num=2,test_str="test2b"']
        args = self.parser.parse_args(_cmd)
        
        self.assertTrue('DummyClass' in args)
        self.assertTrue('DummyClass2' in args)
            
    # def test_config_requires_dummy(self):
    #     """When configured as a config file input, it should show Dummy Class options
    #     """
    #     pass
    
if __name__ == '__main__':
    unittest.main()