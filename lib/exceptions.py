class SmartHomeException(Exception):
    pass

class InvalidSubclassException(SmartHomeException):
    def __init__(self, cls, base):
        SmartHomeException.__init__(
                self,
                '%r is not a subclass of %r',
                cls, base)

class MethodMissingException(SmartHomeException):
    def __init__(self, module, method):
        SmartHomeException.__init__(
                self,
                'Module %r doesn\'t implement method %s' %
                (module, method))

class RelayAlreadyHandledException(SmartHomeException):
    def __init__(self, relay_id, module):
        ModuleContainerException.__init__(
                self,
                'Relay %d is already handled by module %r',
                relay_id, module)

class InvalidModuleConfigurationException(SmartHomeException):
    pass
