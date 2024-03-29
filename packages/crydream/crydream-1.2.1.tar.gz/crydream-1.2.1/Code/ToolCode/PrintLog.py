import datetime
import os
import sys
import time

sys.path.append(os.path.dirname(__file__))


class Print_Log:
    def __init__(self):
        self.Print_Save = False
        self.temp = ""

    def logPrevious(self, address):
        self.temp = sys.stdout
        if self.Print_Save == True:
            now_time = datetime.datetime.now()
            time_now = now_time.strftime("%Y-%m-%d_%H-%M-%S")
            Print_log = open("%s/%s.log" % (address, time_now), 'w')
            sys.stdout = Print_log
            return True
        else:
            return False

    def logUpper(self, time):
        print("时间消耗：%.2f s" % time)

        if self.Print_Save == True:
            sys.stdout = self.temp
            return True
        else:
            return False
