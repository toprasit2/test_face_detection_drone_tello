#===================================================================================
#
# FileName: updown.py
#
# Summary:  This program sends following commands to a drone
#             - takeoff
#             - down
#             - land
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
    dronecontroller.wait_for_connection(10.0)

    # sending commands to the drone
    dronecontroller.takeoff()
    sleep(5)
    dronecontroller.down(50)
    sleep(3)
    dronecontroller.land()
    sleep(5)

    # Stop Drone
    dronecontroller.disconnect()

#===================================================================================
# Start up
import framework
if __name__ == '__main__':
    _framework = framework.Framework(main)
    _framework.run()
