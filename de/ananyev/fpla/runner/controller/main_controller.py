import importlib
import json
import sys
import trace
import uuid

from klein import Klein


class MainController():
    threads = {}
    app = Klein()
    tracer = trace.Trace(
        ignoredirs=[sys.prefix, sys.exec_prefix],
        trace=1,
        count=0)

    # scenario
    @app.route('/scenario/run/<string:name>', methods=['GET'])
    def run_scenario(self, request, name):
        request.setHeader('Content-Type', 'application/json')
        mod = importlib.import_module('de.ananyev.fpla.runner.scenario.' + name)
        scenario = mod.Scenario()
        scenario.start()
        generated_uuid = uuid.uuid4().__str__()
        self.threads[generated_uuid] = scenario
        return json.dumps({'success': True, 'thread_id': generated_uuid})

    @app.route('/scenario/status/<string:thread_uuid>', methods=['GET'])
    def get_status(self, request, thread_uuid):
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self.threads[thread_uuid].status)
