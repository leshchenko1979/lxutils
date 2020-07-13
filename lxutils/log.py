import datetime

lastlog = 0

def log (text):
    global lastlog
    if lastlog == 0:
        print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + text)
    else:
        print ('{}: {}, +{}s'.format(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            text,
            str(datetime.datetime.now()-lastlog)
        ))
    lastlog = datetime.datetime.now()
