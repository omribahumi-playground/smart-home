from outputbase import *

class DummyOutputIoPort(IoPortBase):
    pass

class DummyOutput(OutputBase):
    def __init__(self, *args, **kwargs):
        OutputBase.__init__(self, *args, **kwargs)
        self.io_ports_state = dict(
                zip(self.relays.keys(), [False]*len(self.relays)))

    def getIoPort(self, io_port):
        return DummyOutputIoPort(self, io_port)

    def setPhysicalIoPortState(self, io_port, new_state):
        print '%s %s : %s -> %s' % (self.__class__.__name__, io_port,
                self.io_ports_state[io_port], new_state)
        self.io_ports_state[io_port] = new_state

    def getPhysicalIoPortsState(self):
        return dict(self.io_ports_state)

__all__ = ['DummyOutput']
