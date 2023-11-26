import schedule
import time
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
from dateutil import tz
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append("/rpi-rgb-led-matrix/bindings/python")
from rgbmatrix import RGBMatrix, RGBMatrixOptions

light_pink = (255,219,218)
dark_pink = (219,127,142)
white = (230,255,255)

salmon = (255,150,162)
tan = (255,205,178)
orange_tinted_white = (248,237,235)

washed_out_navy = (109,104,117)

discordColor = (150,170,255)
messengerColor = (60, 220, 255)
snapchatColor = (255, 252, 0)
smsColor = (110, 255, 140)

spotify_color = (0,255,0)

font = ImageFont.truetype("fonts/tiny.otf", 5)

background = Image.open("backgrounds/sakura-bg.png").convert("RGB")

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.brightness = 100
options.pixel_mapper_config = "U-mapper;Rotate:180"
options.gpio_slowdown = 2
options.pwm_lsb_nanoseconds = 80
options.limit_refresh_rate_hz = 150
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'
options.drop_privileges = False
matrix = RGBMatrix(options = options)

def padToTwoDigit(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)

def printTime():
    frame = background.copy()
    draw = ImageDraw.Draw(frame)

    currentTime = datetime.now(tz=tz.tzlocal())
    month = currentTime.month
    day = currentTime.day
    dayOfWeek = currentTime.weekday() + 1
    hours = currentTime.hour
    minutes = currentTime.minute

    draw.text((3, 6), padToTwoDigit(hours), light_pink, font=font)
    draw.text((10, 6), ":", light_pink, font=font)
    draw.text((13, 6), padToTwoDigit(minutes), light_pink, font=font)
    # Put the date here as DD/MM/YYYY
    draw.text((3, 12), padToTwoDigit(day), dark_pink, font=font)
    draw.text((6, 12), "/", dark_pink, font=font)
    draw.text((8, 12), padToTwoDigit(month), dark_pink, font=font)
    draw.text((11, 12), "/", dark_pink, font=font)
    draw.text((13, 12), str(currentTime.year), dark_pink, font=font)



    matrix.SetImage(frame)

printTime()

schedule.every(10).seconds.do(printTime)
while True:
    schedule.run_pending()
    time.sleep(1)