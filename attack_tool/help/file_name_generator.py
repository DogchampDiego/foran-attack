import datetime

def gen_file_name(tool_name, format, extension):
    delim = '-'
    res = [tool_name, delim, get_timestamp(), '.', extension]
    res = ''.join(res)
    return res

def get_timestamp():
    time = datetime.datetime.now()
    time = str(time.strftime("%Y%m%d-%H%M%S"))
    return time