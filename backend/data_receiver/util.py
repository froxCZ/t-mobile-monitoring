import os
import pickle
from datetime import datetime
from datetime import timedelta
def dateToBucket(startDate,date,granularity):
    d = date - startDate
    diffMinutes = d.total_seconds() / 60;
    return round(diffMinutes / granularity)

def stringToDate(dateTimeStr):
    return datetime.strptime(dateTimeStr, "%d.%m.%y %H:%M:%S")

def bucketToDate(startDate:datetime,bucket,granularity):
    return startDate+timedelta(0,bucket*granularity*60)

def dateToWeekdayName(date):
    days=["Mo","Tu","We","Th","Fr","Sa","Su"]
    dayNumber=date.weekday()
    return days[dayNumber]

def isDateWorkDay(date):
    if date.weekday() <=4:
        return True
    else:
        return False

def createDirIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def pickleToFile(file,data):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    output = open(file, 'wb')
    pickle.dump(data, output)

def loadFromFile(file):
    input = open(file, 'rb')
    return pickle.load(input)