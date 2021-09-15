import sys
sys.path.insert(0, '../logger')
from Logger import Logger
import datetime
class DateTimeService:
    def __init__(self):
        Logger.log().info("DateTimeService initialized")
    @staticmethod
    def get_current_date_time(self, type):
        if not type:
            type = "%d %b %Y"
        mydate = datetime.datetime.now()
        try:
            curr_date = mydate.strftime(type)
        except Exception as ex:
            Logger.error_log(ex)
        return curr_date