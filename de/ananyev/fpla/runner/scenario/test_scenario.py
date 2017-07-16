import time

from selenium import webdriver


class TestScenario():
    def __init__(self):
        self._items = {}

    browser = None

    def run(self):
        self.openBrowser()
        while True:
            time.sleep(5)
            self.getTime()
            # todo save in the db

    def openBrowser(self):
        self.browser = webdriver.PhantomJS(
            "/home/ilya/Programming/fpla/fpla-core/node_modules/phantomjs-prebuilt/bin/phantomjs")
        self.browser.get('http://localhost:8761/')

    def getTime(self):
        current_time_element = self.browser.find_element_by_xpath(
            "//*[text()[contains(.,'Current time')]]/following-sibling::td")
        print(current_time_element.text)
