import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from mpl_toolkits import mplot3d
import datetime
import dateutil
from mayavi import mlab


def parse_accelerometer_data_file_line(line):
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


def load_data_from_file(path):
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
    data_points = list(map(parse_accelerometer_data_file_line, data_lines))

    print('Loaded ' + str(len(data_points)) + ' data points')
    return data_points


def data_points_to_series(data_points):
    """
    Convert a list of data point dictionaries to a list for each axis over time (similar to unzip)

    Parameters
    ----------
    data_points:
        List of Dictionaries with keys:
            'x','y','z': float
            't': datetime

    Returns
    ----------
    data_series:
        Dictionary with keys:
            'x','y','z','t': Array of floats for each value as a series over time

    """
    xdata = [point['x'] for point in data_points]
    ydata = [point['y'] for point in data_points]
    zdata = [point['z'] for point in data_points]
    tdata = [point['t'].timestamp() for point in data_points]

    data_series = {
        'x': xdata,
        'y': ydata,
        'z': zdata,
        't': tdata
    }

    return data_series


def center_data_series(data):
    for key in ['x', 'y', 'z']:
        data[key] = data[key] - np.mean(data[key])


def remove_outliers_data_series(data_series, std_limit):
    indices_to_delete = np.array([])

    for key in ['x', 'y', 'z']:
        this_series = data_series[key]
        std = np.std(this_series)
        new_indices_to_delete = np.argwhere(np.abs(this_series -
                                                   np.mean(this_series)) > std_limit*std)
        indices_to_delete = np.append(indices_to_delete, new_indices_to_delete)

    for key in ['x', 'y', 'z']:
        for index in sorted(indices_to_delete, reverse=True):
            data_series[key] = np.delete(data_series[key], index)


def plot_raw_accelerometer_data3d(data):

    xdata = [point['x'] for point in data]
    ydata = [point['y'] for point in data]
    zdata = [point['z'] for point in data]
    tdata = [point['t'].timestamp() for point in data]

    fig_raw = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(xdata, ydata, zdata, c=tdata, cmap='Blues')
    plt.show()

    return fig_raw


def plot_raw_accelerometer_data(data):

    xdata = [point['x'] for point in data]
    ydata = [point['y'] for point in data]
    zdata = [point['z'] for point in data]
    tdata = [point['t'].timestamp() for point in data]

    fig_raw = plt.figure()

    lim = (-2, 2)

    plt.subplot(3, 1, 1)
    plt.ylabel('X data')
    plt.ylim(lim)
    plt.plot(tdata, xdata)

    plt.subplot(3, 1, 2)
    plt.ylabel('Y data')
    plt.ylim(lim)
    plt.plot(tdata, ydata)

    plt.subplot(3, 1, 3)
    plt.ylabel('Z data')
    plt.ylim(lim)
    plt.plot(tdata, zdata)

    plt.show()

    return fig_raw


def plot_integrate(data_series):
    xline = np.array([])
    yline = np.array([])
    zline = np.array([])

    x, y, z = 0, 0, 0
    vx, vy, vz = 0.0, 0.0, 0.0

    for i in range(3500):
        dt = data_series['t'][i+1] - data_series['t'][i]

        vx += data_series['x'][i]
        vy += data_series['y'][i]
        vz += data_series['z'][i]

        x += vx * dt
        y += vy * dt
        z += vz * dt

        xline = np.append(xline, x)
        yline = np.append(yline, y)
        zline = np.append(zline, z)

    fig = plt.figure()
    plt.scatter(xline, yline, color='b')
    plt.show()

    return


def plot_integrate3d(data):
    xline = np.array([])
    yline = np.array([])
    zline = np.array([])

    x, y, z = 0, 0, 0
    vx, vy, vz = 0.0, 0.0, 0.0

    for i in range(500):
        dt = data[i+1]['t'].timestamp() - data[i]['t'].timestamp()
        data_point = data[i]

        vx += data_point['x']
        vy += data_point['y']
        vz += data_point['z']

        x += vx * dt
        y += vy * dt
        z += vz * dt

        xline = np.append(xline, x)
        yline = np.append(yline, y)
        zline = np.append(zline, z)

    sizeline = np.empty(len(xline)).fill(0.25)
    s = mlab.plot3d(xline, yline, zline, tube_radius=50)
    mlab.show()
    return s


data_points = load_data_from_file(
    'accelerometer-plotting/accelerometer20200420-1.txt')

data_series = data_points_to_series(data_points)

center_data_series(data_series)
#remove_outliers_data_series(data_series, 1)
# plot_raw_accelerometer_data(data)
plot_integrate(data_series)

plt.show()
print('done')
