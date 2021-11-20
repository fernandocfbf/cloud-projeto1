from datetime import datetime

def create_log(text):
    print("{0} -> {1}".format(datetime.now().strftime('%d/%m/%Y %H:%M:%S'), text))