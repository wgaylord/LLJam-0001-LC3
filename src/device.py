import socket
import struct
import threading


multicast_group = '224.3.0.1'
server_address = ('', 10000)


class Device(threading.Thread):
    def __init__(self,loc=0,size=2**16):
        threading.Thread.__init__(self)
        self.loc = loc
        self.size = size
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(server_address)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    def run(self): #Allow run to be over-riden so devices can have their own loops. (Pygame based Display / Keyboard input device is an example.)
        while self.running:
            self.handleUDP()

    def handleUDP(self):
        data, sock_address = self.sock.recvfrom(10)
        unpacked_data = struct.unpack('?HB',data) #Format is Bool for read or write, 16-bit address, 8-bit data 
        if unpacked_data[1] >= self.loc and unpacked_data[1] < (self.loc+self.size):
            if unpacked_data[0]:
                self.sock.sendto(struct.pack('B', self.read(unpacked_data[1])),sock_address) #Always returns a byte
            else:
                self.sock.sendto(struct.pack('B', self.write(unpacked_data[1],data)), sock_address) #Always returns a byte
    
    
       
    def read(self,address):
        return 0
    
    def write(self,address,data):
        return data
