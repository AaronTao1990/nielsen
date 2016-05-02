import time
from datetime import datetime

def str_to_seconds(time_s, format_s='%Y-%m-%d %H:%M:%S'):
    struct_t = time.strptime(time_s, format_s)
    return int(time.mktime(struct_t))

def str_to_mcroseconds(time_s, format_s='%Y-%m-%d %H:%M:%S'):
    struct_t = datetime.strptime(time_s, format_s)
    return time.mktime(struct_t.timetuple()) * 1000 + struct_t.microsecond / 1000

def get_current_date():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    print long(str_to_mcroseconds('2015-12-12 12:12:12'))
    print long(str_to_seconds('2015-12-12 12:12:12'))
