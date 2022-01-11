# USER WARNING: Starting a matplotlib GUI outside of main will likely fail
# to-be-used in terminal/bash/linux for the plot
import time
import threading
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import pandas as pd
import requests
import csv
from queue import Queue

q = Queue()
lock = threading.Lock()


def read_ISS(qq):
    while True:
        response = requests.get("http://api.open-notify.org/iss-now.json")
        result = response.json()

        location = result['iss_position']
        latitude = float(location['latitude'])
        longitude = float(location['longitude'])
        print('[read_ISS]: ', [latitude, longitude])
        with lock:
            qq.put([latitude, longitude])
        time.sleep(1)


def write_ISS(qq):
    fieldnames = ["latitude", "longitude"]
    with open('position.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    while True:
        with open('position.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            while qq.empty():
                time.sleep(0.1)
                if not qq.empty():
                    with lock:
                        data = qq.get()
                        print('[write_ISS]: ', [data[0], data[1]])
                        latitude, longitude = data[0], data[1]

                        info = {
                            "latitude": latitude,
                            "longitude": longitude,
                        }
                        csv_writer.writerow(info)
                        csv_file.flush()
        time.sleep(1)


def animate(i):
    data = pd.DataFrame(list())
    while data.empty:
        time.sleep(2)
        data = pd.read_csv('position.csv')

    data.dropna()
    x = data['latitude']
    y = data['longitude']
    plt.cla()

    plt.plot(x, y)
    plt.draw()
    plt.tight_layout()
    plt.pause(1)


def plot_ISS(q):
    ani = FuncAnimation(plt.gcf(), animate, frames=100, interval=1000)
    plt.show()


def main():
    t1 = threading.Thread(target=read_ISS, args=(q,))
    t2 = threading.Thread(target=write_ISS, args=(q,))
    t3 = threading.Thread(target=plot_ISS, args=(q,))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()


if __name__ == '__main__':
    main()
