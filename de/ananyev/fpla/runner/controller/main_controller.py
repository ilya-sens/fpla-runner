import importlib
import json
import os
import sys
import trace
import uuid

from flask import Blueprint, request

scenario = Blueprint('scenario', __name__)
threads = {}
tracer = trace.Trace(
    ignoredirs=[sys.prefix, sys.exec_prefix],
    trace=1,
    count=0)

# scenario
@scenario.route('/run/<string:name>', methods=['GET'])
def run_scenario(name):
    mod = importlib.import_module('de.ananyev.fpla.runner.scenario.' + name)
    scenario = mod.Scenario()
    scenario.start()
    generated_uuid = uuid.uuid4().__str__()
    threads[generated_uuid] = scenario
    return json.dumps({'success': True, 'thread_id': generated_uuid})

@scenario.route('/status/<string:thread_uuid>', methods=['GET'])
def get_status(thread_uuid):
    return json.dumps({'line': threads[thread_uuid].status, 'exceptions': threads[thread_uuid].exceptions})

@scenario.route('/upload', methods=['POST'])
def upload_scenario():
    scenario_file_json = request.get_json()
    file = open(os.path.join(os.path.dirname(sys.argv[0]), 'scenario', scenario_file_json['fileName']), "w")
    file.write(scenario_file_json['sequence'])
    file.close()

    return json.dumps({'success': True, 'filename': scenario_file_json['fileName']})
