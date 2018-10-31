#===================================================================================
#
# FileName: key_manager.py
#
# Summary:  This program provides functions for checking the keyboard statas
#
#===================================================================================

import time
from pynput.keyboard import Key, Listener

class KeyManager:
    __pressed = { "a" : False, "b" : False }
    __lastkey = ''

    def initialize(self):
        listener = Listener(on_press = self.__on_press, on_release= self.__on_release)
        listener.start()

    def pressed_key(self, key):
        return self.__pressed.get(key, False)

    def get_lastkey(self):
        return self.__lastkey.replace("'", "")

    def __on_press(self, key):
        if self.__pressed.get(str(key), False) == True:
            return
        else:
            try:
                keycode = str(key).replace("'", "")
                self.__pressed[keycode] = True
            except AttributeError:
                pass
            self.__pressed[str(key)] = True
            self.__lastkey = str(key)

    def __on_release(self, key):
        if self.__pressed.get(str(key), False) == False:
            return
        else:
            try:
                keycode = str(key).replace("'", "")
                self.__pressed[keycode] = False
            except AttributeError:
                pass
            self.__pressed[str(key)] = False
