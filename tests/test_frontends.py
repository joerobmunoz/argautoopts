import unittest

from argautoopts.decorate import OBJECT_REGISTRATION
from tests.mocks.decorators import DummyClass

class TestDecoratedClassesShouldRegister(unittest.TestCase):
    def setUp(self):
        self.registered_dummy_class = OBJECT_REGISTRATION[DummyClass.__name__]
        
    def test_cli_requires_dummy(self):
        """When configured as a CLI, it should show Dummy Class options
        """
        pass
        
    def test_config_requires_dummy(self):
        """When configured as a config file input, it should show Dummy Class options
        """
        pass
    
if __name__ == '__main__':
    unittest.main()