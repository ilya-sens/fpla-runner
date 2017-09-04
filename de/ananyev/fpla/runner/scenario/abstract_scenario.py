import random
import sys
import threading
import trace
import traceback
import time
from inspect import getframeinfo

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from de.ananyev.fpla.runner.util.set_trace import SetTrace
from de.ananyev.fpla.runner.util.browser_type import BrowserType


class AbstractScenario(threading.Thread):
    status = ""
    browser = None
    tracer = trace.Trace(
        ignoredirs=[sys.prefix, sys.exec_prefix],
        trace=False,
        count=True)

    def __init__(self):
        super(AbstractScenario, self).__init__()
        self.data = {}
        self.exceptions = []
        self.stop = False
        self.schedule_id = 0
        self.scenario_id = 0

    def open_browser(self, browser_type=BrowserType.PHANTOM_JS):
        if browser_type == BrowserType.PHANTOM_JS:
            desired_capabilities = dict(DesiredCapabilities.PHANTOMJS)
            desired_capabilities["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87")
            self.browser = webdriver.PhantomJS(
                "/home/ilya/Programming/fpla/fpla-core/node_modules/phantomjs-prebuilt/bin/phantomjs",
                desired_capabilities=desired_capabilities)
        elif browser_type == BrowserType.GOOGLE_CHROME:
            desired_capabilities = dict(DesiredCapabilities.CHROME)
            self.browser = webdriver.Chrome(
                "/usr/lib/chromium-browser/chromedriver",
                desired_capabilities=desired_capabilities)
        self.browser.set_window_size(1024, 768)

    def run(self):
        with SetTrace(self.monitor):
            try:
                self.do_run()
            except BaseException as e:
                self.exceptions.append(''.join(traceback.format_exception_only(type(e), e)))

    def do_run(self):
        raise NotImplemented()

    def monitor(self, frame, event, arg):
        if self.stop:
            self._prepare_to_stop()
            self._stop()
        if event == "line":
            frame_info = getframeinfo(frame)
            if "/scenario/" in frame_info.filename:
                self.status = '%s %s' % (frame_info.filename, frame_info.lineno)
        return self.monitor

    def _prepare_to_stop(self):
        try:
            self.browser.close()
        except:
            pass

    def random_sleep(self, from_secs=1, till_secs=3):
        time.sleep(random.uniform(from_secs, till_secs))
