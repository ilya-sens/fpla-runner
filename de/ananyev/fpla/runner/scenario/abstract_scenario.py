import random
import sys
import threading
import trace
import traceback
import time
import signal
from inspect import getframeinfo

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy

from de.ananyev.fpla.runner.util.chrome_proxy_helper import create_proxyauth_extension
from de.ananyev.fpla.runner.util.chrome_header_helper import create_modheaders_plugin
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

    def open_browser(self, browser_type=BrowserType.PHANTOM_JS, proxy=None, device=None):
        if browser_type == BrowserType.PHANTOM_JS:
            # headers
            desired_capabilities = dict(DesiredCapabilities.PHANTOMJS)
            if device is not None:
                desired_capabilities["phantomjs.page.settings.userAgent"] = (device['USER_AGENT'])
            else:
                desired_capabilities["phantomjs.page.settings.userAgent"] = (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87")
            # proxy
            service_args = []
            if proxy is not None and 'IP' and 'PORT' in proxy:
                service_args.append('--proxy=https://{}:{}'.format(proxy['IP'], proxy['PORT']))
                service_args.append('--proxy-type=https')
                service_args.append('--ignore-ssl-errors=true')
                if 'USERNAME' and 'PASSWORD' in proxy:
                    service_args.append('--proxy-auth={}:{}'.format(proxy['USERNAME'], proxy['PASSWORD']))
            # start
            self.browser = webdriver.PhantomJS(
                "/home/ilya/Programming/fpla/fpla-core/node_modules/phantomjs-prebuilt/bin/phantomjs",
                desired_capabilities=desired_capabilities, service_args=service_args)
        elif browser_type == BrowserType.GOOGLE_CHROME:
            # user agent
            desired_capabilities = dict(DesiredCapabilities.CHROME)
            co = Options()
            if device is not None:
                co.add_argument(device['USER_AGENT'])
            else:
                co.add_argument("user-agent=Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36")
            # proxy
            if proxy is not None and 'IP' and 'PORT' in proxy:
                proxyauth_plugin_path = create_proxyauth_extension(
                    proxy_host="{}".format(proxy['IP']),
                    proxy_port=proxy['PORT'],
                    proxy_username=proxy['USERNAME'] if 'USERNAME' in proxy else '',
                    proxy_password=proxy['PASSWORD'] if 'PASSWORD' in proxy else ''
                )
                co.add_extension(proxyauth_plugin_path)
            # initiate
            self.browser = webdriver.Chrome(
                "/usr/lib/chromium-browser/chromedriver",
                desired_capabilities=desired_capabilities,
                chrome_options=co)
        resolution_width = 1024
        resolution_height = 768
        if device is not None:
            resolution = device['RESOLUTION'].split('x')
            resolution_width = resolution[0]
            resolution_height = resolution[1]
        print(resolution_width)
        self.browser.set_window_size(resolution_width, resolution_height)

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
            self.browser.service.process.send_signal(signal.SIGTERM)
            self.browser.quit()
        except:
            pass

    def random_sleep(self, from_secs=1, till_secs=3):
        time.sleep(random.uniform(from_secs, till_secs))
