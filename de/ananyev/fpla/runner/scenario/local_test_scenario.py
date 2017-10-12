from de.ananyev.fpla.runner.scenario.abstract_scenario import AbstractScenario
from de.ananyev.fpla.runner.util import gen_db_resource
from de.ananyev.fpla.runner.util.browser_type import BrowserType


class Scenario(AbstractScenario):
        
        
    def __init__(self):
        super().__init__() 
        self.scenario_id = 7
        
        
    def do_run(self):
        self.open_browser()
        import time
        time.sleep(5)
        self.browser.get('http://localhost:8761/')
        print(self.get_time())

    def get_time(self):
        current_time_element = self.browser.find_element_by_xpath(
             "//*[text()[contains(.,'Current time')]]/following-sibling::td")
        return current_time_element.text

