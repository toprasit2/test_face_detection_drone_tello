#===================================================================================
#
# FileName: modeling_csvseq.py
#
# Summary:  This program controls drone accroding to specified csv file
#
#===================================================================================
# setting library path
import sys
sys.path.append('./../lib')

# importing library
from time import sleep
import csv
import drone_controller
import ar_checker

#===================================================================================
# Command class
#===================================================================================
class Command:
    def __init__(self, type, parameter):
        self.type = type
        self.parameter = parameter

#===================================================================================
# CSVSequencer class
#===================================================================================
class CSVSequencer:
    def __init__(self, dronecontroller, archecker, commands):
        self._framework = framework.Framework(main)
        self.dronecontroller = dronecontroller
        self.archecker = archecker
        self.commands = commands

    def initialize(self):
        # Start Drone
        self.dronecontroller.connect()
        self.dronecontroller.wait_for_connection(20.0)
        self.archecker.start_armcheck()

    def run(self):
        for command in self.commands:
            if command.type == 'takeoff':
                self.dronecontroller.takeoff()
            elif command.type == 'down':
                self.dronecontroller.down(command.parameter)
            elif command.type == 'up':
                self.dronecontroller.up(command.parameter)
            elif command.type == 'land':
                self.dronecontroller.land()
            elif command.type == 'sleep':
                sleep(command.parameter)
            else:
                print(command.type + command.parameter)
            # added more commands!

            self.arid_check()

    # check AR marker
    def arid_check(self):
        ids = self.archecker.get_finded_ids()
        for id in ids:
            print('Detected ArMark ID = ', id)

    def stop(self):
        # Stop Drone
        self.dronecontroller.disconnect()
        self.archecker.stop_armcheck()

#===================================================================================
# Main function
def csv2command(file):
    commands = []
    with open('commands.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 2:
                commands.append(Command(row[0], int(row[1])))
            elif len(row) == 1:
                commands.append(Command(row[0], 0))

    return commands

def main(dronecontroller, archecker, cmdrecoder, keymanager):
    commands = csv2command('commands.csv')
    cs = CSVSequencer(dronecontroller, archecker, commands)
    cs.initialize()
    cs.run()
    cs.stop()


#===================================================================================
# Start up
import framework
if __name__ == '__main__':
    _framework = framework.Framework(main)
    _framework.run()
