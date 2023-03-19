from collections import namedtuple
from argautoopts.decorate import register_opts

INLINE_NAMED_TUPLE_CLS_NAME = 'TestInlineNamedTuple'

@register_opts
class DummyClass(object):
    def __init__(self, test_num: int, test_str:str='test'):
        self.test_num = test_num
        self.test_str = test_str
            
    def __eq__(self, other):
        """For test assertions"""        
        return self.__dict__ == other.__dict__

        
@register_opts
class DummyClass2(object):
    def __init__(self, test_num: int, test_str:str='test'):
        self.test_num = test_num
        self.test_str = test_str
        
class NotDecoratedClass(object):
    def __init__(self, test_num: int, test_str:str='test'):
        self.test_num = test_num
        self.test_str = test_str

@register_opts
class DummyDataClass:
    basic_int: int
    test_str: str = 'test'
    
@register_opts
class DummyTypedNamedTuple:
    basic_int: int
    test_str: str = 'test'
    
DummyInlineNamedTuple = namedtuple(INLINE_NAMED_TUPLE_CLS_NAME, 'basic_int test_str')
register_opts(DummyInlineNamedTuple)