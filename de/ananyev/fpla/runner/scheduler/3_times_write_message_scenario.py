from de.ananyev.fpla.runner.scheduler.abstract_scheduler import AbstractScheduler
from de.ananyev.fpla.runner.util import gen_db_resource
from de.ananyev.fpla.runner.controller import main_controller

import schedule
import time

class Scheduler(AbstractScheduler):
        
    def __init__(self):
        super().__init__() 
        self.scheduler_id = 1
        
        
    def do_run(self):
        print(123)
        schedule.every().second.do(self.wall_post)
        while True:
            schedule.run_pending()
            time.sleep(1)
            
        
    def wall_post(self):
        print(456)
        users = gen_db_resource.get_all("FB_USER")
        print(users)
        #for user in users:
            # main_controller.run_scenario("wall_post.py", {"user": user})
        return

