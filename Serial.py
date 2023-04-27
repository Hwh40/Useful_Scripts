"""
Author: Henry Hall
Prints data from a specified serial port to a live graph. Session is 
ended when the ENTER key is hit. 

Data must be printed to the serial port in form:
'S'
'\n'
'data1'
'\n'
'data2'
'\n'
...

"""

import numpy as np
import matplotlib.pyplot as plt
import serial
import time
import keyboard

PORT = 'COM9'
BAUD = 1000000
MAX_OUT = 10
WIDTH = 20
EXCEPTIONS = [["b'\\n'", "b'S'"], ['\\', '']]

def graph_set(fig, axes):
    """Sets the graph settings"""
    axes.grid(True)
    axes.set_xlabel('Time (s)')
    axes.set_title('Readings')

def plot(fig, axes, xs, ys, i):
    """Clears graph data and plots new data live"""
    axes.cla()
    graph_set(fig, axes)
    if xs[-1] < WIDTH:
        axes.set_xlim([0, WIDTH])
    else:
        axes.set_xlim([xs[-1] - WIDTH, xs[-1]])
    for j in range(0, i):
        axes.plot(xs, ys[j], label = f'Reading{j + 1}')
    axes.legend()
    plt.pause(0.001)

def set_data(data, xs, ys, start):
    """Puts time and data into x and y lists"""
    for i in range(0, len(data)):
        ys[i].append(data[i])
    if len(xs) == 0:
        start = time.time()
    xs.append(time.time() - start)

def check_end(axes, fig, xs):
    """Checks to see if the session has been quit"""
    if keyboard.is_pressed('Enter'):
        print('Quit')
        axes.set_xlim([0, xs[-1]])
        plt.show()
        return True
    else:
        return False

def set_ys():
    """Sets an empty y list"""
    ys = []
    for i in range(0, MAX_OUT):
        ys.append([])
    return ys

get_b = lambda ser: str(ser.read())

def main():
    """The main function"""
    #Set all initial values and empty lists
    fig1 = plt.figure("Figure")
    axes = plt.axes() 
    ser = serial.Serial(PORT, BAUD)
    start = time.time()
    print(ser.name)
    is_done = False
    is_first = True
    xs = []
    ys = set_ys()
    data = []
    s = ''
    byte = get_b(ser)
    while is_done != True:
        #Continuous while loop which reads, proccesses and plots data from the serial port
        try:
            if byte == "b'S'":
                is_first = False
                if data != []:
                    set_data(data, xs, ys, start)
                    plot(fig1, axes, xs, ys, len(data))
                data = []
                byte = get_b(ser)
                byte = get_b(ser)
            if byte == "b'\\n'":  
                data.append(float(s))
                s = ''
            if (byte not in EXCEPTIONS[0]) and (list(byte)[2] not in EXCEPTIONS[1]):
                s += list(byte)[-2]
            is_done = check_end(axes, fig1, xs)
            byte = get_b(ser)
        except:
            print('Restarting')
            is_first = True
            data = []
            xs = []
            ys = set_ys()
            s = ''            

main()