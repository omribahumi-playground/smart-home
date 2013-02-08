from exceptions import *
from output import OutputBase

class OutputContainer(object):
    """Output modules container

    Contains the output modules and manages the relays inside them.
    Lets you search for relays inside the container.

    main.py creates a OutputContainer instance and initializes the modules
    inside it. In turn, this instance is passed to the InputModule's
    constructor for OutputModules and Relays management.
    """
    def __init__(self):
        self.relay_id_to_module = {}
        self.module_to_relay_ids = {}

    def addModule(self, module, relays):
        """Add a module to the container for management.

        This method is invoked by main.py for every module in the configuration file
        """
        if not isinstance(module, OutputBase):
            raise TypeError('%r is not a subclass of %r' %
                (module, OutputBase))

        self.module_to_relay_ids[module] = []
        for io_port, relay_id in relays.iteritems():
            if relay_id in self.relay_id_to_module:
                raise RelayAlreadyHandledException(relay_id,
                        self.relay_id_to_module[relay_id])
            else:
                self.relay_id_to_module[relay_id] = module
                self.module_to_relay_ids[module].append(relay_id)

    def getModules(self):
        """Get the modules managed by this OutputContainer"""
        return tuple(self.module_to_relay_ids.keys())

    def getRelayIdsForModule(self, module):
        """Get the associated relay ids for module"""
        return tuple(self.module_to_relay_ids[module])

    def getRelayIds(self):
        """Get all the relay ids associated with this OutputContainer"""
        return self.relay_id_to_module.keys()

    def getModuleForRelayId(self, relay_id):
        """Fetch the module that handles relay_id"""
        return self.relay_id_to_module[relay_id] \
                if relay_id in self.relay_id_to_module else None

    def getRelayForRelayId(self, relay_id):
        """Get the Relay instance for relay_id"""
        return self.getModuleForRelayId(relay_id).getRelay(relay_id) \
                if self.getModuleForRelayId(relay_id) else None

__all__ = ['OutputContainer']
