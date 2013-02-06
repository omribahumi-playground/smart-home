from exceptions import *
from output import OutputBase

class OutputContainer(object):
    def __init__(self):
        self.relay_id_to_module = {}
        self.module_to_relay_ids = {}

    def addModule(self, module, relays):
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
        return tuple(self.module_to_relay_ids.keys())

    def getRelayIdsForModule(self, module):
        return tuple(self.module_to_relay_ids[module])

    def getRelayIds(self):
        return self.relay_id_to_module.keys()

    def getModuleForRelayId(self, relay_id):
        return self.relay_id_to_module[relay_id] \
                if relay_id in self.relay_id_to_module else None

    def getRelayForRelayId(self, relay_id):
        return self.getModuleForRelayId(relay_id).getRelay(relay_id) \
                if self.getModuleForRelayId(relay_id) else None

__all__ = ['OutputContainer']
