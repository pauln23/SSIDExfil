from scapy.all import *
from scapy.layers.dot11 import *
import re
import zlib
from codecs import encode
import sys

#Start character of info
startChar = '*'
# rdpcap to read pcap
packets = rdpcap(sys.stdin.read().strip())

def decompressData(compressedData):
    data = []
    print(len(compressedData))
    for x in compressedData:

        #Edit out fluff characters
        tmp = list(x)
        tmp[0] = ''
        tmp[1] = ''
        tmp[2] = ''
        tmp[-1] = ''
        tmp = ''.join(tmp)
        data.append(tmp)

    #Decompress
    print(data[0])
    print(data[1])
    print(data[2])
    print(data[3])
    print(data[4])
    print(data[5])
    data = (''.join(data))
    print(data)
    data = encode(data.encode().decode('unicode_escape'), "raw_unicode_escape")
    print(data)
    data = (zlib.decompress(data))
    return data


# Let's go through every packet in capture and look for ssid name
def getData(packets):
    compressedData = []
    for packet in packets:
        try:
            packet = packet.getlayer(Dot11Elt).info.decode('utf-8')
            if re.match('^[' + startChar + ']', packet):
                if packet not in compressedData:
                    compressedData.append(packet)

        except Exception as e:
            #Fails because packet has nothing in info field
            pass
    return compressedData

if __name__ == '__main__':
    compressedData = getData(packets)
    data = decompressData(compressedData)
    with open('exfiltratedData.txt','wb') as writer:
        writer.write(data)
        writer.close()

