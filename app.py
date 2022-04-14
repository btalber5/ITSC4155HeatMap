import os  # os is used to get environment variables IP & PORT
from flask import Flask, render_template, session, redirect, request, jsonify, Response
from functools import wraps
import pymongo
import certifi
import couchbaseDB

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
client = pymongo.MongoClient(
    "mongodb://BraxtonT9:W5QSpI81YBBHrgas@cluster0-shard-00-00.ljtel.mongodb.net:27017,cluster0-shard-00-01.ljtel.mongodb.net:27017,cluster0-shard-00-02.ljtel.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-vp85gf-shard-0&authSource=admin&retryWrites=true&w=majority",
    tlsCAFile=certifi.where())
db = client.user_login_system


# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap


# Routes
from user import routes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == "POST":

        firstTime = request.form.get("starttime")
        endtime = request.form.get("endtime")

        formatFirstTime = firstTime + ":00:00"
        formattedfEndTime = endtime + ":00:00"

        numberOfTicks = int((couchbaseDB.convertTimetoMinutes(formattedfEndTime) - couchbaseDB.convertTimetoMinutes(
            formatFirstTime)) / 10)
        numberOfSteps = int(
            ((couchbaseDB.convertTimetoMinutes(formattedfEndTime) / 60) - (
                        couchbaseDB.convertTimetoMinutes(formatFirstTime) / 60)))
        numberOfNodesJson = {'NumofNodes': numberOfSteps}

        hoursStartTime = int(couchbaseDB.convertTimetoMinutes(formatFirstTime) / 60)

        jsonMonths = {

        }
        monthVal = "01"
        totalWeight = 0
        listMonth = []

        for y in range(0, 12):
            months = {

            }
            listTime = []


            convertedStart = int(couchbaseDB.convertTimetoMinutes(formatFirstTime))
            for i in range(0, numberOfSteps):
                timeDict = {}
                queryTime1 = couchbaseDB.deconvertTimeToMinutes(convertedStart)

                queryTime2 = couchbaseDB.deconvertTimeToMinutes(
                    couchbaseDB.convertTimetoMinutes(queryTime1) + 60)
                #print(queryTime2)
                queryMonth = couchbaseDB.queryCountBetweenTimesofAll(queryTime1, queryTime2, monthVal, "2021")

                timeDict[hoursStartTime + i + 1] = {

                    "connectedValue": queryMonth,
                    "monthVal": monthVal,
                    "time": hoursStartTime + i + 1
                }
                totalWeight = totalWeight + queryMonth
                listTime.append(timeDict)
                print(listTime)

                convertedStart = couchbaseDB.convertTimetoMinutes(queryTime2)
            months["month_" + str(y)] = {

                "Time": listTime

            }

            locals().update(months)
            listMonth.append(months)
            monthValInt = int(monthVal) + int("01")


            if(monthValInt < 10):
                monthVal = "0" + str(monthValInt)
            else:
                monthVal = str(monthValInt)

        jsonData = {
            "Month": listMonth

        }
        print(jsonData)

        return render_template('testingCouchbase.html', queriedInfo=jsonData, startdate=firstTime, enddate=endtime,numberOfSteps = numberOfSteps,totalWeight = totalWeight,hoursStartTime = hoursStartTime)
    else:
        return render_template('dashboard.html')


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
