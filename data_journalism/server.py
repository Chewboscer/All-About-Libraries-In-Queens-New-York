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
    print(gotData)
        
    

    colors = ["hsl(244, 85%, 90%)",  "hsl(244, 85%, 83%)",  "hsl(244, 85%, 76%)",  "hsl(244, 85%, 69%)",  "hsl(244, 85%, 62%)", "hsl(244, 85%, 55%)",  "hsl(244, 85%, 48%)",  "hsl(244, 85%, 41%)",   "hsl(244, 85%, 34%)","hsl(244, 85%, 27%)",   "hsl(244, 85%, 20%)"] 
   # dataColors = []
   # for i in range(len(gotData)):
        #dataColors.append(math.ceil(gotData[i]/3)-18)



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
    for year in years:
        if zip in data[year]:
            project_counts.append(len(data[year][zip]))
        else:
            project_counts.append(0)
        voltages.append((sum(project_counts)) / (len(project_counts)))

    y_scale = 400 / 1000
    y_scale2 = 400 / 1000
    x_scale = 420 / (len(years) - 1 if len(years) > 1 else 1)


    small = False
    medium = False
    large = False

    year_length = (len(years)-1)
    if (max(project_counts)) < 500: 
        y_scale = 400 / 500
        project_labels = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
        small = True
    elif ((max(project_counts)) > 500) & ((max(project_counts)) < 2000):
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

    if (max(voltages)) < 500:
        y_scale2 = 400 / 500
        voltage_labels = [0, 100, 200, 300, 400, 500]
        small1 = True
    elif ((max(voltages)) > 500) & ((max(voltages)) < 2000):
        y_scale2 = 400 / 2000
        voltage_labels = [0, 500, 1000, 1500, 2000]
        medium1 = True
    elif (max(voltages)) > 2000:
        y_scale2 = 400 / 10000
        voltage_labels = [0, 2000, 4000, 6000, 8000, 10000]
        large1 = True


    return render_template('micro.html', zipcodes = zipcodes, zip=zip, years=years, data=data, project_counts=project_counts, x_scale=x_scale, y_scale=y_scale, year_length=year_length, y_scale2=y_scale2, voltage_labels=voltage_labels, voltages=voltages, project_labels=project_labels, small=small, large=large, medium=medium, small1=small1, large1=large1, medium1=medium1)



















"""
    f = open("data/solar.json", "r")
    data = json.load(f)
    f.close()

    zipcodes = []
    for year in data:
        for zip in data[year]:
            if (zip not in zipcodes):
                zipcodes.append(zip)

    years = sorted(data.keys())
    project_counts = []
    average_voltages = []
    for year in years:
        if zip in data[year]:
            projects = data[year][zip]
            project_counts.append(len(projects))
            voltages = [float(voltage) for voltage in projects if voltage]  # Adjust based on actual data structure
            average_voltages.append(sum(voltages) / len(voltages) if voltages else 0)
        else:
            project_counts.append(0)
            average_voltages.append(0)

    year_length = (len(years) - 1)

    max_count = max(project_counts)
    x_scale = 420 / (len(years) - 1) 
    y_scale = 400 / max_count  
    max_voltage = max(average_voltages)
    y_scale2 = 400 / max_voltage  

"""

    



app.run(debug=True)
