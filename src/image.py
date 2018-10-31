#===================================================================================
#
# FileName: image.py
#
# Summary:  This program shows the movie of the drone camera
#           and finds AR Markers
#
#===================================================================================
# setting library path
import sys
sys.path.append('./../lib')

# importing library
from time import sleep
import drone_controller
import ar_checker

#===================================================================================
# Program
#===================================================================================
def main(dronecontroler, archecker, cmdrecoder, keymanager):
    # Initialization
    dronecontroler.connect()
    archecker.start_armcheck()

    # Printting AR Markers ID
    while True:
        sleep(0.01)
        ids = archecker.get_finded_ids()
        for id in ids:
            print('Detected ArMark ID = ', id)
        archecker.reset_ids()

    # Finalization
    archecker.stop_armcheck()
    dronecontroler.disconnect()

#===================================================================================
# Start up
import framework
if __name__ == '__main__':
    _framework = framework.Framework(main)
    _framework.run()
