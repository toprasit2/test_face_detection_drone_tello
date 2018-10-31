#===================================================================================
#
# FileName: get_state.py
#
# Summary:  This program gets state of a drone about following
#             - height
#             - fly_mode
#             - battery_percentage
#             - drone_battery_left
#
#===================================================================================
# setting library path
import sys
sys.path.append('./../lib')

# importing library
from time import sleep
import drone_controller

#===================================================================================
# Program
#===================================================================================
def main(dronecontroller, archecker, cmdrecoder, keymanager):
    # Start Drone
    dronecontroller.connect()

    while True:
        sleep(1)
        print(dronecontroller.get_flight_data())
        print('height:             ', dronecontroller.get_height())
        print('fly mode:           ', dronecontroller.get_fly_mode())
        print('battery percentage: ', dronecontroller.get_battery_percentage())
        print('drone_battery_left: ', dronecontroller.get_drone_battery_left())
        print('')

    # Stop Drone
    dronecontroller.disconnect()

#===================================================================================
# Start up
import framework
if __name__ == '__main__':
    _framework = framework.Framework(main)
    _framework.run()
