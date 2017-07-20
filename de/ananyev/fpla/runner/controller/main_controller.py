import json
import sys
import trace

from klein import Klein

from de.ananyev.fpla.runner.scenario.test_scenario import TestScenario


class MainController():
    threads = []
    app = Klein()
    tracer = trace.Trace(
        ignoredirs=[sys.prefix, sys.exec_prefix],
        trace=1,
        count=0)

    # scenario
    @app.route('/scenario/run/<string:name>', methods=['GET'])
    def run_scenario(self, request, name):
        request.setHeader('Content-Type', 'application/json')
        test_scenario = TestScenario()
        test_scenario.start()
        self.threads.append(test_scenario)
        return json.dumps({'success': True})

    @app.route('/scenario/status/<string:name>', methods=['GET'])
    def get_status(self, request, name):
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self.threads[len(self.threads) - 1].status)
