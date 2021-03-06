from time import sleep
import os

keyboard_path = os.environ.get('KEYBOARD_PATH', '/dev/hidg0')
mouse_path = os.environ.get('MOUSE_PATH', '/dev/hidg1')


def _write_to_hid_interface_immediately(hid_path, buffer):
    try:
        with open(hid_path, 'wb+') as hid_handle:
            hid_handle.write(bytearray(buffer))
    except BlockingIOError:
        print('Failed to write to HID interface: %s. Is USB cable connected?',
              hid_path)


KEYCODE_LEFT_CTRL = 0xe0
KEYCODE_LEFT_SHIFT = 0xe1
KEYCODE_LEFT_ALT = 0xe2
KEYCODE_LEFT_META = 0xe3
KEYCODE_RIGHT_CTRL = 0xe4
KEYCODE_RIGHT_SHIFT = 0xe5
KEYCODE_RIGHT_ALT = 0xe6
KEYCODE_RIGHT_META = 0xe7
_MODIFIER_KEYCODES = [
    KEYCODE_LEFT_CTRL, KEYCODE_LEFT_SHIFT, KEYCODE_LEFT_ALT, KEYCODE_LEFT_META,
    KEYCODE_RIGHT_CTRL, KEYCODE_RIGHT_SHIFT, KEYCODE_RIGHT_ALT,
    KEYCODE_RIGHT_META
]


def send_keystroke(keyboard_path, control_keys, hid_keycode):
    buf = [0] * 8
    buf[0] = control_keys
    buf[2] = hid_keycode
    _write_to_hid_interface_immediately(keyboard_path, buf)
    if hid_keycode not in _MODIFIER_KEYCODES:
        release_keys(keyboard_path)


def release_keys(keyboard_path):
    _write_to_hid_interface_immediately(keyboard_path, [0] * 8)


def send_mouse_event(mouse_path, button, dx, dy, wheel):
    report = [button, dx & 0xff, dy & 0xff, wheel & 0xff]
    _write_to_hid_interface_immediately(mouse_path, report)


def key_stroke(key_event):
    send_keystroke(keyboard_path, key_event[1], key_event[0])
    return {'success': True}


def mouse_action(mouse_event):
    send_mouse_event(
        mouse_path, mouse_event[0], mouse_event[1], mouse_event[2], mouse_event[3])
    return {'success': True}

