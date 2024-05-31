from flask import Flask, render_template
import time
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

class Washer:
    def __init__(self, state):
        self.state = state
        self.start_time = time.time()
        self.end_time = self.start_time + 1740  # 1740 seconds = 29 minutes

class Dryer:
    def __init__(self, state, timer=0):
        self.state = state
        self.timer = timer

    def add_time(self, additional_time):
        self.timer += additional_time

class Building:
    def __init__(self, washer_num, dryer_num):
        self.machines = []
        self.chat_memory = []
        self.washer_num = washer_num
        self.dryer_num = dryer_num

    def add_machine(self, machine):
        self.machines.append(machine)

# Home page
@app.route("/")
def index():
    buildings = [
        'Sontag', 'Dialynas', 'Norton', 'Lawry', 'Clark 1', 'Clark 3',
        'Clark 5', 'Walker', 'Smiley', 'Oldenborg', 'Blaisdell', 'Mudd',
        'Lyon', 'Harwood', 'Gibson', 'Wig'
    ]
    return render_template('index.html', buildings=buildings)

# Page of machines for given building
@app.route('/<building>')
def buildingFunc(building):
    f = open('templates/machineInfo.json') # Load json file with all laundry room machine info
    data = json.load(f)
    return render_template('building.html', machines = data)

if __name__ == "__main__":
    # debug=True allows for auto updates. 
    # Without this you need to restart server to see updates.
    # Moreover, our port is currently on 8000.
    app.run(debug=True, host="127.0.0.1", port=8000)