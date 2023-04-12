import unittest, argparse


from argautoopts.decorate import OBJECT_REGISTRATION
from argautoopts.frontends.argparse import extend_parser
from tests.mocks.decorators import (
    make_dummy_reg,
    make_dummy2_reg,
    make_dummydatacls_reg,
    make_dummyinlinenamedtuple_reg,
    make_dummytypednamedtuple_reg
)


class TestDecoratedClassesShouldRegister(unittest.TestCase):
    def setUpClass(self):
        self.DummyClass = make_dummy_reg()
        print('CALLED')
        self.registered_dummy_class = OBJECT_REGISTRATION[self.DummyClass.__name__]
        self.parser = argparse.ArgumentParser()
        self.parser = extend_parser(self.parser)
        
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
        breakpoint()
        self.assertTrue(self.DummyClass.__name__ in _h)
        
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
        
    def test_registered_item_is_omitted_from_args(self):
        """An item should not show up up as an attribute in the parser
        obj if it has no parameters provided. We do want them to force
        an error if it's in strict mode.
        """
        
        _cmd = ['--DummyClass', 
                'test_num=1,test_str="test1b"',]
        _args = self.parser.parse_args(_cmd)
        breakpoint()
        self.assertTrue('DummyClass' in _args)
        self.assertTrue('DummyClass2' not in _args)
        
    # def test_all_required_types_are_not_none_after_frontend_parsing(self):
    #     _cmd = ['--DummyClass', 
    #             'test_num=1,test_str="test1b"',]
    #     args = self.parser.parse_args(_cmd)  
    #     self.assertRaises(SystemExit, command_with_help_flag)
        
    # def test_config_requires_dummy(self):
    #     """When configured as a config file input, it should show Dummy Class options
    #     """
    #     pass
    
if __name__ == '__main__':
    unittest.main()