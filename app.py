from flask import Flask, render_template, request, redirect, url_for
import datetime
from typing import List
import json
import os


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
# create a washer class that will initialize with two parameters, to represent if a washer is available/working and 
# the real world time the machine will finish its cycle based on a datetime object
class Washer:
    def __init__(self, state, end_time):
        # will represent states like available, in use, pending, out of order, reserved
        self.state = state
        # what time the washer wil finish the cycle
        self.end_time = end_time

    def start_washer(self, setting):
        # acces the user's current browser time to reference
        start_time = datetime.datetime.now()
        # use timedelta to put the amount of time the user's machine will run for into a datetime object format
        # this will allow us to add it to their current browser time since that is also in a datetime object format
        time_change = datetime.timedelta(minutes=setting)
        # add the amount of time the machine will run for to the user's current time, resulting in the datetime object
        # formatted time for when their machine cycle will finish
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

    def cycle_complete(self, browserTime):
        # return a boolean True or False. We already have the end time of the cycle set in the start washer function
        # and the moment the user's browser time passes that set end time, meaning the time set for the cycle to finish
        # has already passed, the boolean will switch from returning False to True for if the cycle is complete
        return self.end_time < browserTime

    # format the Washer class object in the String format below. Without this, the class object will print as a class 
    # object, making debugging more difficult
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
        # the name of the building that the respective laundry room is related to
        self.name = name
        # supposed to represent the washers and dryers in each laundry room and whether they are available or not
        # but is not needed anymore due to the presence of our json file with all laundry room info
        self.machines = {
            "Washers": [],
            "Dryers" : []
        }
        # would have represented our chat memory but seems inefficient compared to better options offered by Node
        self.chat_memory = []
        # the number of washers in a given laundry room
        self.washer_num = washer_num
        # the number of dryers in a given laundry room
        self.dryer_num = dryer_num

        # not needed because of the JSON file with all machine data. These for loops would have populated the 
        # washer and dryer lists within the machines dictionary with the correct number of machines given the 
        # correct washer and dryer nums
        for washer in range(washer_num):
            self.machines["Washers"].append(Washer("available", 0))

        for dryer in range(dryer_num):
            self.machines["Dryers"].append(Dryer("available", 0))

    # adds a machine to the dictionary but does it incorrectly. we would have to key into the dictionary first
    # then append to the list in the value
    def add_machine(self, machine):
        self.machines.append(machine)

    def __str__(self):
        return "Building: " + self.name + "  " + "washers: " + str(self.washer_num) + "  " + "dryers: " + str(self.dryer_num)

# open and read the JSON file with all the laundry room data within it, then put that list of dictionaries into 
# data, which will represent a list of dictionaries
with open("templates/machineInfo.json", "r") as json_file:
    data = json.load(json_file)

# list comprehension to 
building_list = [Building(item['building'], item['washers'], item['dryers']) 
                 for item in data]
print(building_list[0])


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
    return render_template('building_error.html')


#Page for washer
# @app.route('/<building>/<washer>')
# def washerFunc(building, washer):
#     # creating a folder when someone goes to the washer
#     newpath = f"buildings/{building}/{washer}/"
#     if not os.path.exists(newpath):
#         os.makedirs(newpath)
#         file = open(f"{newpath}machine_info.txt", 'w')
#         file.write("Status: Available\n")
#         file.write("Current Time: 0\n")
#         file.close()
    
#     with open(f"{newpath}machine_info.txt", 'r') as file:
#         content = file.read()
#     return render_template('washer.html', content = content, building=building, washer=washer)



