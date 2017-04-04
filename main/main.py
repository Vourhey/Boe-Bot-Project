import numpy as np
import cv2
from pprint import pprint
from time import sleep
from botclass import Bot

def getboxes(img, b_tuple, count):
  lower = np.array(b_tuple[0], dtype = "uint8")
  upper = np.array(b_tuple[1], dtype = "uint8")

  mask = cv2.inRange(img, lower, upper)
  mask = cv2.erode(mask, None, iterations=1)
  mask = cv2.dilate(mask, None, iterations=1)
  mask = cv2.blur(mask, (7,7))
  mask = cv2.bilateralFilter(mask, 5, 20, 20)
  
  contours, _ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key = cv2.contourArea, reverse = True)[:count]
  
  # example of one box
  # box = array([[ 74, 318],
  #              [ 68, 186],
  #              [147, 183],
  #              [153, 315]])]
  boxes = []
  for i in range(0, count):
    rect = cv2.minAreaRect(contours[i])
    box = cv2.cv.BoxPoints(rect)
    box = np.int0(box)
    boxes.append(box)

  return boxes

# takes rectangle as 4 points and returns the center point
def center(b):
  cx = int((b[0][0] + b[2][0]) / 2)
  cy = int((b[0][1] + b[2][1]) / 2)
  return (cx,cy)

def calculateLength(tc, tb):
  return np.sqrt((tb[0] - tc[0])**2 + (tb[1] - tc[1])**2)

def calculateDestination(point1, point2):
  x1, y1 = point1[0], point1[1]
  x2, y2 = point2[0], point2[1]
  ROOTOF3 = np.sqrt(3)

  x3 = (x1 + x2 - (y1 - y2) * ROOTOF3) / 2
  y3 = (y1 + y2 - (x2 - x1) * ROOTOF3) / 2

  return (int(x3), int(y3))

def getDeltaAngle(bot):
  (cx, cy) = bot.getCenter()
  (bx, by) = bot.getBlueCenter()
  (dx, dy) = bot.getDestination()

  bottan = float(-(by - cy))/(bx - cx)
  botangle = np.rad2deg(np.arctan(bottan))

  print "botangle befor if: {}".format(botangle)
  
  if bx < cx:
    botangle = botangle + 180
  elif by > cy:
    botangle = botangle + 360

  desttan = float(-(dy - cy))/(dx - cx)
  destangle = np.rad2deg(np.arctan(desttan))

  print "destangle befor if: {}".format(destangle)

  if dx < cx:
    destangle = destangle + 180
  elif dy > cy:
    destangle = destangle + 360

  print "botangle = {} destangle = {}".format(botangle, destangle)

  delta = botangle - destangle
  if delta > 180:
    return delta - 360
  elif delta < -180:
    return 360 + delta
  else:
    return delta

# reading image
img = cv2.imread('img\\07.jpg')
# resizing to fit the display
resized_image = cv2.resize(img, None, fx=0.15, fy=0.15, interpolation = cv2.INTER_CUBIC)
resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

output = resized_image.copy()

cv2.imshow("ii", resized_image)
cv2.waitKey(0)

# define main structure
bots = []
bots.append(Bot("orange", "COM3"))
bots.append(Bot("yellow", "COM4"))
bots.append(Bot("green", "COM5"))

#define boundaries
color_boundaries = [
  ([90, 107, 93], [155, 217, 161]), # blue
  ([0, 44, 117], [14, 168, 200]),  # orange
  ([16, 100, 176], [65, 189, 238]), # yellow
  ([65, 100, 80], [89, 178, 162])  # green
]

# find bots and rectangles around them
botsboundaries = [] # orange, yellow and green boxes
for i in range(1, 4):
  boundary = getboxes(output, color_boundaries[i], 1)
  #bots[i-1].setCenter(center(boundary))
  botsboundaries.append(boundary[0])

# and find centers of bots
for i in range(0,3):
  bots[i].setCenter(center(botsboundaries[i]))
  cv2.circle(resized_image, bots[i].getCenter(), 3, (0,255,0))
  cv2.putText(resized_image, repr(bots[i].getCenter()), bots[i].getCenter(), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0))

# blue marks
bluemarks = getboxes(output, color_boundaries[0], 3)

# find centers of blue marks
bluecenters = []
for i in range(0, 3):
  bluecenters.append(center(bluemarks[i]))
  cv2.circle(resized_image, center(bluemarks[i]), 2, (0,0,255))

cv2.drawContours(resized_image, bluemarks, -1, (255,0,0), 2)
#cv2.imshow("ii", resized_image)
#cv2.waitKey(0)

# now I have to match nearest blue mark with its bot
for idb in range(len(bots)):
  tuplecenter = bots[idb].getCenter()
  minlen = 10000000 # it a real big length
  nearestbluedot = ()
  for tupleblue in bluecenters:
    length = calculateLength(tuplecenter, tupleblue)
    if length < minlen:
      nearestbluedot = tupleblue
      minlen = length

  bots[idb].setBlueMark(nearestbluedot)

# now we have a right structure with centers of bots and directions
# for every bot I calculate its direction (point)

bots[0].setDestination(calculateDestination(bots[1].getCenter(), bots[2].getCenter()))
bots[1].setDestination(calculateDestination(bots[2].getCenter(), bots[0].getCenter()))
bots[2].setDestination(calculateDestination(bots[0].getCenter(), bots[1].getCenter()))

for bot in bots:
  cv2.circle(resized_image, bot.getDestination(), 3, (0,255,0))

cv2.imshow("ii", resized_image)

# now I have to find angles between destination and bot's direction
for bot in bots:
  deltaangle = getDeltaAngle(bot)

  print "for bot {} deltaangle is {}".format(bot.getCenter(), deltaangle)

  if abs(deltaangle) < 5:
    bot.moveForward() 
  elif deltaangle > 0:
    bot.moveRight()
  else:
    bot.moveLeft()
  sleep(0.2)

cv2.waitKey(0)  
cv2.destroyAllWindows()
