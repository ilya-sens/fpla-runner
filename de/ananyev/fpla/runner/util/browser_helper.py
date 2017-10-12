import datetime
import random


def make_screen_shot(browser):
    file_name = '/tmp/fpla/screenshots/{}.png'.format(str(datetime.datetime.now()))
    browser.save_screenshot(file_name)
    return file_name


def get_random_user_agent():
    i = random.randint(0, 1)
    if i == 0:
        return 'user-agent=user-agent:Mozilla/5.0 ({}) AppleWebKit/537.36 (KHTML, like Gecko) ' \
               'Chrome/60.0.3112.101 Safari/537.36 '.format(_get_random_windows_version())
    if i == 1:
        return 'user-agent=Mozilla/5.0 ({}) AppleWebKit/537.36 (KHTML, like Gecko) ' \
               'Chrome/59.0.3071.109 Safari/537.36 '.format(_get_random_windows_version())


def _get_random_chrome_version():
    random_int = random.randint(0, 1)
    return '59.0.3071.109' if random_int == 0 else \
        '60.0.3112.101' if random_int == 1 else '60.0.3112.101'


def _get_random_windows_version():
    random_int = random.randint(0, 2)
    return 'Windows NT 6.3; Win64; x64' if random_int == 0 else \
           'Windows NT 10.0; Win64; x64' if random_int == 1 else \
           'Windows NT 6.2; Win64; x64' if random_int == 3 else \
           'Windows NT 6.1; WOW64'
