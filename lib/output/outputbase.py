from lib.exceptions import *

class IoPortBase(object):
    def get(self):
        raise MethodMissingException(self, 'get')

    def set(self, new_state):
        raise MethodMissingException(self, 'set')

class Relay(object):
    def __init__(self, relay_id, io_port):
        if not isinstance(io_port, IoPortBase):
            raise InvalidSubclassException(io_port, IoPortBase)
        else:
            self.io_port = io_port
            self.relay_id = relay_id

            # expose io_port get, set methods
            self.get = io_port.get
            self.set = io_port.set

    def __repr__(self):
        return '%s(relay_id=%r, io_port=%r)' % (self.__class__.__name__,
                self.relay_id, self.io_port)

class OutputBase(object):
    def __init__(self, relays):
        self.relays = relays
        if len(self.relays) != self.getIoPortsCount():
            raise InvalidModuleConfigurationException(
                    'Output module %r has %d relays with %d IO ports' %
                    (self, len(self.relays), self.getIoPortsCount()))

    def getRelay(self, relay_id):
        io_port_index = self.relays.index(relay_id)
        return Relay(relay_id, self.getIoPort(io_port_index))

    def getIoPort(self, index):
        raise MethodMissingException(self, 'getIoPort')

    def getIoPortsCount(self):
        raise MethodMissingException(self, 'getIoPortsCount')

__all__ = ['IoPortBase', 'Relay', 'OutputBase']
