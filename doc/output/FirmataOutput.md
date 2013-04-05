# FirmataOutput

## Dependencies

* Python serial
* pyFirmata

## Description

The FirmataOutput module lets you interface with micro controllers supporting the Firmata protocol (such as the Arduino).  
With complementary relay board (such as the ones sold on eBay), one can hook up the micro controller's digital/analog outputs to the board, controlling it via the firmata protocol.  

The module accepts the following parameters:
* reverse - true or false(default) - reverse the output logic. By default, this module sets HIGH for turning the relay ON, and LOW for turning it off. Specify true here to make it the other way around.
* board_type - 'arduino_mega' or 'arduino' (default)
* port - serial device to access the micro controller via Firmata interface
* baud_rate - integer (default: 57600) - serial port baud rate
* relays - key: value - represents the digital/analog output port to relay name - use A5 for analog 5, 10 for digital 10

## Example configuration

```
output:
  - module: FirmataOutput
    relays:
      2: relay_1
      3: relay_2
      4: relay_3
      5: relay_4
      6: relay_5
      7: relay_6
      8: relay_7
      9: relay_8
      10: relay_9
      11: relay_10
      12: relay_11
      13: relay_12
      A0: relay_13
      A1: relay_14
      A2: relay_15
      A3: relay_16
    module_parameters:
      reverse: true
      board_type: 'arduino_mega'
      port: /dev/ttyACM0
      baud_rate: 57600
```
