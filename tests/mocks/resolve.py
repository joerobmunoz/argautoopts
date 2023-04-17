import pytest

from argautoopts.decorate import OBJECT_REGISTRATION
from argautoopts.resolver import IOCResolverType

@pytest.fixture
def resolver():
    yield IOCResolverType(OBJECT_REGISTRATION)