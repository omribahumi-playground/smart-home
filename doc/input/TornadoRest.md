# TornadoRest

## Dependencies

* Python Tornado

## Description

The TornadoRest module implements a REST API interface using the tornado Python web server.
The module accepts the following parameters:
* path - Base path for the REST API. Could be something like /api or /smarthome (default: /)
* port - HTTP listener port (default: 8080)

## REST API

### Notes
These examples take into consideration that the path is "/" and the port is 8080. Also, the tests are running locally (hence the localhost)

### Urls

GET /status - returns a JSON representing the current state of the relays in the following format: {"relay_id": true/false, "relay_id2": true/false} 
GET /relay/<relay_id> - returns a string - on/off - representing the status of the particular relay 
POST /relay/<relay_id> - on/off/toggle - change the status of the particular relay 

### Examples

```
# Query the server for current relays status
$ curl http://localhost:8080/status
{"DummyOutput1_7": false, "DummyOutput1_6": false, "DummyOutput1_5": false,
"DummyOutput1_4": false, "DummyOutput0_2": false, "DummyOutput0_3": false,
"DummyOutput0_0": false, "DummyOutput0_1": false}

# Switch the "DummyOutput0_1" relay to "on"
$ curl -d on http://localhost:8080/relay/DummyOutput0_1

# Read the status after changing "DummyOutput0_1" to on. Notice "DummyOutput0_1" is now true
$ curl http://localhost:8080/status
{"DummyOutput1_7": false, "DummyOutput1_6": false, "DummyOutput1_5": false,
"DummyOutput1_4": false, "DummyOutput0_2": false, "DummyOutput0_3": false,
"DummyOutput0_0": false, "DummyOutput0_1": true}

# Read the status of "DummyOutput1_5"
$ curl http://localhost:8080/relay/DummyOutput1_5
off
```

## Example configuration

```
input:
  module: TornadoRest
  module_parameters:
    path: /api
    port: 8080
```
