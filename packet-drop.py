import subprocess
import json
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from multiprocessing import Process, Queue

def get_drop_counters():
    output = subprocess.check_output(["pktmon", "counters", "--type", "drop", "--json"])
    data = json.loads(output)
    counters = {}
    for group in data:
        for component in group["Components"]:
            for counter in component["Counters"]:
                name = f"{group['Group']} - {component['Name']} - {counter['Name']}"
                counters[name] = counter["Inbound"]["Packets"] + counter["Outbound"]["Packets"]
    return counters

def plot_data(q):
    plt.ion()
    fig, ax = plt.subplots()
    x, y = [], []
    line, = ax.plot(x, y)

    while True:
        counters = q.get()
        x.append(datetime.now())
        y.append( sum(counters.values()))
        line.set_xdata(x)
        line.set_ydata(y)
        ax.relim()
        ax.autoscale_view()
        date_format = mdates.DateFormatter('%H:%M:%S')
        ax.xaxis.set_major_formatter(date_format)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(1)

if __name__ == '__main__':
    try:
        subprocess.call(["pktmon", "start", "-c", "-o"])
        q = Queue()
        p = Process(target=plot_data, args=(q,))
        p.start()
    
        while True:
            counters = get_drop_counters()
            q.put(counters)
            time.sleep(1)
    finally: 
        subprocess.call(["pktmon", "stop"])

