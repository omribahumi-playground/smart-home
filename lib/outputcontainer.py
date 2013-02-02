from exceptions import *
from output import *

class OutputContainer(object):
    def __init__(self):
        self.modules = []
        self.relay_id_to_module = {}

    def addModule(self, module, relay_ids):
        if not isinstance(module, OutputBase):
            raise InvalidSubclassException(module, OutputBase)
        else:
            self.modules.append(module)
            for relay_id in relay_ids:
                if relay_id in self.relay_id_to_module:
                    raise RelayAlreadyHandledException(relay_id,
                            self.relay_id_to_module[relay_id])
                else:
                    self.relay_id_to_module[relay_id] = module

    def getRelayIds(self):
        return self.relay_id_to_module.keys()

    def getModule(self, relay_id):
        return self.relay_id_to_module[relay_id] \
                if relay_id in self.relay_id_to_module else None

    def getRelay(self, relay_id):
        return self.getModule(relay_id).getRelay(relay_id) \
                if self.getModule(relay_id) else None

__all__ = ['OutputContainer']
