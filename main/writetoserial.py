import serial
import time

ser = serial.Serial('COM3', 9600)

for i in range(0, 15):
  ser.write('w')
  time.sleep(0.1)

ser = serial.Serial('COM7', 9600)

for i in range(0, 15):
  ser.write('w')
  time.sleep(0.1)

ser = serial.Serial('COM9', 9600)

for i in range(0, 15):
  ser.write('w')
  time.sleep(0.1)

ser.close()
