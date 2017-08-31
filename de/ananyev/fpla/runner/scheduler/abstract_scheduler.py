import sys
import threading
import trace
import traceback
from inspect import getframeinfo

from de.ananyev.fpla.runner.util.set_trace import SetTrace


class AbstractScheduler(threading.Thread):
    status = ""
    tracer = trace.Trace(
        ignoredirs=[sys.prefix, sys.exec_prefix],
        trace=False,
        count=True)

    def __init__(self):
        super(AbstractScheduler, self).__init__()
        self.exceptions = []
        self.stop = False
        self.scheduler_id = 0

    def run(self):
        with SetTrace(self.monitor):
            try:
                self.do_run()
            except Exception as e:
                self.exceptions.append(''.join(traceback.format_exception_only(type(e), e)))

    def do_run(self):
        raise NotImplemented

    def monitor(self, frame, event, arg):
        if self.stop:
            self._stop()
        if event == "line":
            frame_info = getframeinfo(frame)
            if "/scheduler/" in frame_info.filename:
                self.status = '%s %s' % (frame_info.filename, frame_info.lineno)
        return self.monitor
