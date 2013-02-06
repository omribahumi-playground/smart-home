#!/usr/bin/python
import yaml
import pprint
import sys

import lib.output
import lib.input
from lib import *

def main():
    config = yaml.load(open('config.yml'))
    pprint.pprint(config)

    output_container = OutputContainer()
    for module in config['output']:
        output_class = getattr(lib.output, module['module'], None)
        if not output_class:
            print >>sys.stderr, 'Unable to find module %r' % (module['module'])
            sys.exit(1)

        output_instance = output_class(relays=module['relays'],
            **(module.get('module_parameters', {})))
        output_container.addModule(output_instance, module['relays'])

    module = config['input']
    input_class = getattr(lib.input, module['module'], None)
    if not input_class:
        print >>sys.stderr, 'Unable to find module %r' % (module['module'])
        sys.exit(1)

    input_instance = input_class(output_container=output_container,
        **module.get('module_parameters', {}))
    input_instance.run()

if __name__ == '__main__':
    main()
