from abc import ABCMeta, abstractmethod

class IoPortBase(object):
    """Base class for IO ports.

    You should subclass this in your module for your IO ports,
    even if you don't override any of these methods.
    """
    def __init__(self, module, io_port_id):
        self.module = module
        self.io_port_id = io_port_id

    def __repr__(self):
        return '%s(module=%r, io_port_id=%r, state=%r)' % (
                self.__class__.__name__, self.module, self.io_port_id, self.get())

    def set(self, new_state):
        self.module.setPhysicalIoPortState(self.io_port_id, new_state)

    def get(self):
        return self.module.getPhysicalIoPortState(self.io_port_id)

class Relay(object):
    """Relay object wrapping the IO port carrying the relay_id with it"""
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
    """OutputModule abstract base class

    Stores the relay_ids associated with this module in self.relays
    Implements base __repr__(), getRelay(), getRelayState(), getIoPortsCount(),
    getPhysicalIoPortState()
    """
    __metaclass__ = ABCMeta

    def __init__(self, relays):
        """Base constructor. Stores relays in self.relays"""
        self.relays = relays

    def __repr__(self):
        """Base __repr__() function. Returns the module name with the relays
        associated with it
        """
        return '%s(relays=%r)' % (self.__class__.__name__, self.relays)

    def getRelay(self, relay_id):
        """Base getRelay(). Wraps the IO port associated of this relay_id
        with Relay() instance.
        """
        return Relay(relay_id, self.getIoPort(
            dict(zip(self.relays.values(), self.relays.keys()))[relay_id]))

    def getRelaysState(self):
        """Base getRelaysState()

        Queries physical IO ports state and iterates through self.relays
        Returning a dictionary:
        {
            relay_id: True,             # relay_id is on
            another_relay_id: False,    # another_relay_id is off
            ...
        }
        """
        ret = {}
        states = self.getPhysicalIoPortsState()
        for io_port_id, name in self.relays.iteritems():
            ret[name] = states[io_port_id]
        return ret

    def getIoPortsCount(self):
        """Base getIoPortsCount(). Returns the length of self.relays"""
        return len(self.relays)

    def getPhysicalIoPortState(self, io_port_id):
        """Base getPhysicalIoPortState().
        Returns the state of this io_port_id inside self.getPhysicalIoPortsState()
        """
        return self.getPhysicalIoPortsState()[io_port_id]

    @abstractmethod
    def setPhysicalIoPortState(self, io_port_id, new_state):
        """Abstract method.
        This method should change the io_port_id to new_state (boolean)
        """
        pass

    @abstractmethod
    def getIoPort(self, io_port_id):
        """Abstract method.
        This method should return the IoPortBase instance for the given
        io_port_id
        """
        pass

    @abstractmethod
    def getPhysicalIoPortsState(self):
        """Abstract method.
        This method should return the module's physcal IO ports state
        in a dictionary form:

        {
            io_port_id: True,          # io_port is on
            another_io_port_id: False, # another_io_port is off
            ...
        }
        """
        pass

__all__ = ['IoPortBase', 'Relay', 'OutputBase']
