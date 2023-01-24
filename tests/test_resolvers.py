import unittest

from argautoopts.decorate import OBJECT_REGISTRATION
from tests.mocks.decorators import DummyClass

class TestDecoratedClassesShouldRegister(unittest.TestCase):
    def setUp(self):
        self.registered_dummy_class = OBJECT_REGISTRATION[DummyClass.__name__]
    
    def test_resolve_fails_when_no_args(self):
        """The IOC resolver can resolve a dummy class object when given
        argparse params"""
        from argautoopts.resolver import IOCResolver, ResolveException
        resolver = IOCResolver(OBJECT_REGISTRATION)
        resolve_dummy_obj_fn = lambda: resolver.resolve(DummyClass)
        self.assertRaises(ResolveException, resolve_dummy_obj_fn)
        
    def test_resolver_can_create_registered_object(self):
        """The IOC resolver can create objects from registered types"""
        pass
    
if __name__ == '__main__':
    unittest.main()