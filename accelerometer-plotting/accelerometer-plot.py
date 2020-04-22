import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from mpl_toolkits import mplot3d
import datetime
import dateutil

print("hi")


def parseAccelerometerDataLine(line):
    line_split = line.split(',')

    x = float(line_split[0])
    y = float(line_split[1])
    z = float(line_split[2])
    t = dateutil.parser.parse(line_split[3])

    data_point = {
        'x': x,
        'y': y,
        'z': z,
        't': t
    }

    return data_point


def loadDataFromFile(path):
    """
    Parameters:
      path : string
        Accelerometer log file path

    Returns:
    Array of accelerometer data entries as dictionaries
    """
    print('Loading data from ' + path)
    data_file = open(path)

    data_lines = data_file.readlines()
    data_points = list(map(parseAccelerometerDataLine, data_lines))

    return data_points


data = loadDataFromFile('accelerometer-plotting/accelerometer20200420-1.txt')

# for i in range(len(data)):
xdata = [point['x'] for point in data]
ydata = [point['y'] for point in data]
zdata = [point['z'] for point in data]
tdata = [point['t'].timestamp() for point in data]

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(xdata, ydata, zdata, c=tdata, cmap='Blues')

plt.show()
print('done')
