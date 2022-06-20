import socket
import struct
import threading
import argparse
from array import array


multicast_group = '224.3.0.1'
server_address = ('', 10000)



class RAM(threading.Thread):
    def __init__(self,loc=0,size=2**16):
        threading.Thread.__init__(self)
        self.loc = loc
        self.size = size
        self.running = True
        self.storage = array('B',[0]*size)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(server_address)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    def run(self):
        while self.running:
            data, address = self.sock.recvfrom(10)
            print('Got request.')
            unpacked_data = struct.unpack('?HB',data) #Format is Bool for read or write, 16-bit address, 8-bit data
           
            if unpacked_data[1] >= self.loc and unpacked_data[1] < (self.loc+self.size):
                if unpacked_data[0]:
                    print('Its a read!')
                    print('Reading address',unpacked_data[1])
                    self.sock.sendto(struct.pack('B', self.storage[unpacked_data[1]-self.loc]),address) #Always returns a byte
                else:
                    print('Its a write!')
                    print('Writing',unpacked_data[2],"to address",unpacked_data[1])
                    self.storage[unpacked_data[1]-self.loc] = unpacked_data[2]
                    self.sock.sendto(struct.pack('B', self.storage[unpacked_data[1]-self.loc]), address) #Always returns a byte
            
    def stop(self):
        self.running = False
            
class ROM(threading.Thread):
    def __init__(self,loc=0,data = []):
        threading.Thread.__init__(self)
        self.loc = loc
        self.size = len(data)
        self.running = True
        self.storage = array('B',data)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(server_address)

        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)



    
    def run(self):
        while self.running:
            data, address = self.sock.recvfrom(4)
            print('Got request.')
            unpacked_data = struct.unpack('?HB',data)
            if unpacked_data[1] >= self.loc and unpacked_data[1] < (self.loc+self.size):
                if unpacked_data[0]:
                    print('Its a read!')
                    print('Reading address',unpacked_data[1])
                    self.sock.sendto(struct.pack('B',self.storage[unpacked_data[1]-self.loc]),address)
            
    def stop(self):
        self.running = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RAM/ROM Program')
    parser.add_argument('location', type=int,
                    help='Location in memory, please enter as an integer.')
    parser.add_argument('--length', type=int,
                    help='Length of the RAM region. ')
    parser.add_argument('--readonly', action='store_true',
                    help='Sets it to be a ROM.')
    parser.add_argument('--file', type=str,
                    help='ROM binary to load. Required while setting a ROM.')

    args = parser.parse_args()
    
    if(args.readonly):
        if(args.file):
            data = b''
            try:
                dfile = open(args.file,"rb")
                data = dfile.read()
                dfile.close()
            except Exception as E:
                print("Error: reading ROM binary file provided.")
                print(E)
                exit()

            thread = ROM(args.location,data)
            thread.start()
            print("Started ROM Thread")
            thread.join()
        else:
            print("Must provide a ROM binary to load.")
            exit()

    else:
        if(args.length):
            thread = RAM(args.location,args.length)
            thread.start()
            print("Started RAM Thread")
            thread.join()
        else:
            print("Must provide the length of the RAM region to be added.")
            exit()
    



