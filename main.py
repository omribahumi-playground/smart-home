#!/usr/bin/python
import yaml
import pprint
import sys
import argparse
import os

import lib.output
import lib.input
from lib import *

def main():
    parser = argparse.ArgumentParser(description='Smart-Home project')
    parser.add_argument('--fork', action='store_true',
            help='Fork into the background')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--pid', metavar='file', type=argparse.FileType('w'),
            help='pid file')
    parser.add_argument('--config', default='config.yml',
            type=argparse.FileType('r'),
            help='Configuration file in YAML format (default: config.yml)')

    args = parser.parse_args()

    config = yaml.load(args.config)

    if args.debug:
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

    if args.fork:
        print 'Forking into the background...'

        pid = os.fork()
        if pid == -1:
            print >>sys.stderr, 'os.fork() failed'
            sys.exit(1)
        elif pid > 0:
            # parent process
            sys.exit(0)
        else:
            # child process
            if args.pid:
                args.pid.write(str(os.getpid()))
                args.pid.close()

            print 'Child process: %d' % (os.getpid(),)

            sys.stdout = sys.stderr = open('/dev/null', 'w')

            # using /dev/null for stdin is a bad idea. if there's an attempt to
            # read from stdin, the desired behavior is to throw an exception,
            # not to block.
            sys.stdin.close()

            # detach from parent process
            os.chdir('/')
            os.setsid()
            os.umask(0)

    input_instance.run()

if __name__ == '__main__':
    main()
