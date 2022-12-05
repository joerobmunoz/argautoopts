from collections import namedtuple
import unittest


# Example invocation:
# 1. Decorate class
# 2. Class args show as cli options
    # 2a. Exploit type hint information
    # 2b. Exploit defaults

class TestDecoratedClassesShouldRegister(unittest.TestCase):
    def test_class_args_registered(self):
        from .mocks.decorators import DummyClass
        from argautoopts.decorate import OBJECT_REGISTRATION
        
        self.assertTrue(DummyClass.__name__ in OBJECT_REGISTRATION)
        item = OBJECT_REGISTRATION[DummyClass.__name__]
        self.assertTrue(len(item.named_args) == 1)
        
    def test_namedtuple(self):
        from argautoopts.decorate import register_opts, OBJECT_REGISTRATION
        
        _registered_named_tuple = register_opts(namedtuple('TestT', 'test_num', defaults=(1,)))
        self.assertTrue('TestT' in OBJECT_REGISTRATION)
        item = OBJECT_REGISTRATION['TestT']
        
        self.assertTrue(len(item.named_args) == 1)
        self.assertTrue(item.named_args[0].arg_name == 'test_num')
        self.assertTrue(item.named_args[0].value == 1)
        self.assertTrue(item.named_args[0].has_default)
    
    def test_dataclass(self):
        pass
        

if __name__ == '__main__':
    unittest.main()