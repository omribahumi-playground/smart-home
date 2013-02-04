from inputbase import *
import tornado
import tornado.web
import json

class TornadoRest(InputBase):
    def __init__(self, path='', port=8080, *args, **kwargs):
        InputBase.__init__(self, *args, **kwargs)

        class StatusHandler(tornado.web.RequestHandler):
            def get(handler):
                # this could be done with dictionary comprehension
                # but my server runs Debian 6.x with python 2.6 :P
                ret = {}
                for module in self.output_container.getModules():
                    ret.update(module.getRelaysState())
                handler.write(json.dumps(ret))

        class RelayHandler(tornado.web.RequestHandler):
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

        self.application = tornado.web.Application([
            (path + '/status', StatusHandler),
            (path + '/relay/(?P<id>\S+)', RelayHandler)
        ])
        self.application.listen(port)

    def run(self):
        tornado.ioloop.IOLoop.instance().start()

__all__ = ['TornadoRest']
