import couchbaseDB as couchbase

date1 = "2021-01-01 00:00:00"
date2 = "2021-01-25 12:00:00"
#-DATE FORMAT- yyyy-mm-dd HH:MM:SS

def queryCountConnectedBetweenTimes(datetime1,datetime2):
    connectTrue = 0
    try:
        result = couchbase.cluster.query(
            "SELECT connected as Connected FROM accessPointLogs WHERE formattedDate between '" + date1 + "' and '" + date2 + "' AND connected = true",
            couchbase.QueryOptions(metrics=True))

        for row in result:
            connectTrue = connectTrue + 1


        return connectTrue
    except couchbase.CouchbaseException as ex:
        import traceback
        traceback.print_exc()

print(queryCountConnectedBetweenTimes(date1,date2))