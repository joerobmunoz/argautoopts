from argautoopts.errors import ResolveException
import pytest


from argautoopts.frontends.argparse import extend_parser

# Test utilities
from tests.mocks.decorators import (
        dummy_reg,
        dummy2_reg,
        dummydatacls_reg,
        dummyinlinenamedtuple_reg,
        dummytypednamedtuple_reg,
        NotDecoratedClass,
        INLINE_NAMED_TUPLE_CLS_NAME,
        dummy_reg_frontend,
        dummy2_reg_frontend,
)
from tests.mocks.resolve import resolver
from tests.mocks.frontends import parser

def test_parser_help(parser):
    """Help flag calls sys exit
    """
    with pytest.raises(SystemExit):
        parser.parse_args(['-h'])
    
def test_argparse_shows_multiple_dependencies(parser):
    """When multiple classes ars registered, accept multiple groups
    """
    _h = parser.format_help()
    
def test_cli_requires_dummy(parser, dummy_reg):
    """When configured as a CLI, it should show Dummy Class options
    """
    DummyClass = dummy_reg
    
    # Parser must be extended after the fixture is suppled
    parser = extend_parser(parser)
    _h = parser.format_help()
    assert(DummyClass.__name__ in _h)
    
def test_cli_parses_subcommands(parser, dummy_reg, dummy2_reg):
    """CLI can recognize 2 DI classes at once
    """
    _cmd = ['--DummyClass', 
            'test_num=1,test_str="test1b"',
            '--DummyClass2',
            'test_num=2,test_str="test2b"']
    
    # Parser must be extended after the fixture is suppled
    parser = extend_parser(parser)
    args = parser.parse_args(_cmd)
    
    assert('DummyClass' in args)
    assert('DummyClass2' in args)
    
def test_registered_item_is_omitted_from_args(parser, dummy_reg, dummy2_reg):
    """An item should not show up up as an attribute in the parser
    obj if it has no parameters provided. We do want them to force
    an error if it's in strict mode.
    """
    
    _cmd = ['--DummyClass', 
            'test_num=1,test_str="test1b"',]
    # Parser must be extended after the fixture is suppled
    parser = extend_parser(parser)
    _args = parser.parse_args(_cmd)
    assert('DummyClass' in _args)
    assert('DummyClass2' not in _args)

def test_registration_reqs_frontends(dummy_reg_env):
    """
    Registration can target a front-end, instead of the global scope.
    By default, the CLI inherits unscoped variables. Manifests differently
    for different front ends:
    * CLI: prompts for in-scope vars
    * Env: reads globally
    * Remote Calls: only fetches in-scope
    
    When resolving, we can try "optimistic[ally]" to grab from parent
    scopes.
    """
    _cmd = ['--DummyClass', 
            'test_num=1,test_str="test1b"',]
    # Parser must be extended after the fixture is suppled
    parser = extend_parser(parser)
    _args = parser.parse_args(_cmd)
    breakpoint()
    assert('DummyClass' not in _args, 'Env variable scoped \
           should not show in cli help')
    
        
def test_decorators_req_frontend(dummy2)
        
# This is deprecated until we know how multiple front-ends will work.
# def test_throws_on_missing_required_type(parser, dummy_reg, dummy2_reg):
#     """All decorated types must be accounted for. None of this sloppy "maybe" stuff. This isn't Haskell."""
#     _cmd = ['--DummyClass', 
#             'test_num=1,test_str="test1b"',]
#     # Parser must be extended after the fixture is suppled
#     parser = extend_parser(parser)
#     with pytest.raises(ResolveException):
#         args = parser.parse_args(_cmd)
    
    # def test_config_requires_dummy(self):
    #     """When configured as a config file input, it should show Dummy Class options
    #     """
    #     pass
    
if __name__ == '__main__':
    pytest.main()