debug = True
sent = []
actions = {
    1: -20, 2: -19, 3: -18, 4: -17, 5: -16, 6: -15, 7: -14, 8: -13, 9: -12, 10: -11, 11: -10, 12: -9, 13: -8, 14: -7, 15: -6, 16: -5, 17: -4, 18: -3, 19: -2, 20: -1, 21: 0, 22: 1, 23: 2, 24: 3, 25: 4, 26: 5, 27: 6, 28: 7, 29: 8, 30: 9, 31: 10, 32: 11, 33: 12, 34: 13, 35: 14, 36: 15, 37: 16, 38: 17, 39: 18, 40: 19, 41: 20, 42: -20, 43: -19, 44: -18, 45: -17, 46: -16, 47: -15, 48: -14, 49: -13, 50: -12, 51: -11, 52: -10, 53: -9, 54: -8, 55: -7, 56: -6, 57: -5, 58: -4, 59: -3, 60: -2, 61: -1, 62: 0, 63: 1, 64: 2, 65: 3, 66: 4, 67: 5, 68: 6, 69: 7, 70: 8, 71: 9, 72: 10, 73: 11, 74: 12, 75: 13, 76: 14, 77: 15, 78: 16, 79: 17, 80: 18, 81: 19, 82: 20, 83: 1, 84: 2, 85: 4, 86: 0x0, 87: -1, 88: 0, 89: 1, 90: [0x04, 0x0], 91: [0x05, 0x0], 92: [0x06, 0x0], 93: [0x07, 0x0], 94: [0x08, 0x0], 95: [0x09, 0x0], 96: [0x0a, 0x0], 97: [0x0b, 0x0], 98: [0x0c, 0x0], 99: [0x0d, 0x0], 100: [0x0e, 0x0], 101: [0x0f, 0x0], 102: [0x10, 0x0], 103: [0x11, 0x0], 104: [0x12, 0x0], 105: [0x13, 0x0], 106: [0x14, 0x0], 107: [0x15, 0x0], 108: [0x16, 0x0], 109: [0x17, 0x0], 110: [0x18, 0x0], 111: [0x19, 0x0], 112: [0x1a, 0x0], 113: [0x1b, 0x0], 114: [0x1c, 0x0], 115: [0x1d, 0x0], 116: [0x1e, 0x0], 117: [0x1f, 0x0], 118: [0x20, 0x0], 119: [0x21, 0x0], 120: [0x22, 0x0], 121: [0x23, 0x0], 122: [0x24, 0x0], 123: [0x25, 0x0], 124: [0x26, 0x0], 125: [0x27, 0x0], 126: [0x28, 0x0], 127: [0x29, 0x0], 128: [0x2a, 0x0], 129: [0x2b, 0x0], 130: [0x2c, 0x0], 131: [0x2d, 0x0], 132: [0x2e, 0x0], 133: [0x2f, 0x0], 134: [0x30, 0x0], 135: [0x31, 0x0], 136: [0x33, 0x0], 137: [0x34, 0x0], 138: [0x35, 0x0], 139: [0x36, 0x0], 140: [0x37, 0x0], 141: [0x38, 0x0], 142: [0x4a, 0x0], 143: [0x4d, 0x0], 144: [0x4f, 0x0], 145: [0x50, 0x0], 146: [0x51, 0x0], 147: [0x52, 0x0], 148: [0x04, 0x02], 149: [0x05, 0x02], 150: [0x06, 0x02], 151: [0x07, 0x02], 152: [0x08, 0x02], 153: [0x09, 0x02], 154: [0x0a, 0x02], 155: [0x0b, 0x02], 156: [0x0c, 0x02], 157: [0x0d, 0x02], 158: [0x0e, 0x02], 159: [0x0f, 0x02], 160: [0x10, 0x02], 161: [0x11, 0x02], 162: [0x12, 0x02], 163: [0x13, 0x02], 164: [0x14, 0x02], 165: [0x15, 0x02], 166: [0x16, 0x02], 167: [0x17, 0x02], 168: [0x18, 0x02], 169: [0x19, 0x02], 170: [0x1a, 0x02], 171: [0x1b, 0x02], 172: [0x1c, 0x02], 173: [0x1d, 0x02], 174: [0x1e, 0x02], 175: [0x1f, 0x02], 176: [0x20, 0x02], 177: [0x21, 0x02], 178: [0x22, 0x02], 179: [0x23, 0x02], 180: [0x24, 0x02], 181: [0x25, 0x02], 182: [0x26, 0x02], 183: [0x27, 0x02], 184: [0x2d, 0x02], 185: [0x2e, 0x02], 186: [0x2f, 0x02], 187: [0x30, 0x02], 188: [0x31, 0x02], 189: [0x33, 0x02], 190: [0x34, 0x02], 191: [0x35, 0x02], 192: [0x36, 0x02], 193: [0x37, 0x02], 194: [0x38, 0x02], 195: [0x06, 0x01], 196: [0x19, 0x01],
}

for action in actions:
    # print(str(action))
    # Key Actions
    if isinstance(actions[action], list):
        if debug is False:
            key_stroke(actions[action])
        sent.append([action, 'key'])
     # Mouse Actions
    elif isinstance(actions[action], int):
        if action < 42:
            if debug is False:
                mouse_action([0, actions[action], 0, 0])  # delta_x
            print('delta_x ', actions[action])
            sent.append([actions[action], 'deltax'])
        elif action > 41 and action < 83:
            if debug is False:
                mouse_action([0, 0, actions[action], 0])  # delta_y
            sent.append([actions[action], 'deltay'])
            print('delta_y ', actions[action])
        elif action == 83:
            if debug is False:
                mouse_action([actions[action], 0, 0, 0])  # btn_1
            sent.append([action, 'btn1'])
        elif action == 84:
            if debug is False:
                mouse_action([actions[action], 0, 0, 0])  # btn_2
            sent.append([action, 'btn2'])
        elif action == 85:
            if debug is False:
                mouse_action([actions[action], 0, 0, 0])  # btn_3
            sent.append([action, 'btn3'])
        elif action == 86:
            if debug is False:
                mouse_action([0, 0, 0, 0])  # none
            sent.append([action, 'none'])
        elif action == 87:
            if debug is False:
                mouse_action([0, 0, 0, actions[action]])  # whl_dwn
            sent.append([action, 'whl_dwn'])
        elif action == 88:
            if debug is False:
                mouse_action([0, 0, 0, actions[action]])  # whl_none
            sent.append([action, 'whl_none'])
        elif action == 89:
            if debug is False:
                mouse_action([0, 0, 0, actions[action]])  # whl_up
            sent.append([action, 'whl_up'])
    else:
        print('NullEvent')

with open('actionsSent.txt', 'w') as filehandle:
    for action in sent:
        if isinstance(action, list):
            filehandle.writelines("%s\n" % action)
