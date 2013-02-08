"""Smart-Home project Exceptions"""

class SmartHomeException(Exception):
    """Exceptions base class"""
    pass

class RelayAlreadyHandledException(SmartHomeException):
    def __init__(self, relay_id, module):
        ModuleContainerException.__init__(
                self,
                'Relay %d is already handled by module %r',
                relay_id, module)

class InvalidModuleConfigurationException(SmartHomeException):
    pass
