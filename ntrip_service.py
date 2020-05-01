
import time
import subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
STline = 1 #line index to pull mount point from source table
ntripstatus = 0
mountpnt = "notstarted"

def button_up(channel):
    global ntripstatus
    global STline
    if(ntripstatus == 0):
       STline += 1
       cmd = 'sed -n -e "{}"p '.format(STline)
       mountpnt = subprocess.check_output(cmd+'/home/pi/pitrip/source_table.txt', shell=True).decode("utf-8")
       print(mountpnt)
       f= open("mountpnt.txt","w+")
       f.write(mountpnt)

def button_down(channe1):
    global ntripstatus
    global STline
    if(ntripstatus == 0):
       STline -= 1
       cmd = 'sed -n -e "{}"p '.format(STline)
       mountpnt = subprocess.check_output(cmd+'/home/pi/pitrip/source_table.txt', shell=True).decode("utf-8")
       print(mountpnt)
       f= open("mountpnt.txt","w+")
       f.write(mountpnt)

def button_enter(channel):
    global ntripstatus
    global mountpnt
    if(ntripstatus == 0):
       ntripstatus = 1
       f= open("ntripstatus.txt","w+")
       f.write("NTRIP Running")
       cmd = '/home/pi/pitrip/ntripclient -s SERVER -r PORT -u USER -p PASSWORD -m "{}" -D /dev/ttyUSB0 -B 115200 &'.format(mountpnt)
       proc=subprocess.call(cmd, shell=True)
       print("NTRIP STARTED")
    else:
       cmd = "pgrep ntrip"
       ntripPID = subprocess.check_output(cmd, shell=True).decode("utf-8")
       cmd = "sudo kill "
       proc = subprocess.check_output(cmd+ntripPID, shell=True).decode("utf-8")
       ntripstatus = 0
       f= open("ntripstatus.txt","w+")
       f.write("NTRIP DOWN")


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use BCM (chip) or BOARD (physical) pin numbering
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin to be an input pin and set initial value to be pulled high (on)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin to be an input pin and set initial value to be pulled high (on)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin to be an input pin and set initial value to be pulled high (on)
GPIO.add_event_detect(26,GPIO.FALLING,callback=button_up, bouncetime=500) # Setup event on pin 26 rising edge
GPIO.add_event_detect(19,GPIO.FALLING,callback=button_down, bouncetime=500) # Setup event on pin 19 rising edge
GPIO.add_event_detect(13,GPIO.FALLING,callback=button_enter, bouncetime=500) # Setup event on pin 13 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
