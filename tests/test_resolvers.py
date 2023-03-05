import unittest

from argautoopts.decorate import OBJECT_REGISTRATION
from tests.mocks.decorators import DummyClass, DummyClass2, NotDecoratedClass

from argautoopts.resolver import IOC_Resolver, IOCResolverType, \
    ResolveException, RegistrationException

class TestDecoratedClassesShouldRegister(unittest.TestCase):
    def setUp(self):
        self.registered_dummy_class = OBJECT_REGISTRATION[DummyClass.__name__]
        self.resolver = IOCResolverType(OBJECT_REGISTRATION)
    
    def test_can_register_args(self):
        """CLI can recognize 2 DI classes at once
        """
        class1_name = 'DummyClass'
        class1_args = [{'test_num': '1', 'test_str': 'test1b'}]
        class2_name = 'DummyClass2'
        class2_args = [{'test_num': '2', 'test_str': 'test2b'}]
    
    def test_resolve_fails_when_no_args(self):
        """The IOC resolver can resolve a dummy class object when given
        argparse params"""
        resolve_dummy_obj_fn = lambda: self.resolver.resolve(NotDecoratedClass)
        self.assertRaises(ResolveException, resolve_dummy_obj_fn)
     
    def test_resolver_cant_register_undecorated_classes(self):
        """All classes must be registered through controlled hooks"""
        reg_unexpected_obj_fn = lambda: self.resolver.register('BadClass', [])
        self.assertRaises(RegistrationException, reg_unexpected_obj_fn)
        
    # def test_resolver_can_create_registered_object(self):
    #     """The IOC resolver can create objects from registered types"""
    #     pass
        
    
if __name__ == '__main__':
    unittest.main()