import datetime

def compare(item1,item2):
  date1 = item1['day']
  date2 = item2['day']
  if len(date1) > len(date2):
    return 1
  if len(date2) < len(date1):
    return -1
  mounth1 = int(date1[5:7])
  mounth2 = int(date2[5:7])
  if mounth1 > mounth2:
    return 1
  if mounth1 < mounth2:
    return -1
  day1 = int(date1[8:10])
  day2 = int(date2[8:10])
  if day1 > day2:
    return 1
  if day1 < day2:
    return -1
  hour1 = int(item1['hour'][0:2])
  hour2 = int(item2['hour'][0:2])
  if hour1 > hour2:
    return 1
  if hour1 < hour2:
    return -1
  return 0


def compare2(item1, item2):
  if item1['datetime'] > item2['datetime']:
    return 1
  elif item1['datetime'] < item2['datetime']:
    return -1
  else:
    return 0
