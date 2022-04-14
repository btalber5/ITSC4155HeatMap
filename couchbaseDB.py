from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator

from couchbase.cluster import QueryOptions
from couchbase.exceptions import CouchbaseException

cluster = Cluster('couchbase://ec2-18-213-185-222.compute-1.amazonaws.com', ClusterOptions(
PasswordAuthenticator('Administrator', 'password')))

cb = cluster.bucket('accessPointLogs')

cb_coll_default = cb.default_collection()



def upsert_document(doc):
  print("\nUpsert CAS: ")
  try:
    # key will equal: "airline_8091"
    key = doc["id"]
    result = cb_coll_default.upsert(key, doc)
    print(result.cas)
  except Exception as e:
    print(e)


def queryCountConnectedBetweenTimes(datetime1, datetime2,month):
  connectTrue = 0
  try:
    result = cluster.query(
      "SELECT connected as Connected FROM accessPointLogs WHERE formattedDate between '" + datetime1 + "' and '" + datetime2 + "' AND connected = true",
      QueryOptions(metrics=True))
    for row in result:
      connectTrue = connectTrue + 1

    return connectTrue
  except CouchbaseException as ex:
    import traceback
    traceback.print_exc()

def queryCountBetweenTimesofAll(time1,time2,month,year):
  connectTrue = 0
  try:
    result = cluster.query(
      "SELECT connected as Connected FROM accessPointLogs WHERE split(formattedDate,'-')[0] = '"+year+"' and split(formattedDate,'-')[1] = '"+month+"' and split(formattedDate,' ')[1] between '"+time1+"' and '"+time2+"' AND connected = true",
      QueryOptions(metrics=True))
    for row in result:
      connectTrue = connectTrue + 1

    return connectTrue
  except CouchbaseException as ex:
    import traceback
    traceback.print_exc()


def convertTimetoMinutes(time1):
  returnArray = time1.split(":",3)
  hourConvert = int(returnArray[0]) * 60
  minuteConvert = int(returnArray[1])
  totalMinutes = hourConvert + minuteConvert
  return totalMinutes

def deconvertTimeToMinutes(time1):
  if ((time1 % 60) == 0):
    hour = int(time1 / 60)
    minute = 0

  else:
    minute = int(time1 % 60)
    hour = int((time1 - minute)/60)


  if(hour < 10):
    if(minute < 10):
      returnTime = "0"+str(hour) + ":0" + str(minute) + ":00"
    else:
      returnTime = "0"+str(hour) + ":" + str(minute) + ":00"

  else:
    if(minute < 10):
      returnTime = str(hour) + ": 0" + str(minute) + ":00"
    else:
      returnTime = str(hour) + ":" + str(minute) + ":00"

  return returnTime



print(convertTimetoMinutes("08:00:00"))
print(convertTimetoMinutes("08:10:00"))

print(queryCountBetweenTimesofAll("00:00:00","02:00:00","01","2021"))






