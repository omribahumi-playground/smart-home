#!/usr/bin/python
import yaml
import pprint
import sys

import lib.output
from lib import *

YamlExtensions.load()

def main():
    config = yaml.load(open('config.yml'))
    pprint.pprint(config)

    output_modules = OutputContainer()
    for module in config['output']:
        if not hasattr(lib.output, module['module']):
            print >>sys.stderr, 'Unable to find module %r' % (module['module'])
            sys.exit(1)
        else:
            module_class = getattr(lib.output, module['module'])
            module_instance = module_class(
                    relays=module['relays'], **module['module_parameters'])
            output_modules.addModule(module_instance, module['relays'])

    for relay_id in output_modules.getRelayIds():
        print relay_id, output_modules.getRelay(relay_id)

if __name__ == '__main__':
    main()
