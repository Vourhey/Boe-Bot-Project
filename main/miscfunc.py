import numpy as np

HEIGHT = 480
WIDTH = 640

def translateAngle(angle):
  #print "Before translating %f" % angle
  angle = -angle + 360 + 90
  #print "And after %f" % (angle % 360)
  return angle % 360

def getSecondPointForLine(point, angle):
  x2 = point[0] + 0.1 * np.cos(np.deg2rad(angle))
  y2 = point[1] + 0.1 * np.sin(np.deg2rad(angle))

  return [int(x2 * WIDTH), HEIGHT - int(y2 * HEIGHT)]

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
  #botangle = translateAngle(bot.getAngle())
  botangle = bot.getAngle()
  (cx, cy) = bot.getCenter()
  (dx, dy) = bot.getDestination()

  destangle = np.rad2deg(np.arctan2(-(cy - dy), (dx - cx)))

  if destangle < 0:
    destangle += 360

 # destangle = translateAngle(destangle)

  print "destangle is {}".format(destangle)
  

  delta = botangle - destangle

  if delta > 180:
    delta = delta - 360
  if delta < -180:
    delta = 360 + delta

  delta = np.floor(delta * 100) / 100
  destangle = np.floor(destangle * 100) / 100
  
  return delta, destangle

def checkFormation(lengths):
  for i in range(3):
    if not compare(lengths[i % 3], lengths[(i + 1) % 3]):
      return False

  return True

# +- 5%
def compare(l1, l2):
  if l2 > (l1 * 0.95) and l2 < (l1 * 1.05):
    return True

  return False

def getCenterOfTriangle(bots):
  c1 = bots[0].getCenter()
  c2 = bots[1].getCenter()
  c3 = bots[2].getCenter()

  tc = ((c1[0] + c2[0] + c3[0]) / 3, (c1[1] + c2[1] + c3[1]) / 3)
  return tc
