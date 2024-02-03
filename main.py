
from time import sleep
from machine import Pin
from machine import I2C
from machine import ADC
import time
import VL53L0X
from neopixel import NeoPixel
from dfplayer import *

import random




############## FUNCTIONS ###################

def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def play_record(vol,num):
  df.volume(vol)
  df.play(1, num)


############## MAIN PART ###################


################ TOF SENSOR ###################
sda = 7 # lower right pin
scl = 5 # one up from lower right pin
i2c = I2C(0, scl=5, sda=7, freq=400000)

distance = 0

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c)
    

################ LED ###################
channel = I2C(0)
len = 134
i=0
blue_map = 3
green_map = 3
red_map = 3

np = NeoPixel(Pin('A4', Pin.OUT), len)


################ MOISTURE SENSOR ###################
moisture = ADC('A0')


################ MP3 Player ###################
df = DFPlayer(0, 'D1', 'D0')


while True:
  
  tof.start()
  distance = tof.read()
  print(distance)
  tof.stop()

  moisture_value = moisture.read()
  print(moisture_value)
  if moisture_value > 2000:
    moisture_value = 1999

  blue_map = convert(moisture_value, 0, 2000, 10, 200);
  red_map = convert(moisture_value, 0, 2000, -118, -4)*(-1);
  green_map = convert(moisture_value, 0, 2000, -101, -4)*(-1);

  
  ##################### START USER FLOWS ########################

  ######## user is near the flower ########
  if distance < 1000:
    
    ##### the soil is dry #####
    if moisture_value < 300:
     print('moisture low value', moisture_value)
     play_record(35, 7)
      
     while moisture_value < 1000:
      play_record(35, 7)
      moisture_value = moisture.read()
      blue_map = convert(moisture_value, 0, 2000, 10, 200);
      red_map = convert(moisture_value, 0, 2000, -118, -4)*(-1);
      green_map = convert(moisture_value, 0, 2000, -101, -4)*(-1);
      i = 0
      while i < len:
        np[i] = (red_map, green_map, blue_map)
        i+=1
        np.write()
      sleep(5)
     sleep(1)
     play_record(15, 6)
    
          
    ##### soil is wet #####
    else:    
      print('hight value', moisture_value)
      i=0
      while i < len:
        np[i] = (random.randint(50, 155), random.randint(50, 155), random.randint(50, 255))
        i+=1
        np.write()   
      sleep(5)
    
  ######## user is far from soil ########
  else:
    while i < len:
      np[i] = (0, 0, 0)
      i+=1
      np.write() 
    i=0
    
 

  