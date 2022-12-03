import unittest

# Example invocation:
# 1. Decorate class
# 2. Class args show as cli options
    # 2a. Exploit type hint information
    # 2b. Exploit defaults

class TestDecoratedClassShowsAsCLIOpts(unittest.TestCase):
    def test_class_args_registered(self):
        from .mocks.decorators import DummyClass
        
        pass
        
    def test_namedtuple(self):
        pass
    
    def test_class(self):
        pass
    
    def test_dataclass(self):
        pass
        

if __name__ == '__main__':
    unittest.main()
