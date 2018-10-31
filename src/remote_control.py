#===================================================================================
#
# FileName: remote_control.py
#
# Summary:  This program operates a drone by remote control with keyboard.
#
#===================================================================================
# setting library path
import sys
sys.path.append('./../lib')

# importing library
from time import sleep
import framework
import drone_controller
import cmd_recorder
import key_manager

#===================================================================================
# Program
#===================================================================================
def main(dronecontroller, archecker, cmdrecoder, keymanager):
    # Initialization
    dronecontroller.connect()
    archecker.start_armcheck()

    while True:
        sleep(0.01)
        condition = dronecontroller.get_condition()

        # takeoff or land of exit
        if keymanager.pressed_key('t'):
            cmdrecoder.save_cmd('t')
            dronecontroller.takeoff()
        elif keymanager.pressed_key('l'):
            cmdrecoder.save_cmd('l')
            dronecontroller.land()
        elif keymanager.pressed_key("Key.esc"):
            cmdrecoder.save_cmd("Key.esc")
            if condition == 1:
                dronecontroller.land()
            break

        # moving commands
        speed_forward = 0
        speed_rightleft = 0
        speed_clockwise = 0
        if condition == 1:
            if keymanager.pressed_key("Key.left"):
                cmdrecoder.save_cmd("Key.left")
                speed_rightleft = -20
            if keymanager.pressed_key("Key.right"):
                cmdrecoder.save_cmd("Key.right")
                speed_rightleft = 20
            if keymanager.pressed_key("Key.up"):
                cmdrecoder.save_cmd("Key.up")
                speed_forward = 20
            if keymanager.pressed_key("Key.down"):
                cmdrecoder.save_cmd("Key.down")
                speed_forward = -20
            if keymanager.pressed_key('r'):
                cmdrecoder.save_cmd('r')
                speed_clockwise = 45
            if keymanager.pressed_key('e'):
                cmdrecoder.save_cmd('e')
                speed_clockwise = -45

        # moveing drone
        if speed_forward < 0:
            dronecontroller.backward(-speed_forward)
        else:
            dronecontroller.forward(speed_forward)

        if speed_rightleft < 0:
            dronecontroller.left(-speed_rightleft)
        else:
            dronecontroller.right(speed_rightleft)

        if speed_clockwise < 0:
            dronecontroller.counter_clockwise(-speed_clockwise)
        else:
            dronecontroller.clockwise(speed_clockwise)

    # saving all sended commands to the csv file
    cmdrecoder.write_csv('cmdout.csv')

    # Finalization
    archecker.stop_armcheck()
    dronecontroller.disconnect()

#===================================================================================
# Start up
if __name__ == '__main__':
    _framework = framework.Framework(main)
    _framework.run()