"""
**Washer Logic**
"""
@app.route('/washer/<building>/<washer>/', methods=['GET'])
def updateWasherFileData(building, washer):
    # creating a folder when someone goes to the washer
    newpath = f"buildings/{building}/{washer}/" #The file path of the folder that washer that the washer data file is within
    if request.method == 'GET':
        #get method is attempting to retrieve information from the stored data
        if not os.path.exists(newpath):
            #if that data does not currently exist in the database, create a new file for the 
            os.makedirs(newpath)
            file = open(f"{newpath}machine_info.txt", 'w')
            file.write("Status: Available\n")
            file.write("Completion Time: 0\n")
            file.close()
        else:
            with open(f"{newpath}/machine_info.txt", 'r') as file:
                data = file.readlines()
            
            time_data = data[1].split('Completion Time:')
            time_list = time_data[1].strip().split('/')
            # write error handling for this
            completion_time = datetime.datetime(int(time_list[0]),int(time_list[1]), int(time_list[2]), int(time_list[3]), int(time_list[4]), int(time_list[5]))
            time_remaining = completion_time - datetime.datetime.now() 
            
 
            if len(data) == 3:
                data[2] = f"Time Remaining: {time_remaining}\n"
            else:
                data.append(f"Time Remaining: {time_remaining}\n")

            with open(f'{newpath}/machine_info.txt', "w") as file:
                file.writelines(data)

    with open(f'{newpath}/machine_info.txt', 'r') as file:
        content = file.read()
            
    return render_template('washer_status.html', content = content, building= building, washer= washer)


# available, unavailable, pending, reserved, and out of order
@app.route('/update-washer-state', methods=['POST'])
def updateWasherStateFunc():
    if request.method == 'POST':
        information = request.form.getlist('status')[0].split(', ')
        building = information[0]
        washer = information[1]
        choice = information[2]
        fullpath = f"buildings/{building}/{washer}/machine_info.txt"
        
        if choice == 'In Use':
            with open(fullpath, 'r') as file:
                content = file.read()
            return render_template('washer_time.html', content = content, building=building, washer=washer)
        elif choice == "Out-of-Order":
            return redirect('https://pomona.webtma.com/?tkn=zR_pJHKh9JP45Xg9RPojIH2irxyiuxkXCrWY6I1oLlEMORHMSIfRo8C50hsmXjJNq3CC4shHe74IdVLeZelp9ZkWK50Q_luNhA7JFwQ6Lx2OfJd_pFK2rvhrrqeXGqLQywWvEnvUiNo4WgeJcevA2BSHiAXEKNTLwt39ZqtjT4fFs-oTtdZ1O0gv8UN-bLkhcSL7eqRIxeuVbG7ytk3eR5US9MexRJDmTpn6bAkOr0OvwjXtkjGGCJz3uj6jDN_6qPl4d7lOptkG5EDbRxzGXg')

        with open(fullpath, 'r') as file:
             data = file.readlines()
        
        with open(fullpath, "w") as file:
             data[0] = f'Status: {choice}\n'
             data[1] = f'Completion Time: 0\n'
             file.writelines(data)
        
        with open(fullpath, 'r') as file:
            content = file.read()
        
        return render_template('washer.html', content = content, building=building, washer=washer)


# this function is only for in-use logic
@app.route('/update-washer-time', methods=['POST'])
def updateWasherTimeFunc():
    if request.method == 'POST':
        information = request.form.getlist('Time')[0].split(', ')
        building = information[0]
        washer = information[1]
        choice = information[2]
        
        start_time = datetime.datetime.now()
        time_change = datetime.timedelta(minutes=int(choice))
        end_time = start_time+time_change
        Washer_Object = Washer("In Use", end_time=end_time)
        
        
        fullpath = f"buildings/{building}/{washer}/machine_info.txt"
        with open(fullpath, 'r') as file:
             data = file.readlines()
        
        
        with open(fullpath, "w") as file:
             data[0] = f'Status: Unavailable\n'
             data[1] = f'Completion Time: {Washer_Object.end_time.strftime("%Y/%m/%d/%H/%M/%S")}\n'
             file.writelines(data)
        
        with open(fullpath, 'r') as file:
            content = file.read()
        
        return render_template('washer_status.html', content = content, building=building, washer=washer)
    



"""
**Dryer logic**
"""



