# GenericRelayBoard

## Dependencies

* Python serial

## Description

The GenericRelayBoard lets you interface with relays sold on EBay (on probably some other places on the internet)  
The relay board usually comes with a DB9 connector (RS232 connector) or a USB connector. Either way, it interfaces the computer using a serial port (/dev/ttyS when using DB9, /dev/ttyUSB when using USB)  
For configuring this module you mush know the serial port configurations required for your module.  

The protocol used between the module and the relay board is simple:  
\x00\x01\x00 - turn relay 1 off  
\x00\x01\x01 - turn relay 1 on  
\x00\x08\x00 - turn relay 8 off  
\x00\x08\x01 - turn relay 8 on  
\x00\x09\x00 - query the board for current relays status (this was undocumented on the EBay page I purchased my board at. Also note that \x09 is number_of_board_relays+1, hence the board_size module parameter is important)  

The module accepts the following parameters:
* serial - python serial.Serial constructor parameters
* board_size - number of relays on the board

## Example configuration

```
output:
  - module: GenericRelayBoard
    relays:
      2: window_switch_bypass
      3: window_down
      4: window_up
      5: lamp
      6: uv_lamp
    module_parameters:
      serial:
        port: /dev/ttyS0
        baudrate: 9600
      board_size: 8
```
