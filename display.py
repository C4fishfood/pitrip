import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 270

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
#stty -F /dev/ttyUSB1 speed 115200

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")


#    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
#    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
#    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
#    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    proc=subprocess.call('echo log bestpos once > /dev/ttyUSB1',shell=True)
    cmd = "tail -1 poslog.txt | cut -f7 -d' '"
    SOL = subprocess.check_output(cmd,shell=True).decode("utf-8")
    cmd = "tail -1 poslog.txt | cut -f17 -d' '"
    DIFFAGE = subprocess.check_output(cmd,shell=True).decode("utf-8")
    DIFFAGE2 = DIFFAGE.split(".",1)
    DIFFAGE3 = DIFFAGE2[0]
    cmd = "cat /home/pi/ntrip/mountpnt.txt"
    MOUNT = "Base ID: " + subprocess.check_output(cmd,shell=True).decode("utf-8")
    cmd = "tail -1 poslog.txt | cut -f10 -d' '"
    ELEV = "Elev: " + subprocess.check_output(cmd,shell=True).decode("utf-8")
    cmd = "tail -1 poslog.txt | cut -f13 -d' '"
    STDDEVX = "Std.Dev X: " + subprocess.check_output(cmd,shell=True).decode("utf-8")
    cmd = "tail -1 poslog.txt | cut -f14 -d' '"
    STDDEVY = "Std.Dev Y: " + subprocess.check_output(cmd,shell=True).decode("utf-8")
    cmd = "tail -1 poslog.txt | cut -f15 -d' '"
    STDDEVZ = "Std.Dev Z: " + subprocess.check_output(cmd,shell=True).decode("utf-8")
    cmd = "cat /home/pi/ntrip/ntripstatus.txt"
    NTRIPSTATUS = subprocess.check_output(cmd,shell=True).decode("utf-8")


    # Write lines of text.
    y = top
    draw.text((x, y), IP, font=font, fill="#FFFFFF")
    draw.text((x+100, y), NTRIPSTATUS, font=font, fill="#FFFFFF")
    y += font.getsize(IP)[1]
    draw.text((x, y), MOUNT, font=font, fill="#FFFFFF")
    draw.text((x+180, y), DIFFAGE3, font=font, fill="#FFFFFF")
    draw.text((x+200, y), "sec", font=font, fill="#FFFFFF")
    y += font.getsize(MOUNT)[1]
    draw.text((x, y), SOL, font=font, fill="#FF0000")
    y += font.getsize(SOL)[1]
    draw.text((x, y), ELEV, font=font, fill="#ffff00")
    y += font.getsize(ELEV)[1]
    draw.text((x, y), STDDEVX, font=font, fill="#66ff99")
    y += font.getsize(STDDEVX)[1]
    draw.text((x, y), STDDEVY, font=font, fill="#00ffff")
    y += font.getsize(STDDEVY)[1]
    draw.text((x, y), STDDEVZ, font=font, fill="#ff00ff")
    y += font.getsize(STDDEVZ)[1]

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.1)
