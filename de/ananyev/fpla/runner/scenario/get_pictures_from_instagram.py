from de.ananyev.fpla.runner.scenario.abstract_scenario import AbstractScenario
from de.ananyev.fpla.runner.util import gen_db_resource
from de.ananyev.fpla.runner.util.browser_type import BrowserType


class Scenario(AbstractScenario):
        
    def __init__(self):
        super().__init__() 
        self.scenario_id = 11
        
    def do_run(self):
        self.open_browser(BrowserType.PHANTOM_JS)
        stars = gen_db_resource.get_all("STARS")
        import os
        for star in stars:
            if not star['PARSED']:
                if not os.path.exists("/tmp/fpla/" + star['NAME']):
                    os.makedirs("/tmp/fpla/" + star['NAME'])
                self.find_in_insta(star)
        
    def find_in_insta(self, star):
        self.browser.get("https://www.instagram.com/explore/tags/hotgirl/")
        input_search = self.browser.find_element_by_xpath("//input")
        input_search.clear()
        input_search.send_keys(star['NAME'])
        self.random_sleep(5, 7)
        try:
            link = self.browser.find_element_by_xpath("//input/following::a[not(contains(@href,'explore'))]")
            link.click()
            self.random_sleep(10, 15)
            self.browser.find_element_by_xpath("//article//a//img/ancestor::a").click()
            self.random_sleep(10, 15)
            amount_parsed = 0
            for i in range(30):
                try:
                    img_src = self.browser.find_element_by_xpath("//div[@role='dialog']//div/img").get_attribute("src")
                    import urllib.request
                    import datetime
                    urllib.request.urlretrieve(img_src, "/tmp/fpla/" + star['NAME'] + "/" + str(datetime.datetime.now()) + ".jpg")
                    amount_parsed = 1 + amount_parsed
                    self.random_sleep()
                except BaseException as e:
                    print(e)
                    # video
                    pass
                try:
                    self.browser.find_element_by_xpath("//a[contains(@class, 'coreSpriteRightPaginationArrow')]").click()
                    self.random_sleep()
                except:
                    break
            star['PARSED'] = True
            star['NOTIFICATION'] = "Successfully parsed. Pictures: " + str(amount_parsed)
            gen_db_resource.update("STARS", star)
        except BaseException as e:
            print(e)
            import datetime
            screen_shot_path = "/tmp/screenshots/" + str(datetime.datetime.now()) + ".png"
            self.browser.save_screenshot(screen_shot_path)
            star['PARSED'] = True
            star['NOTIFICATION'] = "Exception by parsing: " + str(e) \
                                   + " Possible reason: private account. Screen shot: " + screen_shot_path
            gen_db_resource.update("STARS", star)


if __name__ == '__main__':
    Scenario().run()