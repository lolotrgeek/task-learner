# Test for setting a specific state as a reward signal
# I.e. taking a screenshot and seeing if AI can learn
# to get to the same location as the screenshot was taken
# by using distance in pixels of current state from the goal state

# Usage:
# press esc to quit
# press ` to save state

import pickle
import cv2
import numpy as np
import socket
import sys
from time import sleep
from keyMap import keymap
from humanMap import actions_x, actions_y, actions_keys
from pynput import keyboard

# Start Stream
stream = cv2.VideoCapture(0)
stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# grab initial frame from stream
ret, im = stream.read(0)
cv2.namedWindow("Frame")

dimensions = im.shape
height = dimensions[0]
width = dimensions[1]

last_move = None
connection = False
done = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def on_press(key):
    global done
    modifier = str(key).startswith('Key.')
    if modifier is True:
        key = str(str(key).split('.')[1])
    else:
        key = key.char

    if key == 'esc':
        done = True
    
    try:
        keycode = keymap[key]
        buf = [0] * 8
        buf[0] = keycode[1]  # modifier
        buf[2] = keycode[0]  # hid code
        send(buf)
        send([0] * 8)  # release keys

    except KeyError:
        print('special key')

def relative_pos(pos, total):
    return min(1.0, max(0.0, pos / total))

def scale_mouse_coordinates(relative_x, relative_y):
    # This comes from LOGICAL_MAXIMUM in the mouse HID descriptor.
    max_hid_value = 32767.0
    x = int(relative_x * max_hid_value)
    y = int(relative_y * max_hid_value)
    return x, y

def to_action(abs_x, abs_y):
    pass

def mouse_event(event, x, y, flags, param):
    global last_move
    global width
    global height
    rel_x = relative_pos(x, width)
    rel_y = relative_pos(y, height)
    scale_x, scale_y = scale_mouse_coordinates(rel_x, rel_y)

    if last_move is None:
        last_move = [x, y]

    abs_x = x - last_move[0]
    abs_y = y - last_move[1]

    button = 0
    wheel = 0

    if event == 1 or event == 2:
        button = event
    if flags > 0:
        wheel = 1
    elif flags < 0:
        wheel = -1

    rel = [0] * 6
    rel[0] = button
    rel[1] = scale_x & 0xff
    rel[2] = (scale_x >> 8) & 0xff
    rel[3] = scale_y & 0xff
    rel[4] = (scale_y >> 8) & 0xff
    rel[5] = wheel & 0xff

    buf = [0] * 4 
    buf[0] = button
    buf[1] = abs_x & 0xff
    buf[2] = abs_y & 0xff
    buf[3] = wheel & 0xff

    print(abs_x & 0xff, abs_y & 0xff)

    try :
        actions = (actions_x[abs_x], actions_y[abs_y])
        # print('actions ' , actions)
    except:
        # print('not action ' , abs_x, abs_y)
        pass

    # print(rel)
    # send(buf)
    send(rel)     

    last_move = [x, y]


def send(event):
    global connection
    if connection is False:
        print(event)
        return
    try:
        message = bytearray(event)
        sock.sendall(message)
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
    except:
        print('unable to send', event)
        return


def saveState(frame):
    with open('goal.state', 'wb') as filehandle:
        pickle.dump(frame, filehandle)
    print('Done.')


cv2.setMouseCallback("Frame", mouse_event)
keyListener = keyboard.Listener(on_press=on_press)
keyListener.start()


try:
    print('connecting...')
    sock.connect(('192.168.1.248', 10000))
    connection = True

except:
    print('Unable to Connect')
    pass
try:
    while True:
        if done is True:
            break
        ret, im = stream.read(0)
        cv2.imshow("Frame", im)
        key = cv2.waitKeyEx(1)
        if key & 0xFF == ord('`'):
            print('Saving State...')
            goal = cv2.resize(im, (640, 480))
            saveState(goal)
            break
except:
    pass

print('Exiting...')
sock.close()
keyListener.stop()
stream.release()
cv2.destroyAllWindows()
sys.exit()
