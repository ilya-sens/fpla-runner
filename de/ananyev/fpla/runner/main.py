from de.ananyev.fpla.runner.controller.main_controller import MainController
# tracerTest must be imported to be started from tracer
from de.ananyev.fpla.runner.script.test_script import Script
import trace
import sys


PORT = 3434


if __name__ == '__main__':
    try:
        import argparse
        parser = argparse.ArgumentParser(description='Fpla-Runner')
        parser.add_argument('-p', '--port', type=int, dest="PORT")
    except Exception:
        pass

mainController = MainController()
mainController.app.run('localhost', PORT)
