import numpy as np
import cv2
from pprint import pprint
from time import sleep

def getboxes(img, b_tuple, count):
  lower = np.array(b_tuple[0], dtype = "uint8")
  upper = np.array(b_tuple[1], dtype = "uint8")

  mask = cv2.inRange(img, lower, upper)
  mask = cv2.erode(mask, None, iterations=1)
  mask = cv2.dilate(mask, None, iterations=1)
  output = cv2.bitwise_and(img, img, mask = mask)

 # output = cv2.resize(output, None, fx = 0.1, fy = 0.1, interpolation = cv2.INTER_CUBIC)
  #cv2.imshow("ii", np.hstack([img, output]))
  #cv2.waitKey(0)

  gray_img = mask.copy() #cv2.cvtColor(output, cv2.COLOR_HSV2GRAY)
  gray_img = cv2.blur(gray_img, (7,7))
  edged = cv2.bilateralFilter(gray_img, 25, 20, 20)
  #edged = cv2.Canny(gray_img, 50, 240)
  #edged = cv2.blur(edged, (5,5))
  #cv2.imshow("ii", edged)
  #cv2.waitKey(0)

  contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  #cv2.drawContours(img, contours, -1, (0,255,0), 3)
  contours = sorted(contours, key = cv2.contourArea, reverse = True)[:count]
  #cv2.drawContours(img, contours, -1, (0,255,0), 3)
  #cv2.imshow("ii", img)
  #cv2.waitKey(0)

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

  #pprint(boxes)
  return boxes

def center(b):
  cx = int((b[0][0] + b[2][0]) / 2)
  cy = int((b[0][1] + b[2][1]) / 2)
  return (cx,cy)

def calculateLength(tc, tb):
  return np.sqrt((tb[0] - tc[0])**2 + (tb[1] - tc[1])**2)

def calculateDestination(point1, point2):
  x1, y1 = point1[0], point1[1]
  x2, y2 = point2[0], point2[1]
  rootof3 = np.sqrt(3)

  x3 = (x1 + x2 - (y1 - y2) * rootof3) / 2
  x3 = int(x3)

  y3 = (y1 + y2 - (x2 - x1) * rootof3) / 2
  y3 = int(y3)

  return (x3, y3)

def getDeltaAngle(bot):
  cx, cy = bot[0][0], bot[0][1]
  bx, by = bot[1][0], bot[1][1]
  dx, dy = bot[2][0], bot[2][1]

  bottan = float(-(by - cy))/(bx - cx)
  botangle = np.arctan(bottan)
  botangle = np.rad2deg(botangle)

  print "botangle befor if: {}".format(botangle)
  
  if bx < cx:
    botangle = botangle + 180
  elif by > cy:
    botangle = botangle + 360

  desttan = float(-(dy - cy))/(dx - cx)
  destangle = np.arctan(desttan)
  destangle = np.rad2deg(destangle)

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

#define boundaries
boundaries = [
  ([90, 107, 93], [155, 217, 161]), # blue
  ([0, 44, 117], [14, 168, 200]),  # orange
  ([16, 100, 176], [65, 189, 238]), # yellow
  ([65, 100, 80], [89, 178, 162])  # green
]

# blue marks
bluemarks = getboxes(output, boundaries[0], 3)
pprint(bluemarks)

# find centers of blue marks
bluecenters = []
for i in range(0, 3):
  bluecenters.append(center(bluemarks[i]))
  cv2.circle(resized_image, center(bluemarks[i]), 2, (0,0,255))

cv2.drawContours(resized_image, bluemarks, -1, (255,0,0), 2)
#cv2.imshow("ii", resized_image)
#cv2.waitKey(0)

# find bots and rectangles around them
botsboundaries = [] # orange, yellow and green boxes
for i in range(1, 4):
  boundary = getboxes(output, boundaries[i], 1)
  botsboundaries.append(boundary[0])

pprint(botsboundaries)

# and find centers of bots
botscenters = []
for i in range(0,3):
  botscenters.append(center(botsboundaries[i]))
  cv2.circle(resized_image, center(botsboundaries[i]), 3, (0,255,0))
  cv2.putText(resized_image, repr(botscenters[i]), botscenters[i], cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0))

cv2.drawContours(resized_image, botsboundaries, -1, (255,0,0), 2)
#cv2.imshow("ii", resized_image)
#cv2.waitKey(0)

pprint(botscenters)

# bots struct:
# array([(center of bot), (center of its blue mark), (destination point)], # orange
#       [(cx, cy), (bx, by), (dx, dy)], # yellow
#       [(cx, cy), (bx, by), (dx, dy)]) # green

# now I have to match nearest blue mark with its bot
botstruct = []
for tuplecenter in botscenters:
  #lengths = []
  minlen = 10000000 # it a real big length
  nearestbluedot = ()
  for tupleblue in bluecenters:
    length = calculateLength(tuplecenter, tupleblue)
    if length < minlen:
      nearestbluedot = tupleblue
      minlen = length

  botstruct.append([tuplecenter, nearestbluedot])
  
pprint(botstruct)

# now we have a right structure with centers of bots and directions

for bot in botstruct:
  cv2.line(resized_image, bot[0], bot[1], (0,245, 68))

cv2.imshow("ii", resized_image)
cv2.waitKey(0)

# for every bot I calculate its direction (point)
botstruct[2].append(calculateDestination(botstruct[0][0], botstruct[1][0]))
botstruct[0].append(calculateDestination(botstruct[1][0], botstruct[2][0]))
botstruct[1].append(calculateDestination(botstruct[2][0], botstruct[0][0]))

for bot in botstruct:
  cv2.circle(resized_image, bot[2], 3, (0,255,0))
  cv2.putText(resized_image, repr(bot[2]), bot[2], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))

cv2.imshow("ii", resized_image)

pprint(botstruct)

# now I have to find angles between destination and bot's direction
for bot in botstruct:
  deltaangle = getDeltaAngle(bot)

  print "for bot ({}, {}) deltaangle is {}".format(bot[0][0], bot[0][1], deltaangle)

"""
  if abs(deltaangle) < 5:
    # move forward
    ser.write('w')    
  elif deltaangle > 0:
    # move right
    ser.write('d')
  else:
    # move left 
    ser.write('a')
  sleep(0.2)
"""

cv2.waitKey(0)  
cv2.destroyAllWindows()
