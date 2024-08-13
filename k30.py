# General

# Packages
import time
import os
from datetime import datetime
import serial
import signal
import sys
import RPi.GPIO as GPIO

# Changes current working directory to the Micro SD Card (or wherever you want really)
# I'm sure there's a better way to do it but this value is hardcoded for now
destination = '/home/ashoch/lamont/data' # This is the specific path to the specific MSD on this raspb
# To change destination, change this string to the filepath to any drive/directory
os.chdir(destination)

# Designates which pin the GPIO is on
BUTTON_GPIO = 36 # make sure setmode(GPIO.BOARD) below

# GPS reader, unsure if which port matters
#gps = open('/dev/ttyACM0')

def get_time():
    now = datetime.now()
    return now.strftime("%F_%H%M")

# Helper program to terminate program from commandline for debugging
def signal_handler(sig, frame): 
    GPIO.cleanup()
    sys.exit(0)

def button_callback(channel):
    if not GPIO.input(BUTTON_GPIO):

        # Run state condition
        global run_condition
        run_condition = True

        # Will output file (can change this later)
        #now = datetime.now()
        # Sets date and time in YYYY/MM/DD/TIME format
        date_and_time = get_time() #now.strftime("%F_%H%M")
        # Output filename will always reflect the time the program was initially started
        outputfilename = "gas_%s.csv" % date_and_time
        output = open(outputfilename, "a")
        if os.stat(outputfilename).st_size == 0: # If the output is empty, initial line with labels will be written
            output.write("Date, Time, Lattitude, Longitude, CO2 Value\n")
        output.close() # Closes output for now, each iteration of a drawn line will open it again

        currline = "" # Buffer

        ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout = .5)
        print("AN-137 RP3 to K-30")
        ser.flushInput()
        linecounter = 0
        gps = open('/dev/ttyACM0')
        time.sleep(1)
        for line in gps: 
            '''RMC line contains time in GMT, 
            lattitude, longitude, and date in
            DD/MM/YYYY format'''
            if "RMC" in line:

                output = open(outputfilename, "a")

                ser.write(b'\xFE\x44\x00\x08\x02\x9F\x25') # Blips binary to the sensor to tell it what we want
                resp = ser.read(7)
                high = resp[3]
                low = resp[4]
                co2 = (high*256) + low

                # Once we have all those values, we are going to put them in a line and spit them out
                split = line.split(',')
                date = split[9] 
                curtime = split[1]
                lat = split[3]
                latsign = split[4]
                long = split[5]
                longsign = split[6]
                carbon_dioxide_value = str(co2) 

                currline = "%s, %s, %s %s , %s %s , %s\n" % (date, curtime, lat, latsign, long, longsign, carbon_dioxide_value)

                output.write(currline) # Writes line by line to the results.csv file
                # Debugging, will print each line to terminal before the output gets closed
                print(currline)
                output.close() # Closes the output 
                linecounter+=1
                if GPIO.input(BUTTON_GPIO):
                    print("Stopping output!")
                    gps.close()
                    break

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(BUTTON_GPIO, GPIO.BOTH, 
                          callback=button_callback, bouncetime=25)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
