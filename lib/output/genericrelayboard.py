from outputbase import OutputBase, IoPortBase
from serial import Serial

class GenericRelayBoardIoPort(IoPortBase):
    pass

class GenericRelayBoard(OutputBase):
    def __init__(self, serial, board_size, *args, **kwargs):
        OutputBase.__init__(self, *args, **kwargs)
        self.serial = Serial(**serial)
        self.board_size = board_size
        if min(self.relays.keys()) <= 0 or max(self.relays.keys()) > self.board_size:
            raise InvalidModuleConfigurationException(
                    "Module %r io_ports %r out of range %d - %d" % (
                    self, self.io_ports, 1, self.board_size))

    def __repr__(self):
        return '%s(board_size=%d, relays=%r, serial=%r)' % (self.__class__.__name__,
                self.board_size, self.relays, self.serial)

    def getIoPort(self, io_port_id):
        return GenericRelayBoardIoPort(self, io_port_id)

    def setPhysicalIoPortState(self, io_port_id, new_state):
        self.serial.write("\xff" + chr(io_port_id) + \
                ("\x01" if new_state else "\x00"))

    def getPhysicalIoPortsState(self):
        self.serial.write("\xff" + chr(self.board_size + 1) + "\x00")
        data = [bool(ord(c)) for c in self.serial.read(self.board_size)]
        ret = dict(self.relays)
        for k in ret:
            ret[k] = data[k-1]
        return ret

__all__ = ['GenericRelayBoard']
