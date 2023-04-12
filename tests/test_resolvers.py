from dataclasses import dataclass
import unittest

from argautoopts.decorate import OBJECT_REGISTRATION
from tests.mocks.decorators import (
        make_dummy_reg,
        make_dummy2_reg,
        make_dummydatacls_reg,
        make_dummyinlinenamedtuple_reg,
        make_dummytypednamedtuple_reg,
        NotDecoratedClass,
        INLINE_NAMED_TUPLE_CLS_NAME,
)

from argautoopts.resolver import IOCResolverType
from argautoopts.errors import (
    ResolveException, RegistrationException
)
    
class TestDecoratedClassesShouldRegister(unittest.TestCase):
    def setUpClass(self):
        # Fake DummyClass is decorated/expected
        self.DummyClass = make_dummy_reg()
        self.registered_dummy_class = OBJECT_REGISTRATION[self.DummyClass.__name__]
        self.resolver = IOCResolverType(OBJECT_REGISTRATION)
    
    def test_supplied_class_is_registered(self):
        """CLI can recognize 2 DI classes at once"""
        class1_name = 'DummyClass'
        class1_args = {'test_num': '1', 'test_str': 'test1b'}
        _resolver = self.resolver.register(class1_name, class1_args)
        self.assertTrue(class1_name in self.resolver._registered)

    def test_resolver_can_create_registered_objects(self):
        """The IOC resolver can create objects from registered types"""
        class1_name = 'DummyClass'
        class1_args = {'test_num': 1, 'test_str': 'test1b'}
        _resolver = self.resolver.register(class1_name, class1_args)
        dummy = self.resolver.resolve(self.DummyClass)
        real_obj = self.DummyClass(**class1_args)
        self.assertTrue(dummy == real_obj)
        
    def test_resolver_fails_with_wrong_args(self):
        """The resolver fails when missing required args"""
        class1_name = 'DummyClass'
        class1_args = {'XXXX': 1, 'test_str': 'test1b'}
        _resolver = self.resolver.register(class1_name, class1_args)
        self.assertRaises(ResolveException, lambda: self.resolver.resolve(self.DummyClass))
    
    def test_resolver_fails_with_wrong_args(self):
        """The resolver fails with extra args by default"""
        class1_name = 'DummyClass'
        class1_args = {'test_num': 1, 'XXX': 'test1b'}
        _resolver = self.resolver.register(class1_name, class1_args)
        self.assertRaises(ResolveException, lambda: self.resolver.resolve(self.DummyClass, 
                                                            ignore_extra_params=False))
        dummy = self.resolver.resolve(self.DummyClass, ignore_extra_params=True)
        real_obj = self.DummyClass(test_num=1)
        self.assertTrue(dummy == real_obj)
        
    def test_resolver_can_create_registered_objects_with_defaults(self):
        """The resolver works when missing a default arg."""
        class1_name = 'DummyClass'
        class1_args = {'test_num': 1}
        _resolver = self.resolver.register(class1_name, class1_args)
        dummy = self.resolver.resolve(self.DummyClass)
        real_obj = self.DummyClass(**class1_args)
        self.assertTrue(dummy == real_obj)
    
    def test_resolve_fails_when_not_expected(self):
        """The resolver can't create containers that aren't expected"""
        resolve_dummy_obj_fn = lambda: self.resolver.resolve(NotDecoratedClass)
        self.assertRaises(ResolveException, resolve_dummy_obj_fn)
        
    def test_resolver_fails_when_not_registered(self):
        """The resolver must have expected classes be registered first"""
        resolve_dummy_obj_fn = lambda: self.resolver.resolve(self.DummyClass)
        self.assertRaises(ResolveException, resolve_dummy_obj_fn)
     
    def test_resolver_cant_register_undecorated_classes(self):
        """All classes must be registered through controlled hooks"""
        reg_unexpected_obj_fn = lambda: self.resolver.register('BadClass', [])
        self.assertRaises(RegistrationException, reg_unexpected_obj_fn)
        
    def test_resolver_can_register_unsafe_dict(self):
        """Unsafae classes must use unsafe"""
        reg_unexpected_obj_fn = lambda: self.resolver.register(
            'BadClass', {}, unsafe=False)
        reg_unexpected_obj_unsafe_fn = lambda: self.resolver.register(
            'BadClass2', {}, unsafe=True)
        _reg = reg_unexpected_obj_unsafe_fn()
        self.assertRaises(RegistrationException, reg_unexpected_obj_fn)
        self.assertTrue('BadClass2' in _reg._registered)
    
    def test_inline_namedtuples_fails_resolve(self):
        """Inline named tuple requires all required params"""
        # class1_name = 'DummyInlineNamedTuple'
        class1_args = {'basic_int': 1}
        _resolver = self.resolver.register(INLINE_NAMED_TUPLE_CLS_NAME,
                                           class1_args)
        _resolve_fn = lambda: self.resolver.resolve(DummyInlineNamedTuple)
        self.assertRaises(ResolveException, _resolve_fn)
        
    def test_inline_namedtuples_resolve(self):
        # class1_name = 'DummyInlineNamedTuple'
        class1_args = {'basic_int': 1, 'test_str': 'test'}
        _resolver = self.resolver.register(INLINE_NAMED_TUPLE_CLS_NAME,
                                           class1_args)
        dummy = self.resolver.resolve(DummyInlineNamedTuple)
        real_obj = DummyInlineNamedTuple(**class1_args)
        self.assertTrue(dummy == real_obj)
        
    # def test_dataclasses_resolve(self):
    #     class1_name = 'TestDataClass'
    #     class1_args = {'basic_int': 1}
    #     _resolver = self.resolver.register(class1_name, class1_args)
    #     dummy = self.resolver.resolve(DummyDataClass)
    #     real_obj = DummyDataClass(**class1_args)
    #     self.assertTrue(dummy == real_obj)
    
    # def test_typed_namedtuples_resolve(self):
    #     class1_name = 'DummyTypedNamedTuple'
    #     class1_args = {'basic_int': 1}
    #     _resolver = self.resolver.register(class1_name, class1_args)
    #     dummy = self.resolver.resolve(DummyTypedNamedTuple)
    #     real_obj = DummyTypedNamedTuple(**class1_args)
    #     self.assertTrue(dummy == real_obj)
    

if __name__ == '__main__':
    unittest.main()