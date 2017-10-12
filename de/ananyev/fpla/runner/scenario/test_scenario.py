from de.ananyev.fpla.runner.scenario.abstract_scenario import AbstractScenario
from de.ananyev.fpla.runner.util import gen_db_resource
from de.ananyev.fpla.runner.util.browser_type import BrowserType
from de.ananyev.fpla.runner.util import browser_helper


class Scenario(AbstractScenario):
    def __init__(self):
        super().__init__()
        self.scenario_id = 1

    def do_run(self):
        proxy = self.get_proxy()
        device = self.get_device()
        self.open_browser(BrowserType.PHANTOM_JS, proxy=proxy, device=device)
        print(self.get_proxy_ip())
        file_name = browser_helper.make_screen_shot(self.browser)
        # try:
        #     self.login()
        # except BaseException as e:
        #     print(e)

    def login(self):
        self.browser.get('https://m.facebook.com/login')
        self.browser.find_element_by_xpath("//input[@name='email']").send_keys(self.data['FB_USER']['EMAIL'])
        self.random_sleep()
        try:
            self.browser.find_element_by_xpath("//input[@name='pass']").send_keys(self.data['FB_USER']['PASSWORD'])
        except:
            pass
        self.random_sleep()
        self.browser.find_element_by_xpath("//*[@name='login']").click()
        if not self.login_status:
            # todo save screenshot and stop
            self.stop = True

    def login_status(self):
        if "save-device" in self.browser.current_url:
            self.browser.find_element_by_xpath("//a[contains(@href,'cancel')]").click()
            return True
        if "home.php" in self.browser.current_url:
            return True
        return False

    # https://m.facebook.com/checkpoint/block/

    def get_proxy(self):
        proxy = None
        if 'PROXY' in self.data:
            proxy = self.data['PROXY']
        return proxy

    def get_device(self):
        device = None
        if 'DEVICE' in self.data:
            device = self.data['DEVICE']
        return device

    def get_proxy_ip(self):
        self.browser.get("https://www.whatismybrowser.com/")
        return self.browser.find_element_by_xpath('//*[@title="Your IP Address"]').text

    def basic_settings(self):
        # main setting
        self.browser.find_element_by_xpath("//a/*[contains(text(),'Main Menu')]/ancestor::a").click()
        self.random_sleep()
        # account settings
        self.browser.find_element_by_xpath("//a/*[contains(text(),'Account Settings')]/ancestor::a").click()
        self.random_sleep()
        # general
        self.browser.find_element_by_xpath("//a[contains(@href,'/settings/account/')]").click()

if __name__ == '__main__':
    users = gen_db_resource.get_all('FB_USER')
    proxies = gen_db_resource.get_all('PROXY')
    devices = gen_db_resource.get_all('DEVICE')
    scenario = Scenario()
    user = next((item for item in users if item['ID'] == 2), None)
    proxy = next((item for item in proxies if item['ID'] == user['PROXY_ID']), None)
    device = next((item for item in devices if item['ID'] == user['DEVICE_ID']), None)
    scenario.data['FB_USER'] = user
    scenario.data['PROXY'] = proxy
    scenario.data['DEVICE'] = device
    # print(users)
    # print(proxies)
    print(user)
    print(proxy)
    print(device)
    scenario.run()