# Page for dryer
# @app.route('/<building>/<dryer>')
# def dryerFunc(building, dryer):
#     # creating a folder when someone goes to the dryer
#     newpath = f"buildings/{building}/{dryer}/"
#     if not os.path.exists(newpath):
#         os.makedirs(newpath)
#         file = open(f"{newpath}machine_info.txt", 'w')
#         file.write("Status: Available\n")
#         file.write("Completion Time: 0\n")
#         file.close()
    
#     with open(f"{newpath}machine_info.txt", 'r') as file:
#         content = file.read()
#     return render_template('dryer.html', content = content)


@app.route('/dryer/<building>/<dryer>', methods=['GET'])
def updateDryerFileData(building, dryer):
    # creating a folder when someone goes to the dryer
    newpath = f"buildings/{building}/{dryer}/"
    if request.method == 'GET':
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            file = open(f"{newpath}machine_info.txt", 'w')
            file.write("Status: Available\n")
            file.write("Completion Time: 0\n")
            file.close()
        else:
            with open(f"{newpath}/machine_info.txt", 'r') as file:
                data = file.readlines()
            
            time_data = data[1].split('Completion Time:')
            time_list = time_data[1].strip().split('/')
            completion_time = datetime.datetime(int(time_list[0]),int(time_list[1]), int(time_list[2]), int(time_list[3]), int(time_list[4]), int(time_list[5]))
            time_remaining = completion_time - datetime.datetime.now() 
            
 
            if len(data) == 3:
                data[2] = f"Time Remaining: {time_remaining}\n"
            else:
                data.append(f"Time Remaining: {time_remaining}\n")

            with open(f'{newpath}/machine_info.txt', "w") as file:
                file.writelines(data)

    with open(f'{newpath}/machine_info.txt', 'r') as file:
        content = file.read()
            
    return render_template('dryer_status.html', content = content, building= building, dryer= dryer)


@app.route('/update-dryer-state', methods=['POST'])
def updateDryerStateFunc():
    if request.method == 'POST':
        information = request.form.getlist('status')[0].split(', ')
        building = information[0]
        dryer = information[1]
        choice = information[2]
        fullpath = f"buildings/{building}/{dryer}/machine_info.txt"
        
        if choice == 'In Use':
            with open(fullpath, 'r') as file:
                content = file.read()
            return render_template('dryer_time.html', content = content, building=building, dryer=dryer)
        elif choice == "Out-of-Order":
            return redirect('https://pomona.webtma.com/?tkn=zR_pJHKh9JP45Xg9RPojIH2irxyiuxkXCrWY6I1oLlEMORHMSIfRo8C50hsmXjJNq3CC4shHe74IdVLeZelp9ZkWK50Q_luNhA7JFwQ6Lx2OfJd_pFK2rvhrrqeXGqLQywWvEnvUiNo4WgeJcevA2BSHiAXEKNTLwt39ZqtjT4fFs-oTtdZ1O0gv8UN-bLkhcSL7eqRIxeuVbG7ytk3eR5US9MexRJDmTpn6bAkOr0OvwjXtkjGGCJz3uj6jDN_6qPl4d7lOptkG5EDbRxzGXg')

        
        with open(fullpath, 'r') as file:
             data = file.readlines()
        
        with open(fullpath, "w") as file:
             data[0] = f'Status: {choice}\n'
             data[1] = f'Completion Time: 0\n'
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
        choice = int(information[2])
        add_time = int(request.form.get("additional-time"))
        choice = choice + add_time
        
        fullpath = f"buildings/{building}/{dryer}/machine_info.txt"


        with open(fullpath, 'r') as file:
             data = file.readlines()
        
        with open(fullpath, "w") as file:
             data[0] = f'Status: Unavailable\n'
             data[1] = f'Completion Time: {choice}\n'
             file.writelines(data)
        
        with open(fullpath, 'r') as file:
            content = file.read()
        
        return render_template('dryer_status.html', content = content, building=building, dryer=dryer)


# if __name__ == "__main__":
    # debug=True allows for auto updates. 
    # Without this you need to restart server to see updates.
    # Moreover, our port is currently on 8000.
    # app.run(debug=True, host="127.0.0.1", port=8000)
