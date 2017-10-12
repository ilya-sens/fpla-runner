from de.ananyev.fpla.runner.scenario.abstract_scenario import AbstractScenario
from de.ananyev.fpla.runner.util import gen_db_resource
from de.ananyev.fpla.runner.util.browser_type import BrowserType


class Scenario(AbstractScenario):
        
        
    def __init__(self):
        super().__init__() 
        self.scenario_id = 8
    def do_run(self):
        self.open_browser(BrowserType.GOOGLE_CHROME)
        while True:
      	    self.get_time()
      
    def get_time(self):
        import time
        time.sleep(5)
        self.browser.get("https://lenta.ru/")
        print(self.browser.find_element_by_xpath("//*[@id='date-time']").text)
        time.sleep(5)
        self.browser.get("http://example.com/")
        time.sleep(5)
        self.browser.get("https://angular.io/")

