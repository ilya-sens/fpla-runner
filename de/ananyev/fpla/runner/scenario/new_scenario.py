from de.ananyev.fpla.runner.scenario.abstract_scenario import AbstractScenario

class Scenario(AbstractScenario):
    def do_run(self):
      self.open_browser()
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

