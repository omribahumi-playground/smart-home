from outputbase import *
from serial import Serial

class GenericRelayBoardIoPort(IoPortBase):
    def __init__(self, module, io_port):
        self.module = module
        self.io_port = io_port

    def __repr__(self):
        return '%s(module=%r, io_port=%r, state=%r)' % (
                self.__class__.__name__, self.module, self.io_port, self.get())

    def set(self, new_state):
        self.module.setPhysicalIoPortState(self.io_port, new_state)

    def get(self):
        return self.module.getPhysicalIoPortState(self.io_port)

class GenericRelayBoard(OutputBase):
    def __init__(self, serial, io_ports, size, *args, **kwargs):
        self.serial = Serial(**serial)
        self.io_ports = io_ports
        self.size = size
        OutputBase.__init__(self, *args, **kwargs)
        if min(self.io_ports) <= 0 or max(self.io_ports) > self.size:
            raise InvalidModuleConfigurationException(
                    "Module %r io_ports %r out of range %d - %d" % (
                    self, self.io_ports, 1, self.size))

    def __repr__(self):
        return '%s(io_ports=%r, serial=%r)' % (self.__class__.__name__,
                self.io_ports, self.serial)

    def getIoPort(self, index):
        return GenericRelayBoardIoPort(self, self.io_ports[index])

    def getIoPortsCount(self):
        return len(self.io_ports)

    def setPhysicalIoPortState(self, io_port, new_state):
        self.serial.write("\xff" + chr(io_port) + \
                ("\x01" if new_state else "\x00"))

    def getPhysicalIoPortState(self, io_port):
        return self.getPhysicalIoPortsState()[io_port - 1]

    def getPhysicalIoPortsState(self):
        self.serial.write("\xff" + chr(self.size + 1) + "\x00")
        data = self.serial.read(self.size)
        return [bool(ord(c)) for c in data]

__all__ = ['GenericRelayBoard']
