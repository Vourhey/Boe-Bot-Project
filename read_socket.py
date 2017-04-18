import socket

output = open('udpout.txt', 'w')

UDP_IP = "127.0.0.1"
UDP_PORT = 3333

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

try: 

  while True:
    data, addr = sock.recvfrom(65536) # buffer size is 1024 bytes
   # data  = repr(data)
    print "received message from {}: {}".format(addr, data)

    output.write(data)

except KeyboardInterrupt:
  pass

output.close()
