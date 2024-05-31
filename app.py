from flask import Flask, render_template
import time
from typing import List

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

class Washer:
    def __init__(self, state: str) -> None:
        self.state: str = state
        self.start_time: float = time.time()
        cycle_time = 1740  # 1740 seconds = 29 minutes
        self.end_time: float = self.start_time + cycle_time

class Dryer:
    def __init__(self, state: str, timer: int = 0) -> None:
        self.state: str = state
        self.timer: int = timer

    def add_time(self, additional_time: int) -> None:
        self.timer += additional_time

class Building:
    def __init__(self, washer_num: int, dryer_num: int) -> None:
        self.machines: List[Washer or Dryer] = []
        self.chat_memory: List[str] = []
        self.washer_num: int = washer_num
        self.dryer_num: int = dryer_num

    def add_machine(self, machine: Washer or Dryer) -> None:
        self.machines.append(machine)

# Home page
@app.route("/")
def index() -> str:
    buildings: List[str] = [
        'Sontag', 'Dialynas', 'Norton', 'Lawry', 'Clark 1', 'Clark 3',
        'Clark 5', 'Walker', 'Smiley', 'Oldenborg', 'Blaisdell', 'Mudd',
        'Lyon', 'Harwood', 'Gibson', 'Wig'
    ]
    return render_template('index.html', buildings=buildings)

# Page of machines for given building
@app.route('/<building>')
def buildingFunc(building: str) -> str:
    machines: List[str] = ['Washer1', 'Washer2', 'Washer3', 'Washer4', 'Dryer1', 'Dryer2', 'Dryer3', 'Dryer4']
    return render_template('building.html', machines=machines)

if __name__ == "__main__":
    # debug=True allows for auto updates. 
    # Without this you need to restart server to see updates.
    # Moreover, our port is currently on 8000.
    app.run(debug=True, host="127.0.0.1", port=8000)