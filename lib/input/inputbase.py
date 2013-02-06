from lib.exceptions import *

class InputBase(object):
    def __init__(self, output_container):
        self.output_container = output_container

    def run(self):
        raise NotImplementedError('Module %r doesn\'t implement method %s' %
            (self, 'run'))

__all__ = ['InputBase']
