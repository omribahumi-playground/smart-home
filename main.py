#!/usr/bin/python
import yaml
import pprint
import sys

import lib.output
import lib.input
from lib import *

YamlExtensions.load()

def main():
    config = yaml.load(open('config.yml'))
    pprint.pprint(config)

    output_container = OutputContainer()
    for module in config['output']:
        if not hasattr(lib.output, module['module']):
            print >>sys.stderr, 'Unable to find module %r' % (module['module'])
            sys.exit(1)
        else:
            module_class = getattr(lib.output, module['module'])
            module_instance = module_class(
                    relays=module['relays'], **module['module_parameters'])
            output_container.addModule(module_instance, module['relays'])

    module = config['input']
    if not hasattr(lib.input, module['module']):
        print >>sys.stderr, 'Unable to find module %r' % (module['module'])
        sys.exit(1)
    else:
        input_class = getattr(lib.input, module['module'])
        input_instance = input_class(
                output_container=output_container,
                **(module['module_parameters']
                    if 'module_parameters' in module else {}))
        input_instance.run()

if __name__ == '__main__':
    main()
