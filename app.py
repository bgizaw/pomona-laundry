from flask import Flask, render_template
import time

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

class Washer:
    def __init__ (self, state, endTime, ):
        self.state = state
        
        startTime = time.time()
        endTime = startTime + 1740
        

class Dryer:
    def __init__ (self, state, timer):
        self.state = state
        self.timer = timer

    def add_time ()
        self.timer 

    
class Building:
    def __init__(self, Washer, Dryer, Chat_Memory, WasherNum, DryerNum):
        self.machines = []
        self.chat_Memory = []
        self.washer_num = 0
        self.dryer_num = 0

    def machine_add (machine):
        self.machines.append(machine)
        

    

@app.route("/") #home page
def index():
    buildings = ['Sontag', 'Dialynas', 'Norton', 'Lawry', 'Clark 1', 'Clark 3', 'Clark 5', 'Walker', 'Smiley', 'Oldenborg', 'Blaisdell', 'Mudd', 'Lyon', 'Harwood', 'Gibson', 'Wig']
    return render_template('index.html', buildings=buildings)

@app.route('/building/<building>') #page of machines for given building
def buildingFunc():
    machines = ['Washer1', 'Washer2', 'Washer3', 'Washer4', 'Dryer1', 'Dryer2', 'Dryer3', 'Dryer4']
    return render_template('building.html', machines=machines)

@app.route('/Machine')
def machineFunc():
    return "machine"

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000) #debug=True allows for auto updates. without this you need to restart server to see updates

