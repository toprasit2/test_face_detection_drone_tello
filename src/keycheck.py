#===================================================================================
#
# FileName: keycheck.py
#
# Summary:  This program checks to be pressing specific keys.
#
#===================================================================================
# setting library path
import sys
sys.path.append('./../lib')

# importing library
from time import sleep
import key_manager

#===================================================================================
# Program
#===================================================================================
def main(dronecontroller, archecker, cmdrecoder, keymanager):
    while True:
        sleep(0.01)
        #print(keymanager.get_lastkey())        # checking the keycode of the pressed key

        if keymanager.pressed_key('a'):
            print('pressed: ', 'a')
        if keymanager.pressed_key('b'):
            print('pressed: ', 'b')
        if keymanager.pressed_key('x'):
            print('pressed: ', 'x')
        if keymanager.pressed_key('Key.left'):
            print('pressed: ', 'Key.left')
        if keymanager.pressed_key('Key.f1'):
            print('pressed: ', 'Key.f1')
        if keymanager.pressed_key('Key.backspace'):
            print('pressed: ', 'Key.backspace')
        if keymanager.pressed_key('Key.shift'):
            print('pressed: ', 'Key.shift')
        if keymanager.pressed_key('Key.shift_r'):
            print('pressed: ', 'Key.shift_r')
        if keymanager.pressed_key('Key.ctrl_l'):
            print('pressed: ', 'Key.ctrl_l')
        if keymanager.pressed_key("Key.esc"):
            print('pressed: ', 'Key.esc')
            break

#===================================================================================
# Start up
import framework
if __name__ == '__main__':
    _framework = framework.Framework(main)
    _framework.run()
