import tuio
import numpy as np
import cv2
import time
import serial
from datetime import datetime
from miscfunc import *

class Bot:
  """
  properties:
    id = (orange|yellow|green)
    ser = opened com port
    cx, cy = center coordinates
    dx, dy = destionation point
  """

  def __init__(self, id, com):
    self.id = id
    self.ser = serial.Serial()
    self.ser.baudrate = 9600
    self.ser.port = com
   # self.ser.open()

  def __del__(self):
    # uncoment when needed
    #self.ser.close()
    print "good bye {}".format(self.id)

  def setCenter(self, xpos, ypos):
    self.cx = xpos
    self.cy = ypos

  def getCenter(self):
    return [self.cx, self.cy]

  def setAngle(self, angle):
    self.angle = np.floor(angle*100) / 100

  def getAngle(self):
    return self.angle

  def setDestination(self, dest):
    self.dx = dest[0]
    self.dy = dest[1]

  def getDestination(self):
    return [self.dx, self.dy]

  def moveForward(self):
    print "moving forward"
    if self.ser.isOpen():
      self.ser.write('w')

  def moveRight(self):
    print "moving right"
    if self.ser.isOpen():
      self.ser.write('d')

  def moveLeft(self):
    print "moving left"
    if self.ser.isOpen():
      self.ser.write('a')

ID0 = 3
ID1 = 4
ID2 = 6
tracking = tuio.Tracking()
#print "loaded profiles:", tracking.profiles.keys()
#print "list functions to access tracked objects:", tracking.get_helpers()

img = np.zeros((HEIGHT, WIDTH, 3), np.uint8)
cv2.namedWindow("output")
cv2.resizeWindow("output", 640 , 480)
out = cv2.VideoWriter('output.avi', -1, 5.0, (640,480))

# file for store points
pointsFile = open("coordinates.txt", "a")
pointsFile.write('bot\tangle\tCX\tCY\tDX\tDY\n')

bots = []
bots.append(Bot(ID0, "COM3"))
bots.append(Bot(ID1, "COM7"))
bots.append(Bot(ID2, "COM9"))

formationsready = False

try:
  while 1:
    cv2.rectangle(img, (0,0), (WIDTH, HEIGHT), (255,255,255), -1)
    #dt = datetime.now()
    for i in range(0, 200):
      tracking.update()
      time.sleep(0.001)
    #print "Time delta is ", datetime.now() - dt

    # find centers
    length = 0
    cid = 0
    for obj in tracking.objects():
      print "id: {} X, Y = ({}, {}), angle = {}".format(obj.id, obj.xpos, obj.ypos, obj.angle)
      if obj.id == ID0:
        cid = 0
        length += 1
      elif obj.id == ID1:
        cid = 1
        length += 1
      elif obj.id == ID2:
        cid = 2
        length += 1

      bots[cid].setCenter(obj.xpos, obj.ypos)
      bots[cid].setAngle(translateAngle(obj.angle))
      point1 = bots[cid].getCenter()
      point1 = [int(point1[0] * WIDTH), HEIGHT - int(point1[1] * HEIGHT)]
      cv2.line(img, tuple(point1), tuple(getSecondPointForLine(bots[cid].getCenter(), bots[cid].getAngle())), (255,0,0), 2)
      cv2.putText(img, "%.2f" % bots[cid].getAngle(), tuple(point1), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0))

  #  print "After for obj loop. length is {}".format(length)
    #time.sleep(0.2)
    #continue

    if length != 3:
      continue

    lengths_between_bots = []
    for i in range(3):
      length = calculateLength(bots[i % 3].getCenter(), bots[(i+1)%3].getCenter())
      lengths_between_bots.append(length)

    print lengths_between_bots

    if checkFormation(lengths_between_bots):  # formation is settled 
      print "Formation's ready!"
      sideLength = lengths_between_bots[0]
      triangleCenter = getCenterOfTriangle(bots)
      destPoint = (0.8, 0.8) # is set by supervisor
      L = calculateLength(triangleCenter, destPoint)
      phi = np.arctan2(-(destPoint[1] - triangleCenter[1]), (destPoint[0] - triangleCenter[0]))
      dx = L * np.cos(phi)
      dy = L * np.sin(phi)

      for i in range(3):
        (x, y) = bots[i].getCenter()
        bots[i].setDestination((x + dx, y + dy))

        # for visualization
        point1 = (int(x * WIDTH), HEIGHT - int(y * HEIGHT))
        point2 = (int((x+dx) * WIDTH), HEIGHT - int((y+dy) * HEIGHT))
        cv2.line(img, point1, point2, (0, 255, 255), 2)

    else:
      print "Working on formation..."
      # find destination points by means of IET
      for i in range(3):
        center1 = bots[(i + 1) % 3].getCenter()
        center2 = bots[(i + 2) % 3].getCenter()
        bots[i].setDestination(calculateDestination(center1, center2))

        # debug information, for visualization
        point1 = bots[i].getCenter()
        point1 = (int(point1[0] * WIDTH), HEIGHT - int(point1[1] * HEIGHT))
        point2 = bots[i].getDestination()
        point2 = (int(point2[0] * WIDTH), HEIGHT - int(point2[1] * HEIGHT))
        cv2.line(img, point1, point2, (0, 255, 255), 2)

    wasrotation = False
    for bot in bots:
      print "Writing bot's angle, center and destionation"
      (CX, CY) = bot.getCenter()
      (DX, DY) = bot.getDestination()
      pointsFile.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(bot.id, bot.getAngle(), CX, CY, DX, DY))
      if calculateLength(bot.getCenter(), bot.getDestination()) > 0.1:
        deltaangle, destangle = getDeltaAngle(bot)

        print "id {} deltaangle is {}".format(bot.id, deltaangle)
        point = bot.getDestination()
        point = (int(point[0] * WIDTH), HEIGHT - int(point[1] * HEIGHT))
        cv2.putText(img, "%.2f" % destangle, point, cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0))

        if deltaangle > 10:
          bot.moveRight()
          wasrotation = True
          time.sleep(0.1)

        if deltaangle < -10:
          bot.moveLeft()
          wasrotation = True
          time.sleep(0.1)

    if wasrotation == False:
      for bot in bots:
        if calculateLength(bot.getCenter(), bot.getDestination()) > 0.2:
          bot.moveForward()

    cv2.imshow("output", img)
    out.write(img)
    cv2.waitKey(60)

except KeyboardInterrupt:
  tracking.stop()

out.release()
cv2.destroyAllWindows()
pointsFile.close()
