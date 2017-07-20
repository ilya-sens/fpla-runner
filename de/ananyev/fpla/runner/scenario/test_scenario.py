import time

from de.ananyev.fpla.runner.scenario.abstract_scenario import AbstractScenario


class Scenario(AbstractScenario):
    def __init__(self):
        super(Scenario, self).__init__()

    def do_run(self):
        self.open_browser()
        while True:
            time.sleep(5)
            self.browser.get('http://localhost:8761/')
            print(self.get_time())

    def get_time(self):
        current_time_element = self.browser.find_element_by_xpath(
            "//*[text()[contains(.,'Current time')]]/following-sibling::td")
        return current_time_element.text
