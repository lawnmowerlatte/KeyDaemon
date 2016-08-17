#!/usr/bin/python3

import time
import requests
from random import randint

class KeyDaemon(object):
    _SPECIAL_CHARS = {
        "LEFT_CTRL": 128,
        "CTRL": 128,
        "LEFT_SHIFT": 129,
        "SHIFT": 129,
        "LEFT_ALT": 130,
        "ALT": 130,
        "LEFT_GUI": 131,
        "GUI": 131,
        "LEFT_COMMAND": 131,
        "COMMAND": 131,
        "RIGHT_CTRL": 132,
        "RIGHT_SHIFT": 133,
        "RIGHT_ALT": 134,
        "RIGHT_GUI": 135,
        "RIGHT_COMMAND": 135,
        "UP_ARROW": 218,
        "UP": 218,
        "DOWN_ARROW": 217,
        "DOWN": 217,
        "LEFT_ARROW": 216,
        "LEFT": 216,
        "RIGHT_ARROW": 215,
        "RIGHT": 215,
        "BACKSPACE": 178,
        "TAB": 179,
        "RETURN": 176,
        "ESC": 177,
        "INSERT": 209,
        "DELETE": 212,
        "PAGE_UP": 211,
        "PAGE_DOWN": 214,
        "HOME": 210,
        "END": 213,
        "CAPS_LOCK": 193,
        "F1": 194,
        "F2": 195,
        "F3": 196,
        "F4": 197,
        "F5": 198,
        "F6": 199,
        "F7": 200,
        "F8": 201,
        "F9": 202,
        "F10": 203,
        "F11": 204,
        "F12": 205,
        "ENTER": 10
    }
    
    def __init__(self, ip, port="80", protocol="http", os="Windows"):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.os = os
        
        for k, v in self._SPECIAL_CHARS.items():
            setattr(self, k, v)
        
        self.delay = 0
        self.release_all()
        
    def _get(self, page, params=None):
        if params is not None:
            print(page + "?" + "&".join(["{}={}".format(k,v) for k, v in params.items()]))
        else:
            print(page)
            
            
        requests.get(self.endpoint + page,
                     params=params)
        time.sleep(.1)
    
    @classmethod
    def _get_special(cls, value):
        if value.upper() in cls._SPECIAL_CHARS.keys():
            value = cls._SPECIAL_CHARS[value.upper()]
        
        return value
    
    @classmethod
    def _is_special(cls, value):
        return value.upper() in cls._SPECIAL_CHARS.keys()
    
    @property
    def endpoint(self):
        return "{}://{}:{}/".format(self.protocol,
                                    self.ip,
                                    self.port)
    
    @property
    def state(self):
        return None
    
    @state.setter
    def state(self, value):
        if value not in ["on", "off"]:
            raise Exception("Invalid value {},"
            " value must be 'on' or 'off'".format(value))
    
        self._get("set_state", {"s": value})
    
    @property
    def delay(self):
        return None
    
    @delay.setter
    def delay(self, value):
        try:
            int(value)
        except:
            raise Exception("Invalid value {},"
            " value must be an integer".format(value))
        
        self._get("set_delay", {"d": value})
                     
    def send(self, value):
        for i in range(0, len(value), 20):
            self._get("send_characters", {"s": value[i:i+20]})
    
    def special(self, value):
        value = self._get_special(value)
        
        try:
            int(value)
        except:
            raise Exception("Invalid value {},"
            " value must be an integer".format(value))
    
        self._get("send_special", {"c": value})

    def press(self, value):
        if self._is_special(value):
            value = self._get_special(value)
            api = "press_special"
        else:
            api = "press_key"
            if len(value) > 1:
                raise Exception("Invalid value {},"
                " expected only one character".format(value))
        
        self._get(api, {"p": value})
    
    def release(self, value):
        if self._is_special(value):
            value = self._get_special(value)
            api = "release_special"
        else:
            api = "release_key"
            if len(value) > 1:
                raise Exception("Invalid value {},"
                " expected only one character".format(value))
        
        self._get(api, {"r": value})

    def mouse_act(self, action, button):
        button = button.lower()
        action = action.lower()
        
        if button not in ['left', 'right', 'middle']:
            raise Exception("Invalid button {},"
            " expected 'left', 'right' or 'middle'".format(button))
        
        if action not in ['click', 'press', 'release']:
            raise Exception("Invalid button {},"
            " expected 'left', 'right' or 'middle'".format(button))
        
        self._get("mouse_{}".format(action), {"b": button})
    
    def mouse_click(self, button):
        self.mouse_act("click", button)
    
    def mouse_press(self, button):
        self.mouse_act("press", button)
        
    def mouse_release(self, button):
        self.mouse_act("release", button)
        
    def mouse_move(self, x=0, y=0, w=0):
        try:
            int(x)
            int(y)
            int(w)
        except:
            raise Exception("Invalid value,"
            " all valuee must be integers")
        
        x = min(max(x, -127), 127)
        y = min(max(y, -127), 127)
        w = min(max(w, -127), 127)
        
        self._get("mouse_move", {"m": "{},{},{}".format(x, y, w)})

    # MACROS ########################
    def subliminal(self, message):
        self.delay = 0
        self.send(message)
        self.send(chr(178) * len(message))
    
    def select_all(self):
        if self.os == "OSX":
            key = "COMMAND"
        else:
            key = "CTRL"
    
        self.press(key)
        self.send("a")
        self.release(key)

    def ctrl_alt_del(self):
        if self.os == "OSX":
            keys = [
                "COMMAND",
                "ALT",
                "ESC"
            ]
        else:
            keys = [
                "CTRL",
                "ALT",
                "DELETE",
            ]
    
        self.press(keys[0])
        self.press(keys[1])
        self.special(keys[-1])
        self.release(keys[0])
        self.release(keys[1])
    
    def interactive(self):
        while(True):
            try:
                lines = raw_input("> ")
                
                for line in lines.split(";"):
                    line = line.strip()
                    
                    if line.upper() == "EOF":
                        exit()
                    elif self._is_special(line):
                        self.special(line)
                    elif line[0] == "/":
                        self.send(line[1:])
                    elif line[0] == ".":
                        eval("self." + line[1:])
                    else:
                        args = line.split()
                        if args[0] == "press":
                            for arg in args[1:]:
                                self.press(arg)
                        elif args[0] == "release":
                            for arg in args[1:]:
                                self.release(arg)
                        elif args[0] == "special":
                            for arg in args[1:]:
                                self.special(arg)
                        elif args[0] == "mouse":
                            if args[1] == "click":
                                self.mouse_click(args[2])
                            elif args[1] == "press":
                                self.mouse_press(args[2])
                            elif args[1] == "release":
                                self.mouse_release(args[2])
                            elif args[1] == "move":
                                if len(args) > 2:
                                    x = int(args[2])
                                else:
                                    x = 0
                                if len(args) > 3:
                                    y = int(args[3])
                                else:
                                    y = 0
                                if len(args) > 4:
                                    w = int(args[4])
                                else:
                                    w = 0
                            
                                self.mouse_move(x, y, w)
                        else:
                            print("Unknown command")
                    
            except Exception as e:
                print(e)
    
    def release_all(self, full=False):
        if full == False:
            modifiers = ["COMMAND", "CTRL", "ALT", "SHIFT", "GUI"]
        else:
            modifiers = self._SPECIAL_CHARS.keys()

        for key in modifiers:
            self.release(key)
            
    def alt_tab(self, tabs=1):
        if self.os == "OSX":
            key = "COMMAND"
        else:
            key = "ALT"
            
        self.press(key)
        
        for i in range(tabs):
            self.special('TAB')
            
        self.release(key)
    
    def tiny_circles(self, scale, count=1):
        for i in range(count+1):
            self.mouse_move(scale*2, 0, 0)
            self.mouse_move(scale, scale, 0)
            self.mouse_move(0, scale*2, 0)
            self.mouse_move(-scale, scale, 0)
            self.mouse_move(-scale*2, 0, 0)
            self.mouse_move(-scale, -scale, 0)
            self.mouse_move(-0, -scale*2, 0)
            self.mouse_move(scale, -scale, 0)
            
    def mouse_reset(self):
        for i in range(30):
            self.mouse_move(-127, -127)
    
    def mod(self, modifiers, keys):
        if not isinstance(modifiers, list): modifiers = [modifiers]
        if not isinstance(keys, list): keys = [keys]
        
        for mod in modifiers:
            self.press(mod)
        
        for key in keys:
            if self._is_special(key):
                self.special(key)
            else:
                self.send(key)
        
        for mod in modifiers:
            self.release(mod)
        
    
    def ctrl(self, keys):
        if self.os == "OSX":
            mod = "COMMAND"
        else:
            mod = "CTRL"
        
        self.mod(mod, keys)
    
    def alt(self, keys):
        self.mod("alt", keys)
        
    def gui(self, keys):
        self.mod("gui", keys)
        
    def shift(self, keys):
        self.mod("shift", keys)
    
    def copy(self):
        self.ctrl("c")
    
    def cut(self):
        self.ctrl("x")
        
    def paste(self):
        self.ctrl("v")
        
    def undo(self):
        self.ctrl("z")
        
    def scramble(self, length):
        for i in range(length):
            self.shift("left")
            self.cut()
            self.send("left")
            self.paste()
            self.send("left")

        for i in range(length*2):
            self.send("right")
            
    def virtual_console(self):
        self.mod(["ctrl", "alt"], "f1")
    
    def xwindows(self):
        self.mod(["ctrl", "alt"], "f8")
    
    def jitter(self, scale=5, duration=25, frequency=30):
        try:
            while True:
                for i in range(randint(0, duration)):
                    self.mouse_move(randint(-scale, scale),
                                    randint(-scale, scale))
                time.sleep(randint(0, frequency))
        except KeyboardInterrupt:
            pass
