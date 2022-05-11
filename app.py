import os  # os is used to get environment variables IP & PORT
from flask import Flask, render_template, session, redirect, request, jsonify, Response
from functools import wraps
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from forms import ContactForm
import couchbaseDB
import datetime
import configparser

app = Flask(__name__)

# Configuration
config = configparser.ConfigParser()
config.read('configuration.ini')
default = config['DEFAULT']
app.secret_key = default['SECRET_KEY']
app.config['MONGO_DBNAME'] = default['DATABASE_NAME']
app.config['MONGO_URI'] = default['MONGO_URI']
app.config['PREFERRED_URL_SCHEME'] = "https"

# Create Pymongo
mongo = PyMongo(app)

# Create Bcrypt
bc = Bcrypt(app)

# Create CSRF protect
csrf = CSRFProtect()
csrf.init_app(app)

# Routes
from user import routes


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about')    

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
                queryMonth = couchbaseDB.queryCountBetweenTimesofAll(queryTime1, queryTime2, monthVal, "2020")
                result = couchbaseDB.cb2_coll_default.get("agg_2021_"+monthVal)


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

@app.route('/dashboard2/', methods=['GET', 'POST'])
@login_required
def dashboard2():

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
                sTime = datetime.datetime.now()
                result = couchbaseDB.cb2_coll_default.get("agg_2021_" + monthVal)

                eTime = datetime.datetime.now()

                execTime = eTime - sTime
                print(execTime)

                timeDict[hoursStartTime + i + 1] = {

                    "connectedValue": result.content['aggregate'][queryTime1 + "-"+queryTime2]['weight'],
                    "monthVal": monthVal,
                    "time": hoursStartTime + i + 1
                }
                totalWeight = totalWeight + result.content['aggregate'][queryTime1 + "-"+queryTime2]['weight']
                listTime.append(timeDict)
                print(listTime)

                convertedStart = couchbaseDB.convertTimetoMinutes(queryTime2)
            months["month_" + str(y)] = {

                "Time": listTime

            }

            locals().update(months)
            listMonth.append(months)
            monthValInt = int(monthVal) + int("01")

            if (monthValInt < 10):
                monthVal = "0" + str(monthValInt)
            else:
                monthVal = str(monthValInt)

        jsonData = {
            "Month": listMonth

        }


        return render_template('testingCouchbase.html',queriedInfo=jsonData, startdate=firstTime, enddate=endtime,numberOfSteps = numberOfSteps,totalWeight = totalWeight,hoursStartTime = hoursStartTime)
    else:
        return render_template('dashboard.html')


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
