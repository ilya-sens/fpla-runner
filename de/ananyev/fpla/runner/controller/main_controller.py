import json
import trace
import sys
import _thread
from de.ananyev.fpla.runner.script.test_script import Script
from klein import run, route, Klein


class MainController():
    app = Klein()
    tracer = trace.Trace(
        ignoredirs=[sys.prefix, sys.exec_prefix],
        trace=1,
        count=0)

    def __init__(self):

        self._items = {}

    @app.route('/')
    def items(self, request):
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self._items)

    @app.route('/<string:name>', methods=['PUT'])
    def save_item(self, request, name):
        request.setHeader('Content-Type', 'application/json')
        body = json.loads(request.content.read())
        self._items[name] = body
        return json.dumps({'success': True})

    @app.route('/<string:name>', methods=['GET'])
    def get_item(self, request, name):
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self._items.get(name))

    @app.route('/run/<string:name>', methods=['GET'])
    def run_script(self, request, name):
        request.setHeader('Content-Type', 'application/json')
        _thread.start_new(self.tracer.run, ('Script().run()',))
        return
