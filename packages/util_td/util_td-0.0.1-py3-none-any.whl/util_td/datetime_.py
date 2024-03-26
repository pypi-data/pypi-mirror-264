import datetime
import string
from dateutil.parser import parse

DATETIME_TPL = '%Y-%m-%d %H:%M:%S'
DATE_TPL = '%Y-%m-%d 00:00:00'
LOG_TPL = '%Y%m%d_%H%M%S' # 日志字符串模板

def dt_to_str(time, tpl=DATETIME_TPL):
    if isinstance(time, datetime.datetime):
        return time.strftime(tpl)
    elif isinstance(time, str):
        return parse(time).strftime(tpl)
    else:
        return time

#dt_str = dt_to_mq(datetime.datetime.now())
#dt_str = dt_to_mq('2022-04-14')

def get_date_str(time):
    return dt_to_str(time, DATE_TPL)
