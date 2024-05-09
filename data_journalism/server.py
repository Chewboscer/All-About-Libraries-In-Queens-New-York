from flask import Flask
from flask import render_template
from flask import request 
import math
import json


app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def about():
    f = open("data/solar.json", "r")
    data = json.load(f)
    f.close()
    

    zipcodes = []
    for year in data:
        for zip in data[year]:
            if len(zip) == 3:
                if (zip not in zipcodes):
                    zipcodes.append(zip)


    return render_template('about.html', zipcodes=zipcodes)

@app.route('/macro')
def macro():
    f = open("data/solar.json", "r")
    data = json.load(f)
    f.close()

    gotData = {}
    zipcodes = []
    for year in data:
        for zip in data[year]:
            if zip: 
                if len(zip) == 3:
                    if zip not in zipcodes:
                        zipcodes.append(zip)
                    if zip not in gotData:
                        gotData[zip] = 0
    for year in data:
        for zip in data[year]:
            if zip:  
                gotData[zip] = int(gotData[zip]) + len(data[year][zip])

    colors = ["hsl(244, 85%, 90%)",  "hsl(244, 85%, 83%)",  "hsl(244, 85%, 76%)",  "hsl(244, 85%, 69%)",  "hsl(244, 85%, 62%)", "hsl(244, 85%, 55%)",  "hsl(244, 85%, 48%)",  "hsl(244, 85%, 41%)",   "hsl(244, 85%, 34%)","hsl(244, 85%, 27%)",   "hsl(244, 85%, 20%)"] 

    return render_template('macro.html', zipcodes=zipcodes, colors=colors, zip=zip, gotData=gotData)

@app.route('/micro/<zip>')
def micro(zip):
    f = open("data/solar.json", "r")
    data = json.load(f)
    f.close()

    zipcodes = []
    for year in data:
        for zip_code in data[year]:
            if len(zip_code) == 3:
                if (zip_code not in zipcodes):
                    zipcodes.append(zip_code)

    years = sorted(data.keys())
    project_counts = []
    voltages = []
    nyCount = []
    nyVoltage = []

    for year in years:
        if zip in data[year]:
            project_counts.append(len(data[year][zip]))

            total_voltage = 0
            count = len(data[year][zip]) 

            for volt in data[year][zip]:
                total_voltage += float(volt)

            if count > 0:
                average_voltage = total_voltage / count
            else:
                average_voltage = 0

            voltages.append(average_voltage)  
        else:
            project_counts.append(0)
            voltages.append(0) 
    print(voltages)
    
    for year in years:
        total_count = 0
        total_voltage = 0
        count = 0

        for zip_code in zipcodes:
            if zip_code in data[year]:
                total_count += len(data[year][zip_code])
                for volt in data[year][zip_code]:
                    total_voltage += float(volt) 
                    count += 1

        if count > 0:
            nyCount.append(total_count / len(zipcodes))
            nyVoltage.append(total_voltage / count)
        else:
            nyCount.append(0)
            nyVoltage.append(0)

    x_scale = 420 / (len(years) - 1 if len(years) > 1 else 1)


    small = False
    medium = False
    large = False

    year_length = (len(years)-1)
    if (max(project_counts)) < 600: 
        y_scale = 400 / 600
        project_labels = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
        small = True
    elif ((max(project_counts)) > 600) & ((max(project_counts)) < 2000):
        y_scale = 400 / 2000
        project_labels = [0,500,1000,1500,2000]
        medium = True
    elif (max(project_counts)) > 2000:
        y_scale = 400 / 8000
        project_labels = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
        large = True
    
    small1 = False
    medium1= False
    large1 = False
    small2=False

    midVolt = (sum(voltages) / len(voltages))

    if (sum(voltages) / len(voltages)) < 15000:
        if(max(voltages)< 40000):
            y_scale2 = 400 / 40000
            voltage_labels = [0, 10000, 20000, 30000, 40000]
            small1 = True
        elif(max(voltages) > 40000):
            y_scale2 = 400 / 60000
            voltage_labels = [0, 15000, 30000, 45000, 60000]
            small2 = True
    elif ((sum(voltages) / len(voltages)) > 10000) & ((sum(voltages) / len(voltages)) < 25000):
        y_scale2 = 400 / 100000
        voltage_labels = [0, 20000, 40000, 60000, 80000, 100000]
        medium1 = True
    elif ((sum(voltages) / len(voltages)) > 25000):
        y_scale2 = 400 / 600000
        voltage_labels = [0, 150000, 300000, 450000, 600000]
        large1 = True


    return render_template('micro.html', zipcodes = zipcodes, zip=zip, years=years, data=data, project_counts=project_counts, x_scale=x_scale, y_scale=y_scale, year_length=year_length, y_scale2=y_scale2, voltage_labels=voltage_labels, voltages=voltages, project_labels=project_labels, small=small, large=large, medium=medium, small1=small1, large1=large1, medium1=medium1, nyCount=nyCount, nyVoltage=nyVoltage, midVolt=midVolt, small2=small2)
app.run(debug=True)
