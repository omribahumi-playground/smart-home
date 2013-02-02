from lib.exceptions import *

class InputBase(object):
    def __init__(self, output_container):
        self.output_container = output_container

    def run(self):
        raise MethodMissingException(self, 'run')

__all__ = ['InputBase']
