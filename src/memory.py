import socket
import struct
import threading
import argparse
from device import Device
from array import array


multicast_group = '224.3.0.1'
server_address = ('', 10000)



class RAM(Device):
    def __init__(self,loc=0,size=2**16):
        Device.__init__(self,loc,size)
        self.storage = array('B',[0]*size)
    def read(self,address):
        return self.storage[unpacked_data[1]-self.loc]

    def write(self,address,data):
        self.storage[address-self.loc] = data
        return self.storage[unpacked_data[1]-self.loc]
            
class ROM(Device):
    def __init__(self,loc=0,data = []):
        Device.__init__(self,loc,len(data))
        self.storage = array('B',data)

    def read(self,address):
        return self.storage[unpacked_data[1]-self.loc]

    def write(self,address,data):
        return 0



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
    



