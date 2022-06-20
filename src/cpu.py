import socket
import struct


class DataBusInterface:
    
    multicast_group = ('224.3.0.1', 10000)
    def __init__(self,timeout = 0.2):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    def read(self,address):
        data = struct.pack('?HB',True,address,0)
        self.sock.sendto(data, self.multicast_group)
        try:
            data, server = self.sock.recvfrom(1)
            return struct.unpack('B',data)[0]
        except socket.timeout:
            print('Timed out, no more responses from DataBus!')
            return 0
    
    def write(self,address,data):
        data = struct.pack('?HB',False,address,data)
        self.sock.sendto(data, self.multicast_group)
        try:
            data, server = self.sock.recvfrom(1)
            return struct.unpack('B',data)[0] == data
        except socket.timeout:
            print('Timed out, no more responses from DataBus!')
            return False

