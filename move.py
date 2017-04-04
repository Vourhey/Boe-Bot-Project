import serial
import time

ser = serial.Serial('COM4', 9600, timeout=0)
print ser.isOpen()

# w - forward
# d - right
# a - left
# s - backward
moves = ['w'] * 100 + ['d'] * 50 + ['w'] * 50

for m in moves:
  print m 
  ser.write(m)
  # sleep 

ser.close()
