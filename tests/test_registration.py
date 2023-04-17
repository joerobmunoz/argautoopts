import pytest

from collections import namedtuple
import unittest


# Example invocation:
# 1. Decorate class
# 2. Class args show as cli options
    # 2a. Exploit type hint information
    # 2b. Exploit defaults

from tests.mocks.decorators import dummy_reg

def test_class_args_registered(dummy_reg):
    from argautoopts.decorate import OBJECT_REGISTRATION
    
    DummyClass = dummy_reg
    assert(DummyClass.__name__ in OBJECT_REGISTRATION)
    item = OBJECT_REGISTRATION[DummyClass.__name__]
    assert(len(item.named_args) == 2)
    
def test_namedtuple():
    from argautoopts.decorate import register_opts, OBJECT_REGISTRATION
    
    _named_tuple = namedtuple('TestT', 'test_num', defaults=(1,))
    _registered_named_tuple = register_opts(_named_tuple)
    assert('TestT' in OBJECT_REGISTRATION)
    item = OBJECT_REGISTRATION['TestT']
    
    assert(len(item.named_args) == 1)
    assert(item.named_args[0].arg_name == 'test_num')
    assert(item.named_args[0].value == 1)
    assert(item.named_args[0].has_default)

def test_dataclass():
    pass        

if __name__ == '__main__':
    pytest.main()