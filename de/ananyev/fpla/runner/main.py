import argparse

from flask import Flask
# tracerTest must be imported to be started from tracer
# from de.ananyev.fpla.runner.scenario.fb_scenario import FbScenario
# from de.ananyev.fpla.runner.scenario.test_scenario import TestScenario
from flask import request

from de.ananyev.fpla.runner.controller.main_controller import scenario, scheduler, main

PORT = 5000

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Fpla-Runner')
        parser.add_argument('-p', '--port', type=int, dest="PORT")
    except Exception:
        pass


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


app = Flask(__name__)
app.after_request(add_cors_headers)
app.register_blueprint(scenario, url_prefix="/scenario")
app.register_blueprint(scheduler, url_prefix="/schedule")
app.register_blueprint(main)
app.run(port=PORT, debug=True, use_reloader=False)
