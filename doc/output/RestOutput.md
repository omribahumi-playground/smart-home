# RestOutput

## Dependencies

* Python requests ([python-requests.org](http://python-requests.org))

## Description

The RestOutput module lets connect smart-home instances together. It interacts with REST API input modules, such as TornadoRest.
The module accepts the following parameters:
* baseurl - Base URL for REST API calls. Could be something like http://192.168.0.1:8888/api

## Example configuration

```
output:
  - module: RestOutput
    relays:
      remote_relay_name: local_relay_name
      window_up: remote_window_up
      window_down: remote_window_down
      lamp: remote_lamp
    module_parameters:
      baseurl: http://192.168.0.1:8888/api
```
