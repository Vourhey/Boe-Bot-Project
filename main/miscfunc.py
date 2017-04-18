import numpy as np

HEIGHT = 480
WIDTH = 640

def translateAngle(angle):
  return angle
  angle = -angle + 360 + 90
  return angle % 360

def getSecondPointForLine(point, angle):
  x2 = point[0] + 0.1 * np.cos(np.deg2rad(angle))
  y2 = point[1] + 0.1 * np.sin(np.deg2rad(angle))

  return [int(x2 * WIDTH), int(y2 * HEIGHT)]

def calculateDestination(point1, point2):
  x1, y1 = point1[0], point1[1]
  x2, y2 = point2[0], point2[1]
  ROOTOF3 = np.sqrt(3)

  x3 = (x1 + x2 - (y1 - y2) * ROOTOF3) / 2
  y3 = (y1 + y2 - (x2 - x1) * ROOTOF3) / 2

  return (x3, y3)

def calculateLength(tc, tb):
  return np.sqrt((tb[0] - tc[0])**2 + (tb[1] - tc[1])**2)

def getDeltaAngle(bot):
  botangle = bot.getAngle()
  (cx, cy) = bot.getCenter()
  (dx, dy) = bot.getDestination()

  destangle = np.rad2deg(np.arctan2(-(cy - dy), (dx - cx)))
  #destangle += 90

  if destangle < 0:
    destangle += 360

  destangle = translateAngle(destangle)

  print "destangle is {}".format(destangle)
  

  delta = destangle - botangle

  if delta > 180:
    delta = delta - 360
  if delta < -180:
    delta = 360 + delta

  delta = np.floor(delta * 100) / 100
  destangle = np.floor(destangle * 100) / 100
  
  return delta, destangle
