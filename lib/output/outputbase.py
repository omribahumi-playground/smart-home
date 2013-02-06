class IoPortBase(object):
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

class Relay(object):
    def __init__(self, relay_id, io_port):
        if not isinstance(io_port, IoPortBase):
            raise TypeError('%r is not a subclass of %r' %
                (io_port, IoPortBase))

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

    def __repr__(self):
        return '%s(relays=%r)' % (self.__class__.__name__, self.relays)

    def getRelay(self, relay_id):
        return Relay(relay_id, self.getIoPort(
            dict(zip(self.relays.values(), self.relays.keys()))[relay_id]))

    def getRelaysState(self):
        ret = {}
        states = self.getPhysicalIoPortsState()
        for io_port, name in self.relays.iteritems():
            ret[name] = states[io_port]
        return ret

    def getIoPort(self, io_port):
        raise NotImplementedError('Module %r doesn\'t implement method %s' %
            (self, 'getIoPort'))

    def getIoPortsCount(self):
        return len(self.relays)

    def setPhysicalIoPortState(self, io_port, new_state):
        raise NotImplementedError('Module %r doesn\'t implement method %s' %
             (self, 'setPhysicalIoPortState'))

    def getPhysicalIoPortState(self, io_port):
        return self.getPhysicalIoPortsState()[io_port]

    def getPhysicalIoPortsState(self):
        raise NotImplementedError('Module %r doesn\'t implement method %s' %
            (self, 'getPhysicalIoPortsState'))


__all__ = ['IoPortBase', 'Relay', 'OutputBase']
