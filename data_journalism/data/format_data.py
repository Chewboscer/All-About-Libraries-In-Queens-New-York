import json

f1 = open("data/solar_data.csv", "r")
lines = f1.readlines()

dict = {}

for index in range(1, len(lines)): 
    splitter = lines[index].split(",")
    year = splitter[0].split("/")[2]
    zip = splitter[4][0:3]
    voltage = splitter[8].strip()
    print(year,zip,voltage)

    if (year not in dict):
        dict[year] = {}

    if (zip not in dict[year]):
        dict[year][zip] = []

    dict[year][zip].append(voltage)

f1.close()

f2 = open("solar.json", "w")
json.dump(dict, f2, indent=4)

f2.close()




    

