from argautoopts.decorate import register_opts

@register_opts
class DummyClass(object):
    def __init__(self, test_num: int, test_str:str='test'):
        self.test_num = test_num
        self.test_str = test_str