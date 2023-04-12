from collections import namedtuple
from argautoopts.decorate import register_opts

INLINE_NAMED_TUPLE_CLS_NAME = 'TestInlineNamedTuple'

def make_dummy_reg():    
    @register_opts
    class DummyClass(object):
        def __init__(self, test_num: int, test_str:str='test'):
            self.test_num = test_num
            self.test_str = test_str
                
        def __eq__(self, other):
            """For test assertions"""        
            return self.__dict__ == other.__dict__
        
    return DummyClass

def make_dummy2_reg():
    @register_opts
    class DummyClass2(object):
        def __init__(self, test_num: int, test_str:str='test'):
            self.test_num = test_num
            self.test_str = test_str
            
    return DummyClass2

# Make this for every test
class NotDecoratedClass(object):
    def __init__(self, test_num: int, test_str:str='test'):
        self.test_num = test_num
        self.test_str = test_str

def make_dummydatacls_reg():
    @register_opts
    class DummyDataClass:
        basic_int: int
        test_str: str = 'test'
        
    return DummyDataClass
    
def make_dummytypednamedtuple_reg():
    @register_opts
    class DummyTypedNamedTuple:
        basic_int: int
        test_str: str = 'test'
        
    return DummyTypedNamedTuple

def make_dummyinlinenamedtuple_reg():
    DummyInlineNamedTuple = namedtuple(INLINE_NAMED_TUPLE_CLS_NAME, 'basic_int test_str')
    register_opts(DummyInlineNamedTuple)
    return DummyInlineNamedTuple