import numpy as np
import cv2
from pprint import pprint

def getboxes(img, b_tuple, count):
  lower = np.array(b_tuple[0], dtype = "uint8")
  upper = np.array(b_tuple[1], dtype = "uint8")

  mask = cv2.inRange(img, lower, upper)
  output = cv2.bitwise_and(img, img, mask = mask)

 # output = cv2.resize(output, None, fx = 0.1, fy = 0.1, interpolation = cv2.INTER_CUBIC)
  cv2.imshow("ii", np.hstack([img, output]))
  cv2.waitKey(0)

  gray_img = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
  gray_img = cv2.blur(gray_img, (5,5))
  gray_img = cv2.bilateralFilter(gray_img, 20, 20, 20)
  edged = cv2.Canny(gray_img, 30, 200)
  edged = cv2.blur(edged, (5,5))
  cv2.imshow("ii", edged)
  cv2.waitKey(0)

  contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key = cv2.contourArea, reverse = True)[:count]
  #cv2.drawContours(img, contours, -1, (0,255,0), 3)
  cv2.imshow("ii", img)
  cv2.waitKey(0)

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

# reading image
img = cv2.imread('img\\6.jpg')
# resizing to fit the display
resized_image = cv2.resize(img, None, fx=0.1, fy=0.1, interpolation = cv2.INTER_CUBIC)

#cv2.namedWindow("Image", cv2.WINDOW_AUTOSIZE)
#cv2.imshow("Image", resized_image)

#define boundaries
boundaries = [
  ([150, 50, 0], [220, 155, 35]), # blue
  ([50, 110, 200], [110, 140, 255]),  # orange
  ([0, 170, 170], [40, 230, 240]), # yellow
  ([70, 130, 2], [150, 185, 85])  # green
]

# blue marks
bluemarks = getboxes(resized_image, boundaries[0], 3)

pprint(bluemarks)

bluecenters = []
for i in range(0, 3):
  bluecenters.append(center(bluemarks[i]))
  cv2.circle(resized_image, center(bluemarks[i]), 2, (0,0,255))

cv2.drawContours(resized_image, bluemarks, -1, (255,0,0), 2)
cv2.imshow("ii", resized_image)
cv2.waitKey(0)

botsboundaries = [] # orange, yellow and green boxes
for i in range(1, 4):
  boundary = getboxes(resized_image, boundaries[i], 1)
  botsboundaries.append(boundary[0])

pprint(botsboundaries)

botscenters = []
for i in range(0,3):
  botscenters.append(center(botsboundaries[i]))
  cv2.circle(resized_image, center(botsboundaries[i]), 3, (0,255,0))

cv2.drawContours(resized_image, botsboundaries, -1, (255,0,0), 2)
cv2.imshow("ii", resized_image)
cv2.waitKey(0)

# example of one box
# box = array([[ 74, 318],
#              [ 68, 186],
#              [147, 183],
#              [153, 315]])]

#cx, cy = centre(bluemarks[0])
#cv2.circle(resized_image, (cx,cy), 2, (0,0,255))
#cv2.imshow("ii", resized_image)
#cv2.waitKey(0)

"""
for (lower, upper) in boundaries:
  lower = np.array(lower, dtype = "uint8")
  upper = np.array(upper, dtype = "uint8")

  mask = cv2.inRange(img, lower, upper)
  output = cv2.bitwise_and(img, img, mask = mask)

  output = cv2.resize(output, None, fx = 0.1, fy = 0.1, interpolation = cv2.INTER_CUBIC)
  cv2.imshow("ii", np.hstack([resized_image, output]))
  cv2.waitKey(0)

  gray_img = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
  #ret,gray_img = cv2.threshold(gray_img, 5,255,cv2.THRESH_BINARY)
  gray_img = cv2.blur(gray_img, (5,5))
  gray_img = cv2.bilateralFilter(gray_img, 20, 20, 20)
  edged = cv2.Canny(gray_img, 30, 200)
  edged = cv2.blur(edged, (5,5))
  cv2.imshow("ii", edged)
  cv2.waitKey(0)

  contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key = cv2.contourArea, reverse = True)[:3]
  cv2.drawContours(resized_image, contours, 1, (0,255,0), 3)
  cv2.imshow("ii", resized_image)
  cv2.waitKey(0)

  rect = cv2.minAreaRect(contours[0])
  box = cv2.cv.BoxPoints(rect)
  box = np.int0(box)
  cv2.drawContours(resized_image, [box], 0, (255,0,0), 2)
  cv2.imshow("ii", resized_image)
  cv2.waitKey(0)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
"""

cv2.destroyAllWindows()
