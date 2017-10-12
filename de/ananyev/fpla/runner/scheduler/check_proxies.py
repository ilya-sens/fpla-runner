from de.ananyev.fpla.runner.scheduler.abstract_scheduler import AbstractScheduler
from de.ananyev.fpla.runner.util import gen_db_resource
from de.ananyev.fpla.runner.controller import main_controller
from de.ananyev.fpla.runner.util.browser_type import BrowserType

import schedule
import time


class Scheduler(AbstractScheduler):
        
    def __init__(self):
        super().__init__() 
        self.scheduler_id = 2
        
    def do_run(self):
        proxies = gen_db_resource.get_all("PROXY")
        for proxy in proxies:
            main_controller.run_scenario("are_proxies_alive.py", data={"PROXY": proxy})


if __name__ == '__main__':
    Scheduler().run()