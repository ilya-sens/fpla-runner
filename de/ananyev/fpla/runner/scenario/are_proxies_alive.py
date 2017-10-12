from de.ananyev.fpla.runner.scenario.abstract_scenario import AbstractScenario
from de.ananyev.fpla.runner.util import gen_db_resource
from de.ananyev.fpla.runner.util.browser_type import BrowserType
from de.ananyev.fpla.runner.util import browser_helper


class Scenario(AbstractScenario):
        
    def __init__(self):
        super().__init__() 
        self.scenario_id = 13
        
    def do_run(self):
        proxy = None
        if 'PROXY' in self.data:
            proxy = self.data['PROXY']
        try:
            self.open_browser(BrowserType.GOOGLE_CHROME, proxy=proxy)
            self.browser.get("https://www.whatismybrowser.com/")
            ip = self.browser.find_element_by_xpath('//*[@title="Your IP Address"]').text
            self.random_sleep()
            if ip == proxy['IP']:
                proxy['ACTIVE'] = True
                import datetime
                proxy['COMMENT'] = "Working. Last check {}".format(str(datetime.datetime.now()))
            else:
                file_name = browser_helper.make_screen_shot(self.browser)
                proxy['ACTIVE'] = False
                import datetime
                proxy['COMMENT'] = "Wrong IP. Last check {}. See {}".format(str(datetime.datetime.now()), file_name)
            gen_db_resource.update('PROXY', proxy)
        except BaseException as e:
            file_name = browser_helper.make_screen_shot(self.browser)
            proxy['ACTIVE'] = False
            proxy['COMMENT'] = "Proxy seems to be down. See {}".format(file_name)
            gen_db_resource.update('PROXY', proxy)
            print(str(e))


if __name__ == '__main__':
    scenario = Scenario()
    scenario.data['PROXY'] = {'IP': '23.245.73.210', 'PORT': '4444', 'USERNAME': '2f2d7dad0f', 'PASSWORD': 'UpmjDQ4b'}
    scenario.run()