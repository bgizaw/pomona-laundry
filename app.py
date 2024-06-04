from flask import Flask, render_template, request
import datetime
from typing import List
import json
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
class Washer:
    def __init__(self, state, end_time):
        self.state = state
        self.end_time = end_time

    def start_washer(self, setting):
        start_time = datetime.datetime.now()
        time_change = datetime.timedelta(minutes=setting)
        self.end_time = start_time + time_change

    def change_state(self, state):
        #state should be an integer
        if state == 0:
            self.state = "available"
        elif state == 1:
            self.state = "in-use"
        elif state == 2:
            self.state = "pending"
        elif state == 3:
            self.state = "broken"
        elif state == 4:
            self.state = "reserved"
            #comment

    def __str__(self) -> str:
        return "Washer:" + " " + self.state + " " + "-" + self.time_remaining
        
class Dryer:
    def __init__(self, state, end_time):
        self.state = state
        self.end_time = end_time

    def start_dryer(self, setting):
        start_time = datetime.datetime.now()
        time_change = datetime.timedelta(minutes=setting)
        self.end_time = start_time + time_change

    def add_time(self, additional_time):
        time_change = datetime.timedelta(minutes=additional_time)
        self.end_time += additional_time

    def __str__(self) -> str:
        return "Dryer:" + " " + self.state + " " + "-" + self.timer

class Building:
    def __init__(self, name, washer_num, dryer_num):
        self.name = name
        self.machines = {
            "Washers": [],
            "Dryers" : []
        }
        self.chat_memory = []
        self.washer_num = washer_num
        self.dryer_num = dryer_num

        for washer in range(washer_num):
            self.machines["Washers"].append(Washer("available", 0))

        for dryer in range(dryer_num):
            self.machines["Dryers"].append(Dryer("available", 0))

    def add_machine(self, machine):
        self.machines.append(machine)

    def __str__(self):
        return "Building: " + self.name + "  " + "washers: " + str(self.washer_num) + "  " + "dryers: " + str(self.dryer_num)

with open("templates/machineInfo.json", "r") as json_file:
    data = json.load(json_file)

building_list = [Building(item['building'], item['washers'], item['dryers'])
                 for item in data]

# Home page
@app.route("/")
def index():
    return render_template('index.html', buildings=building_list)

# Page of machines for given building
@app.route('/<building>')
def buildingFunc(building):
    for building_item in building_list:
        if building_item.name == building:

            return render_template('building.html', currBuilding=building_item)
    # fix error handling at some point
    return render_template('building.html', "Error: Building Not Found")

#Page for washer
@app.route('/<building>/<washer>')
def washerFunc(building, washer):
    # creating a folder when someone goes to the washer
    newpath = f"buildings/{building}/{washer}/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        file = open(f"{newpath}machine_info.txt", 'w')
        file.write("Status: Available\n")
        file.write("Current Time: 0\n")
        file.close()
    
    with open(f"{newpath}machine_info.txt", 'r') as file:
        content = file.read()
    return render_template('washer.html', content = content, building=building, washer=washer)

# Page for dryer
@app.route('/<building>/<dryer>')
def dryerFunc(building, dryer):
    # creating a folder when someone goes to the dryer
    newpath = f"buildings/{building}/{dryer}/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        file = open(f"{newpath}machine_info.txt", 'w')
        file.write("Status: Available\n")
        file.write("Current Time: 0\n")
        file.close()
    
    with open(f"{newpath}machine_info.txt", 'r') as file:
        content = file.read()
    return render_template('dryer.html', content = content)

# available, unavailable, pending, reserved, and out of order
@app.route('/update-washer-state', methods=['POST'])
def updateWasherStateFunc():
    if request.method == 'POST':
        information = request.form.getlist('status')[0].split(', ')
        building = information[0]
        washer = information[1]
        choice = information[2]
        fullpath = f"buildings/{building}/{washer}/machine_info.txt"
        with open(fullpath, 'r') as file:
             data = file.readlines()
        
        with open(fullpath, "w") as file:
             data[0] = f'Status: {choice}\n'
             data[1] = f'Current Time: 0\n'
             file.writelines(data)
        
        with open(fullpath, 'r') as file:
            content = file.read()
        
        return render_template('washer.html', content = content, building=building, washer=washer)

@app.route('/update-washer-time', methods=['POST'])
def updateWasherTimeFunc():
    if request.method == 'POST':
        information = request.form.getlist('Time')[0].split(', ')
        building = information[0]
        washer = information[1]
        choice = information[2]
        fullpath = f"buildings/{building}/{washer}/machine_info.txt"
        with open(fullpath, 'r') as file:
             data = file.readlines()
        
        with open(fullpath, "w") as file:
             data[0] = f'Status: Unavailable\n'
             data[1] = f'Current Time: {choice}\n'
             file.writelines(data)
        
        with open(fullpath, 'r') as file:
            content = file.read()
        
        return render_template('washer.html', content = content, building=building, washer=washer)
    

@app.route('/update-dryer-state', methods=['POST'])
def updateDryerStateFunc():
    if request.method == 'POST':
        information = request.form.getlist('status')[0].split(', ')
        building = information[0]
        dryer = information[1]
        choice = information[2]
        fullpath = f"buildings/{building}/{dryer}/machine_info.txt"
        with open(fullpath, 'r') as file:
             data = file.readlines()
        
        with open(fullpath, "w") as file:
             data[0] = f'Status: {choice}\n'
             data[1] = f'Current Time: 0\n'
             file.writelines(data)
        
        with open(fullpath, 'r') as file:
            content = file.read()
        
        return render_template('dryer.html', content = content, building=building, dryer=dryer)

@app.route('/update-dryer-time', methods=['POST'])
def updateDryerTimeFunc():
    if request.method == 'POST':
        information = request.form.getlist('Time')[0].split(', ')
        building = information[0]
        dryer = information[1]
        choice = information[2]
        fullpath = f"buildings/{building}/{dryer}/machine_info.txt"
        with open(fullpath, 'r') as file:
             data = file.readlines()
        
        with open(fullpath, "w") as file:
             data[0] = f'Status: Unavailable\n'
             data[1] = f'Current Time: {choice}\n'
             file.writelines(data)
        
        with open(fullpath, 'r') as file:
            content = file.read()
        
        return render_template('dryer.html', content = content, building=building, dryer=dryer)

@app.route('/check_washer_status2')
def updateWasherStatus2():
    building = 'Sontag'
    washer = 'Washer1'
    # creating a folder when someone goes to the washer
    newpath = f"buildings/{building}/{washer}/"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        file = open(f"{newpath}machine_info.txt", 'w')
        file.write("Status: Available\n")
        file.write("Current Time: 0\n")
        file.close()
    
    with open(f"{newpath}machine_info.txt", 'r') as file:
        content = file.read()
    return render_template('washer_status.html', content = content, building= building, washer= washer)


if __name__ == "__main__":
    # debug=True allows for auto updates. 
    # Without this you need to restart server to see updates.
    # Moreover, our port is currently on 8000.
    app.run(debug=True, host="127.0.0.1", port=8000)