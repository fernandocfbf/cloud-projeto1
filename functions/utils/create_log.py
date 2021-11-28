from datetime import datetime


def create_log(text, type=None):
    string = "[{0}]: {1}".format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'), text)
    print(string)
    with open(r'./' + 'log.txt', 'a+') as f:
        f.seek(0)
        data = f.read(100)
        if len(data) > 0 :
            f.write("\n")
        f.write(string)