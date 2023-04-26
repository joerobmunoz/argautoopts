import pytest

from collections import namedtuple
from argautoopts.decorate import OBJECT_REGISTRATION, register_opts
from argautoopts.frontends.usertypes import Interfaces

INLINE_NAMED_TUPLE_CLS_NAME = 'TestInlineNamedTuple'

@pytest.fixture
def dummy_reg():    
    @register_opts
    class DummyClass(object):
        def __init__(self, test_num: int, test_str:str='test'):
            self.test_num = test_num
            self.test_str = test_str
                
        def __eq__(self, other):
            """For test assertions"""        
            return self.__dict__ == other.__dict__
        
    yield DummyClass
    
    # Test cleanup
    del(OBJECT_REGISTRATION[DummyClass.__name__])

@pytest.fixture
def dummy2_reg():
    @register_opts
    class DummyClass2(object):
        def __init__(self, test_num: int, test_str:str='test'):
            self.test_num = test_num
            self.test_str = test_str
            
    yield DummyClass2
    
    # Test cleanup
    del(OBJECT_REGISTRATION[DummyClass2.__name__])

# Make this for every test
class NotDecoratedClass(object):
    def __init__(self, test_num: int, test_str:str='test'):
        self.test_num = test_num
        self.test_str = test_str

@pytest.fixture
def dummydatacls_reg():
    @register_opts
    class DummyDataClass:
        basic_int: int
        test_str: str = 'test'
        
    yield DummyDataClass
    
    # Test cleanup
    del(OBJECT_REGISTRATION[DummyDataClass.__name__])
    
@pytest.fixture
def dummytypednamedtuple_reg():
    @register_opts
    class DummyTypedNamedTuple:
        basic_int: int
        test_str: str = 'test'
        
    yield DummyTypedNamedTuple
    
    # Test cleanup
    del(OBJECT_REGISTRATION[DummyTypedNamedTuple.__name__])

@pytest.fixture
def dummyinlinenamedtuple_reg():
    DummyInlineNamedTuple = namedtuple(INLINE_NAMED_TUPLE_CLS_NAME, 'basic_int test_str')
    register_opts(DummyInlineNamedTuple)
    yield DummyInlineNamedTuple
    
    # Test cleanup
    del(OBJECT_REGISTRATION[DummyInlineNamedTuple.__name__])
    
    
# Frontends
from argautoopts.frontends.argparse import ArgparseFrontend

@pytest.fixture
def dummy_reg_frontend():    
    @register_opts(frontend=ArgparseFrontend)
    class DummyClass(object):
        def __init__(self, test_num: int, test_str:str='test'):
            self.test_num = test_num
            self.test_str = test_str
                
        def __eq__(self, other):
            """For test assertions"""        
            return self.__dict__ == other.__dict__
        
    yield DummyClass
    
    # Test cleanup
    del(OBJECT_REGISTRATION[DummyClass.__name__])
    
@pytest.fixture
def dummy2_reg_frontend():    
    @register_opts(frontend=ArgparseFrontend)
    class Dummy2Class(object):
        def __init__(self, test_num: int, test_str:str='test'):
            self.test_num = test_num
            self.test_str = test_str
                
        def __eq__(self, other):
            """For test assertions"""        
            return self.__dict__ == other.__dict__
        
    yield Dummy2Class
    
    # Test cleanup
    del(OBJECT_REGISTRATION[Dummy2Class.__name__])


