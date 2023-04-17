import argparse, pytest

from argautoopts.frontends.argparse import extend_parser
from argautoopts.decorate import OBJECT_REGISTRATION

@pytest.fixture
def parser():
    parser = argparse.ArgumentParser()
    parser = extend_parser(parser)
    return parser