from datetime import datetime, time


def getRealTime():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S").split(":")
    return current_time


def toBinary(timeValue):
    return "{0:b}".format(int(timeValue))


def TimeToBinary():
    timeList = getRealTime()
    binaryTimeList = []

    for i in timeList:
        binaryTimeList.append(toBinary(int(i)))

    return binaryTimeList


binarytime = TimeToBinary()

print(binarytime)