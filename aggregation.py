year = 2021
import couchbaseDB

firstTime = "00:00:00"
lastTime = "11:59:00"
agg = {}

for z in range(0,1):
    monthVal = "01"
    listMonths = []
    for y in range(0, 12):
        month = {}


        convertedStart = int(couchbaseDB.convertTimetoMinutes(firstTime))
        for i in range(0,24):
            if(i != 23):
                queryTime1 = couchbaseDB.deconvertTimeToMinutes(convertedStart)
                queryTime2 = couchbaseDB.deconvertTimeToMinutes(
                    couchbaseDB.convertTimetoMinutes(queryTime1) + 60)
            else:
                queryTime1 = couchbaseDB.deconvertTimeToMinutes(convertedStart)
                queryTime2 = couchbaseDB.deconvertTimeToMinutes(
                    couchbaseDB.convertTimetoMinutes(queryTime1) + 59)
            queryMonth = couchbaseDB.queryCountBetweenTimesofAll(queryTime1, queryTime2, monthVal, str(year))
            print(queryTime1)
            print(queryTime2)
            print(monthVal)

            month[queryTime1 +"-"+queryTime2]= {
                "weight": queryMonth,
                "date": str(year)+  "-"+monthVal
             }


            locals().update(month)
            convertedStart = couchbaseDB.convertTimetoMinutes(queryTime2)

            key = "agg_" + str(year) + "_" + monthVal
            agg = {
                "aggregate" : month
            }
            couchbaseDB.upsert_document(agg, key)

        monthValInt = int(monthVal) + int("01")
        if (monthValInt < 10):
            monthVal = "0" + str(monthValInt)
        else:
            monthVal = str(monthValInt)
            print(agg)




    year =  year + 1
