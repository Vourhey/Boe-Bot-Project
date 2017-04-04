import serial
import time

class Bot:
  """
  properties:
    name = (orange|yellow|green)
    ser = opened com port
    cx, cy = center coordinates
    bx, by = center of blue mark
    dx, dy = destionation point
  """

  def __init__(self, name, com):
    self.name = name
    self.ser = com #serial.Serial(com, 9600, timeout=0)

  def setCenter(self, center):
    self.cx = center[0]
    self.cy = center[1]

  def getCenter(self):
    return (self.cx, self.cy)

  def setBlueMark(self, bluecenter):
    self.bx = bluecenter[0]
    self.by = bluecenter[1]

  def getBlueCenter(self):
    return (self.bx, self.by)

  def setDestination(self, dest):
    self.dx = dest[0]
    self.dy = dest[1]

  def getDestination(self):
    return (self.dx, self.dy)

  def moveForward(self):
    print "moving forward"
    #self.ser.write('w')

  def moveRight(self):
    print "moving right"
    #self.ser.write('d')

  def moveLeft(self):
    print "moving left"
    #self.ser.write('a')
