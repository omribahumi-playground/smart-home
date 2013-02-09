import requests
from outputbase import OutputBase, IoPortBase

class RestOutputIoPort(IoPortBase):
    pass

class RestOutput(OutputBase):
    def __init__(self, baseurl, *args, **kwargs):
        OutputBase.__init__(self, *args, **kwargs)
        self.baseurl = baseurl
        physicalPorts = self.getPhysicalIoPortsState()
        for relay in self.relays:
            if not relay in physicalPorts:
                raise InvalidModuleConfigurationException(
                    "%r Relay %r does not exist in url %r",
                    self.__class__.__name,
                    relay, self.baseUrl)

    def getIoPort(self, io_port_id):
        return TornadoRestIoPort(self, io_port_id)

    def setPhysicalIoPortState(self, io_port_id, new_state):
        request = requests.post(self.baseurl + '/relay/' + io_port_id,
                                'on' if new_state else 'off')
        assert(request.status_code == 200)

    def getPhysicalIoPortsState(self):
        request = requests.get(self.baseurl + '/status')
        assert(request.status_code == 200)
        return request.json()

__all__ = ['RestOutput']
