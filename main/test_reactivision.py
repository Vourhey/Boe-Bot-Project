import tuio
import time

tracking = tuio.Tracking()

try:
  while 1:
    #dt = datetime.now()
    for i in range(0, 200):
      tracking.update()
      time.sleep(0.001)
    #print "Time delta is ", datetime.now() - dt

    # find centers
    for obj in tracking.objects():
      print "id: {} X, Y = ({}, {}), angle = {}".format(obj.id, obj.xpos, obj.ypos, obj.angle)

except KeyboardInterrupt:
  tracking.stop()


