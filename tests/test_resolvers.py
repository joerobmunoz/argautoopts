import pytest

from dataclasses import dataclass

from argautoopts.decorate import OBJECT_REGISTRATION
from argautoopts.errors import (
    ResolveException, RegistrationException
)

# Test utilities
from tests.mocks.decorators import (
        dummy_reg,
        dummy2_reg,
        dummydatacls_reg,
        dummyinlinenamedtuple_reg,
        dummytypednamedtuple_reg,
        NotDecoratedClass,
        INLINE_NAMED_TUPLE_CLS_NAME,
)
from tests.mocks.resolve import resolver


def test_supplied_class_is_registered(resolver, dummy_reg):
    """CLI can recognize 2 DI classes at once"""
    class1_name = 'DummyClass'
    class1_args = {'test_num': '1', 'test_str': 'test1b'}
    _resolver = resolver.register(class1_name, class1_args)
    assert(class1_name in resolver._registered)

def test_resolver_can_create_registered_objects(resolver, dummy_reg):
    """The IOC resolver can create objects from registered types"""
    DummyClass = dummy_reg
    class1_name = 'DummyClass'
    class1_args = {'test_num': 1, 'test_str': 'test1b'}
    _resolver = resolver.register(class1_name, class1_args)
    dummy = resolver.resolve(DummyClass)
    real_obj = DummyClass(**class1_args)
    assert(dummy == real_obj)
    
def test_resolver_fails_with_wrong_args(resolver, dummy_reg):
    """The resolver fails when missing required args"""
    DummyClass = dummy_reg
    class1_name = 'DummyClass'
    class1_args = {'XXXX': 1, 'test_str': 'test1b'}
    _resolver = resolver.register(class1_name, class1_args)
    with pytest.raises(ResolveException):
        resolver.resolve(DummyClass)

def test_resolver_fails_with_wrong_args(resolver, dummy_reg):
    DummyClass = dummy_reg
    """The resolver fails with extra args by default"""
    class1_name = 'DummyClass'
    class1_args = {'test_num': 1, 'XXX': 'test1b'}
    _resolver = resolver.register(class1_name, class1_args)
    with pytest.raises(ResolveException):
        resolver.resolve(DummyClass, ignore_extra_params=False)
    dummy = resolver.resolve(DummyClass, ignore_extra_params=True)
    real_obj = DummyClass(test_num=1)
    assert(dummy == real_obj)
    
def test_resolver_can_create_registered_objects_with_defaults(resolver, dummy_reg):
    """The resolver works when missing a default arg."""
    DummyClass = dummy_reg
    class1_name = 'DummyClass'
    class1_args = {'test_num': 1}
    _resolver = resolver.register(class1_name, class1_args)
    dummy = resolver.resolve(DummyClass)
    real_obj = DummyClass(**class1_args)
    assert(dummy == real_obj)

def test_resolve_fails_when_not_expected(resolver):
    """The resolver can't create containers that aren't expected"""
    with pytest.raises(ResolveException):
        resolver.resolve(NotDecoratedClass)
    
def test_resolver_fails_when_not_registered(resolver, dummy_reg):
    """The resolver must have expected classes be registered first"""
    DummyClass = dummy_reg
    with pytest.raises(ResolveException):
        resolver.resolve(DummyClass)
    
def test_resolver_cant_register_undecorated_classes(resolver):
    """All classes must be registered through controlled hooks"""
    with pytest.raises(RegistrationException):
        resolver.register('BadClass', [])
    
def test_resolver_can_register_unsafe_dict(resolver):
    """Unsafae classes must use unsafe"""
    reg_unexpected_obj_fn = lambda: resolver.register(
        'BadClass', {}, unsafe=False)
    reg_unexpected_obj_unsafe_fn = lambda: resolver.register(
        'BadClass2', {}, unsafe=True)
    _reg = reg_unexpected_obj_unsafe_fn()
    assert('BadClass2' in _reg._registered)
    with pytest.raises(RegistrationException):
        
        resolver.register('BadClass', {}, unsafe=False)

def test_inline_namedtuples_fails_resolve(resolver, dummyinlinenamedtuple_reg):
    """Inline named tuple requires all required params"""
    DummyInlineNamedTuple = dummyinlinenamedtuple_reg
    class1_args = {'basic_int': 1}
    _resolver = resolver.register(INLINE_NAMED_TUPLE_CLS_NAME,
                                        class1_args)
    with pytest.raises(ResolveException):
        resolver.resolve(DummyInlineNamedTuple)
    
def test_inline_namedtuples_resolve(resolver, dummyinlinenamedtuple_reg):
    DummyInlineNamedTuple = dummyinlinenamedtuple_reg
    class1_args = {'basic_int': 1, 'test_str': 'test'}
    _resolver = resolver.register(INLINE_NAMED_TUPLE_CLS_NAME,
                                        class1_args)
    dummy = resolver.resolve(DummyInlineNamedTuple)
    real_obj = DummyInlineNamedTuple(**class1_args)
    assert(dummy == real_obj)

if __name__ == '__main__':
    pytest.main()