# Smart home project

## Introduction

I've been playing around with smart home projects for a while now.
There are many ways to implement the "hardware" side - starting from pre-made
boards and ending with DIY projects with Arduino or Raspberry PI.
The logic is pretty much the same - relay module controlled from a computer
(or a phone, for that matter)

The idea of this project is giving you an API to control relay array
constructed with relay controllers from various vendors, including ones you
build on your own using RPI or Arduino, giving you a unified API to rule them
all!

## Dependencies
* Python YAML

Please note that several modules may have their own dependencies.
Make sure you read the module documentation for each and every module you're using.

## Modules

The project is still under development.
There are more modules to come!

### Input modules
* [TornadoRest](doc/input/TornadoRest.md) - Export project's functionality through REST API

### Output Modules
* [GenericRelayBoard](doc/output/GenericRelayBoard.md) - Control a generic relay board (purchased on EBay, more information on module doc)
* [DummyOutput](doc/output/DummyOutput.md) - Dummy relay controlling module for playing with the system and/or development purposes.

## Configuration

### Input configuration section

The input configuration section accepts one input module (might be changed in
the future). This module receives commands through a particular transport
layer (REST, Thrift, etc.) and executes them on the relay array.

Example input configuration section:
```yaml
input:
  module: TornadoRest
  module_parameters:
    path: /api
    port: 8888
```

### Output configuration section

The output configuration section accepts a list of modules with their corresponding parameters

Example output configuration section:
```yaml
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
  - module: DummyOutput
    relays:
      0: DummyOutput0_0
      1: DummyOutput0_1
      2: DummyOutput0_2
      3: DummyOutput0_3
  - module: DummyOutput
    relays:
      4: DummyOutput1_4
      5: DummyOutput1_5
      6: DummyOutput1_6
      7: DummyOutput1_7
```
