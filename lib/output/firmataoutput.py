from outputbase import OutputBase, IoPortBase
from lib.exceptions import InvalidModuleConfigurationException
import pyfirmata

class FirmataOutputIoPort(IoPortBase):
    pass

class FirmataOutput(OutputBase):
    def __init__(self, port, board_type='arduino', baud_rate=57600, reverse=False,
                 *args, **kwargs):
        OutputBase.__init__(self, *args, **kwargs)
        self.firmata = pyfirmata.Board(port, pyfirmata.BOARDS[board_type], baud_rate)
        # for using relay boards where HIGH means ON, LOW means OFF
        self.reverse = reverse

        # analog ports will be parsed as strings from the YAML config file
        # digital ports can be either integers or strings, we don't care.
        analog_ports = [io_port_id for io_port_id in self.relays.keys()
                if type(io_port_id) == str and
                io_port_id.lower().startswith('a')]
        digital_ports = list(set(self.relays.keys()) - set(analog_ports))
        analog_ports = [int(io_port_id[1:]) for io_port_id in analog_ports]
        digital_ports = map(int, digital_ports)

        outofrange_digital_ports = [port for port in digital_ports
            if port < 0 or port >= len(self.firmata.digital)]
        if outofrange_digital_ports:
            raise InvalidModuleConfigurationException(
                "Module %s digital io_ports %s out of range %d - %d" % (
                self.__class__.__name__,
                ', '.join(map(str, outofrange_digital_ports)),
                0, len(self.firmata.digital) - 1))

        outofrange_analog_ports = ['A' + str(port)
            for port in analog_ports
            if port < 0 or port >= len(self.firmata.analog)]
        if outofrange_analog_ports:
            raise InvalidModuleConfigurationException(
                "Module %s analog io_ports %s out of range A%d - A%d" % (
                self.__class__.__name__,
                ', '.join(outofrange_analog_ports),
                0, len(self.firmata.analog) - 1))

        # set all analog ports to output
        for analog_port in analog_ports:
            port = self.firmata.analog[analog_port]
            port.mode = pyfirmata.OUTPUT
            port.write(0)

        # if we're using reversed logic, set all outputs to HIGH (relays off)
        if self.reverse:
            for analog_port in analog_ports:
                self.firmata.analog[analog_port].write(1)
            for digital_port in digital_ports:
                self.firmata.digital[digital_port].write(1)
    def __repr__(self):
        return '%s(relays=%r, firmata=%r)' % (self.__class__.__name__,
                self.relays, self.firmata)

    def getIoPort(self, io_port_id):
        return FirmataOutputIoPort(self, io_port_id)

    def setPhysicalIoPortState(self, io_port_id, new_state):
        # flip new_state if we're using reversed logic
        new_state = self.reverse ^ new_state
        if type(io_port_id) is str and io_port_id.lower().startswith('a'):
            # analog port
            self.firmata.analog[int(io_port_id[1:])].write(int(new_state))
        else:
            # digital port
            self.firmata.digital[io_port_id].write(int(new_state))

    def getPhysicalIoPortsState(self):
        # digital ports
        ret = {port_id: self.reverse ^ bool(port.value)
               for port_id, port in enumerate(self.firmata.digital)}
        # analog ports
        ret.update({'A' + str(port_id): self.reverse ^ bool(port.value)
                    for port_id, port in enumerate(self.firmata.analog)})

        return ret

__all__ = ['FirmataOutput']
