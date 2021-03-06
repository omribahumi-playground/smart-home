from inputbase import *
import tornado
import tornado.web
import json
import os

class TornadoRest(InputBase):
    def __init__(self, api={}, static=None, port=8080,
                 *args, **kwargs):
        InputBase.__init__(self, *args, **kwargs)

        class StatusHandler(tornado.web.RequestHandler):
            def compute_etag(handler):
                return None

            def get(handler):
                handler.set_header('Content-Type', 'application/json')

                # this could be done with dictionary comprehension
                # but my server runs Debian 6.x with python 2.6 :P
                ret = {}
                for module in self.output_container.getModules():
                    ret.update(module.getRelaysState())
                handler.write(json.dumps(ret))

        class RelayHandler(tornado.web.RequestHandler):
            def compute_etag(handler):
                return None

            def get(handler, id=''):
                relay = self.output_container.getRelayForRelayId(id)
                if not relay:
                    handler.send_error(404)
                else:
                    handler.write('on' if relay.get() else 'off')

            def post(handler, id=''):
                mapping = {'on': True, 'off': False, 'toggle': None}
                new_state = handler.request.body

                if not new_state in mapping:
                    handler.send_error(400)
                else:
                    relay = self.output_container.getRelayForRelayId(id)
                    if not relay:
                        handler.send_error(404)
                    elif new_state == 'toggle':
                        relay.set(not relay.get())
                    else:
                        relay.set(mapping[new_state])

        handlers = []
        if api:
            virtual_path = api.get('virtual_path', '')
            handlers.extend([
                (virtual_path + '/status', StatusHandler),
                (virtual_path + '/relay/(?P<id>\S+)', RelayHandler)
            ])

        if static:
            handlers.extend([(
                static.get('virtual_path', '') + '/?(.*)',
                tornado.web.StaticFileHandler,
                # when forking, we're calling os.chdir('/') which can
                # screw things up when using relative paths
                {'path' :
                        os.path.abspath(static.get('physical_path', 'static')),
                 'default_filename' :
                        static.get('directory_index', 'index.html')}
            )])

        self.application = tornado.web.Application(handlers)
        self.application.listen(port)

    def run(self):
        tornado.ioloop.IOLoop.instance().start()

__all__ = ['TornadoRest']
