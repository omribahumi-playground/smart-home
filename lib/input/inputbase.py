from lib.exceptions import *
from abc import ABCMeta, abstractmethod

class InputBase(object):
    """InputModule abstract base class

    The constructor stores the OutputContainer in self.output_container
    """
    __metaclass__ = ABCMeta

    def __init__(self, output_container):
        self.output_container = output_container

    @abstractmethod
    def run(self):
        pass

__all__ = ['InputBase']
