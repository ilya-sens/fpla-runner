import importlib
import json
import os
import sys
import trace
import uuid

from flask import Blueprint, request

scenario = Blueprint('scenario', __name__)
scheduler = Blueprint('schedule', __name__)
main = Blueprint('main', __name__)

threads = []
tracer = trace.Trace(
    ignoredirs=[sys.prefix, sys.exec_prefix],
    trace=1,
    count=0)


# main
@main.route('/status/<string:thread_uuid>', methods=['GET'])
def get_status(thread_uuid):
    for thread in threads:
        if thread_uuid == thread['runningThread']:
            result = {'success': True}
            if 'scenarioModule' in thread:
                result['scenarioLine'] = thread['scenarioModule'].status
                result['scenarioExceptions'] = thread['scenarioModule'].exceptions
                result['scenarioId'] = thread['scenarioModule'].scenario_id
            if 'schedulerModule' in thread:
                result['scheduleLine'] = thread['schedulerModule'].status
                result['scheduleExceptions'] = thread['schedulerModule'].exceptions
                result['scheduleId'] = thread['schedulerModule'].scheduler_id
            return json.dumps(result)
    return json.dumps({'success': False, 'message': 'Thread not found'})


@main.route('/status', methods=['GET'])
def get_running_scripts():
    results = []
    for thread in threads:
        result = {'success': True}
        if 'scenarioModule' in thread:
            result['scenarioLine'] = thread['scenarioModule'].status
            result['scenarioExceptions'] = thread['scenarioModule'].exceptions
            result['scenarioId'] = thread['scenarioModule'].scenario_id
        if 'schedulerModule' in thread:
            result['scheduleLine'] = thread['schedulerModule'].status
            result['scheduleExceptions'] = thread['schedulerModule'].exceptions
            result['scheduleId'] = thread['schedulerModule'].scheduler_id
        results.append(result)
    return json.dumps(results)


@scenario.route('/stop/<string:thread_uuid>', methods=['GET'])
def stop_scenario(thread_uuid):
    for thread in threads:
        if thread_uuid == thread['runningThread']:
            thread['scenarioModule'].stop = True
            threads.remove(thread)
            return json.dumps({
                'success': True,
            })


# scenario
@scenario.route('/run', methods=['POST'])
def run_scenario():
    try:
        scenario_model = request.get_json()
        name = scenario_model['fileName'].split('.')[0]
        mod = importlib.import_module('de.ananyev.fpla.runner.scenario.' + name)
        scenario_module = mod.Scenario()
        scenario_module.start()
        generated_uuid = uuid.uuid4().__str__()
        generated_thread_object = {
            "runningThread": generated_uuid,
            "scenarioModule": scenario_module
        }
        threads.append(generated_thread_object)
    except Exception as e:
        return json.dumps({'success': False, 'message': str(e)}),
    return json.dumps({'success': True, 'data': {
        'runningThread': generated_uuid, 'scenarioId': scenario_module.scenario_id
    }})


@scenario.route('/upload', methods=['POST'])
def upload_scenario():
    scenario_file_json = request.get_json()
    file = open(os.path.join(os.path.dirname(sys.argv[0]), 'scenario', scenario_file_json['fileName']), "w")
    file.write(scenario_file_json['sequence'])
    file.close()

    return json.dumps({'success': True, 'filename': scenario_file_json['fileName']})


# schedule
@scheduler.route('/run', methods=['POST'])
def run_scheduler():
    try:
        scheduler_model = request.get_json()

        file = open(os.path.join(os.path.dirname(sys.argv[0]), 'scheduler', scheduler_model['fileName']), "w")
        file.write(scheduler_model['file'])
        file.close()

        mod = importlib.import_module('de.ananyev.fpla.runner.scheduler.' + scheduler_model['fileName'].split('.')[0])

        scheduler_module = mod.Scheduler()
        scheduler_module.start()
        generated_uuid = uuid.uuid4().__str__()
        generated_thread_object = {
            "runningThread": generated_uuid,
            "schedulerModule": scheduler_module
        }
        threads.append(generated_thread_object)
    except Exception as e:
        return json.dumps({'success': False, 'message': str(e)}),
    return json.dumps({'success': True, 'data': {
        'runningThread': generated_uuid, 'schedulerId': scheduler_module.scheduler_id
    }})
